import argparse
import sys
import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ech_matcher.graph import gen_cir2
from ech_matcher.match import opt_a_circuit
from ech_matcher.patterns.nct.nct_5a_3 import nct_5a_3


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the gate-count scalability experiment and save its plot."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reproduced-scale.png"),
        help="output image path (default: reproduced-scale.png)",
    )
    parser.add_argument("--min-gates", type=int, default=10)
    parser.add_argument("--max-gates", type=int, default=4010)
    parser.add_argument("--step", type=int, default=50)
    parser.add_argument("--repetitions", type=int, default=15)
    args = parser.parse_args()

    if args.min_gates <= 0 or args.max_gates < args.min_gates:
        parser.error("gate counts must be positive and max-gates must be at least min-gates")
    if args.step <= 0 or args.repetitions <= 0:
        parser.error("step and repetitions must be positive")
    if len(range(args.min_gates, args.max_gates + 1, args.step)) < 3:
        parser.error("the quadratic fit requires at least three circuit sizes")
    return args


def run_experiment(gate_counts, repetitions):
    template = nct_5a_3()
    elapsed_means = []
    elapsed_deviations = []
    reduced_gate_means = []

    print("original gate#", end="\t")
    for iteration in range(repetitions):
        print(f"iter_{iteration}", end="\t")
    print("average time", "deviation", "average new gates", sep="\t")

    for gate_count in gate_counts:
        print(gate_count, end="\t", flush=True)
        elapsed_times = []
        optimized_gate_counts = []

        for iteration in range(repetitions):
            seed = gate_count * 100 + iteration
            circuit = gen_cir2(
                "Random_X_CX_CCX", 6, gate_count, seed=seed
            )

            start = time.perf_counter()
            optimized = opt_a_circuit(circuit, template)
            elapsed = time.perf_counter() - start
            elapsed_times.append(elapsed)
            optimized_gate_counts.append(optimized.gates_num())
            print(elapsed, end="\t", flush=True)

        elapsed_mean = np.average(elapsed_times)
        elapsed_deviation = np.std(elapsed_times)
        optimized_gate_mean = np.average(optimized_gate_counts)
        print(
            elapsed_mean,
            elapsed_deviation,
            optimized_gate_mean,
            sep="\t",
            flush=True,
        )
        elapsed_means.append(elapsed_mean)
        elapsed_deviations.append(elapsed_deviation)
        reduced_gate_means.append(gate_count - optimized_gate_mean)

    return elapsed_means, elapsed_deviations, reduced_gate_means


def plot_results(gate_counts, elapsed_means, elapsed_deviations, reduced_gate_means):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.errorbar(
        gate_counts,
        elapsed_means,
        yerr=elapsed_deviations,
        fmt="o",
        color="blue",
        alpha=0.3,
        label="Average Time",
        capsize=3,
    )
    ax1.plot(gate_counts, elapsed_means, color="blue")
    ax2.plot(
        gate_counts,
        reduced_gate_means,
        color="green",
        linestyle="--",
        label="Reduced gate #",
    )

    coefficients = np.polyfit(gate_counts, elapsed_means, 2)
    message = (
        "Fitted curve:\n"
        f"y = {coefficients[0]:.3e}x^2 "
        f"{coefficients[1]:+.3e}x {coefficients[2]:+.3e}"
    )
    print(message)
    fitted_times = np.polyval(coefficients, gate_counts)
    ax1.plot(
        gate_counts,
        fitted_times,
        color="red",
        linestyle="--",
        label="Poly Fit (deg=2)",
    )
    ax1.text(
        0.03,
        0.97,
        message,
        transform=ax1.transAxes,
        va="top",
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "gray"},
    )

    ax1.set_xlabel("x: # circuit gates")
    ax1.set_ylabel("y: Time (s)")
    ax2.set_ylabel("y2: Reduced gate #")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2)
    fig.tight_layout()
    return fig


def main():
    args = parse_args()
    gate_counts = list(range(args.min_gates, args.max_gates + 1, args.step))
    results = run_experiment(gate_counts, args.repetitions)
    figure = plot_results(gate_counts, *results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=300)
    plt.close(figure)
    print(f"Saved plot to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
