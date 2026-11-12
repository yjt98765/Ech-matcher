from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.ticker import LogLocator, NullFormatter


DATA_DIR = Path(__file__).resolve().parent.parent / "expected-results"
DEFAULT_RANDOM_INPUT = DATA_DIR / "random.dat"
DEFAULT_FIXED_INPUT = DATA_DIR / "fixed.dat"
DEFAULT_OUTPUT = DATA_DIR / "speedup.png"


@dataclass(frozen=True)
class Benchmark:
    name: str
    gates: int
    qubits: int
    qiskit_time: float
    hgraph_time: float

    @property
    def speedup(self) -> float:
        return self.qiskit_time / self.hgraph_time


def read_table(path: Path) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """Read a BOM-aware, whitespace-delimited table."""
    with path.open("rb") as raw_handle:
        byte_order_mark = raw_handle.read(2)
    encoding = "utf-16" if byte_order_mark in {b"\xff\xfe", b"\xfe\xff"} else "utf-8-sig"

    with path.open(encoding=encoding) as handle:
        numbered_lines = [
            (line_number, line.split())
            for line_number, line in enumerate(handle, start=1)
            if line.strip()
        ]

    if not numbered_lines:
        raise ValueError(f"{path} is empty")
    _, header = numbered_lines[0]
    rows = numbered_lines[1:]
    for line_number, row in rows:
        if len(row) != len(header):
            raise ValueError(
                f"{path}:{line_number}: expected {len(header)} columns, got {len(row)}"
            )
    return header, rows


def read_benchmarks(path: Path) -> list[Benchmark]:
    """Read arithmetic results using the current named-column schema."""
    header, rows = read_table(path)
    required = {"name", "gates", "qubits", "QTime", "HTime"}
    missing = required.difference(header)
    if missing:
        raise ValueError(f"{path} is missing columns: {', '.join(sorted(missing))}")

    column = {name: header.index(name) for name in required}
    benchmarks = [
        parse_benchmark(
            path=path,
            line_number=line_number,
            name=row[column["name"]],
            gates=row[column["gates"]],
            qubits=row[column["qubits"]],
            qiskit_time=row[column["QTime"]],
            hgraph_time=row[column["HTime"]],
        )
        for line_number, row in rows
    ]

    if not benchmarks:
        raise ValueError(f"{path} contains no benchmark rows")
    return benchmarks


def read_random_benchmarks(path: Path) -> list[Benchmark]:
    """Read random-circuit results; time_qh and gates_qh are intentionally ignored."""
    header, rows = read_table(path)
    required = {"gates", "nqubits", "time_q", "time_h"}
    missing = required.difference(header)
    if missing:
        raise ValueError(f"{path} is missing columns: {', '.join(sorted(missing))}")

    column = {name: header.index(name) for name in required}
    benchmarks = [
        parse_benchmark(
            path=path,
            line_number=line_number,
            name=f"random_{row[column['gates']]}",
            gates=row[column["gates"]],
            qubits=row[column["nqubits"]],
            qiskit_time=row[column["time_q"]],
            hgraph_time=row[column["time_h"]],
        )
        for line_number, row in rows
    ]
    if not benchmarks:
        raise ValueError(f"{path} contains no random-circuit rows")
    return benchmarks


def parse_benchmark(
    *,
    path: Path,
    line_number: int,
    name: str,
    gates: str,
    qubits: str,
    qiskit_time: str,
    hgraph_time: str,
) -> Benchmark:
    """Convert and validate one benchmark row."""
    try:
        benchmark = Benchmark(
            name=name,
            gates=int(gates),
            qubits=int(qubits),
            qiskit_time=float(qiskit_time),
            hgraph_time=float(hgraph_time),
        )
    except ValueError as error:
        raise ValueError(f"{path}:{line_number}: invalid numeric value") from error

    if benchmark.gates <= 0 or benchmark.qubits <= 0:
        raise ValueError(f"{path}:{line_number}: gates and qubits must be positive")
    if benchmark.qiskit_time <= 0 or benchmark.hgraph_time <= 0:
        raise ValueError(f"{path}:{line_number}: runtimes must be positive")
    return benchmark


def plot_benchmarks(
    benchmarks: list[Benchmark],
    random_benchmarks: list[Benchmark],
    output: Path,
    dpi: int,
) -> None:
    """Create a publication-style log-log speed-up scatter plot."""
    gate_counts = [item.gates for item in benchmarks]
    speedups = [item.speedup for item in benchmarks]
    random_gate_counts = [item.gates for item in random_benchmarks]
    random_speedups = [item.speedup for item in random_benchmarks]
    qubit_counts = [item.qubits for item in benchmarks]
    random_qubit_counts = [item.qubits for item in random_benchmarks]
    all_qubit_counts = qubit_counts + random_qubit_counts

    plt.rcParams.update(
        {
            "font.size": 13,
            "axes.labelsize": 17,
            "axes.titlesize": 18,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 13,
            "axes.linewidth": 1.25,
        }
    )

    figure, axis = plt.subplots(figsize=(7.6, 5), constrained_layout=True)
    normalization = Normalize(vmin=min(all_qubit_counts), vmax=max(all_qubit_counts))
    points = axis.scatter(
        gate_counts,
        speedups,
        c=qubit_counts,
        cmap="viridis",
        norm=normalization,
        marker="^",
        s=115,
        edgecolors="#303030",
        linewidths=0.8,
        alpha=0.96,
        zorder=3,
    )
    axis.scatter(
        random_gate_counts,
        random_speedups,
        c=random_qubit_counts,
        cmap="viridis",
        norm=normalization,
        marker="o",
        s=105,
        edgecolors="#303030",
        linewidths=0.8,
        alpha=0.96,
        zorder=3,
    )

    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel("number of gates", labelpad=8)
    axis.set_ylabel("speed-up  (Qiskit / ECH)", labelpad=9)

    # Preserve the clean look of the reference while retaining minor log ticks.
    for scale_axis in (axis.xaxis, axis.yaxis):
        scale_axis.set_major_locator(LogLocator(base=10))
        scale_axis.set_minor_locator(LogLocator(base=10, subs=range(2, 10)))
        scale_axis.set_minor_formatter(NullFormatter())
    axis.tick_params(which="major", direction="out", length=7, width=1.2, pad=6)
    axis.tick_params(which="minor", direction="out", length=3.5, width=0.9)
    axis.margins(x=0.08, y=0.12)

    arithmetic_legend = Line2D(
        [],
        [],
        linestyle="none",
        marker="^",
        markersize=10,
        markerfacecolor=plt.colormaps["viridis"](0.12),
        markeredgecolor="#303030",
        markeredgewidth=0.8,
        label="fixed (1 template)",
    )
    random_qubits = {item.qubits for item in random_benchmarks}
    random_label = (
        f"random (47 templates)"
        if len(random_qubits) == 1
        else "random"
    )
    random_legend = Line2D(
        [],
        [],
        linestyle="none",
        marker="o",
        markersize=9,
        markerfacecolor=plt.colormaps["viridis"](normalization(random_qubit_counts[0])),
        markeredgecolor="#303030",
        markeredgewidth=0.8,
        label=random_label,
    )
    axis.legend(
        handles=[arithmetic_legend, random_legend], loc="upper left", frameon=False
    )

    colorbar = figure.colorbar(points, ax=axis, pad=0.025, fraction=0.055)
    colorbar.set_label("qubits", rotation=90, labelpad=10)
    colorbar.outline.set_linewidth(1.2)

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot Qiskit/H-graph speed-up across the fixed NRS benchmarks."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_FIXED_INPUT)
    parser.add_argument("--random-input", type=Path, default=DEFAULT_RANDOM_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dpi", type=int, default=300)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    benchmarks = read_benchmarks(args.input)
    random_benchmarks = read_random_benchmarks(args.random_input)
    plot_benchmarks(benchmarks, random_benchmarks, args.output, args.dpi)
    total = len(benchmarks) + len(random_benchmarks)
    print(
        f"Saved {total} benchmarks "
        f"({len(benchmarks)} arithmetic, {len(random_benchmarks)} random) "
        f"to {args.output.resolve()}"
    )


if __name__ == "__main__":
    main()
