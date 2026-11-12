from . import *
from ..graph import Circuit

_NCT_PATTERN_FACTORIES = (
    nct_2a_1,
    nct_2a_2,
    nct_2a_3,
    nct_4a_1,
    nct_4a_2,
    nct_4a_3,
    nct_4b_1,
    nct_4b_2,
    nct_5a_1,
    nct_5a_2,
    nct_5a_3,
    nct_5a_4,
    nct_6a_1,
    nct_6a_2,
    nct_6a_3,
    nct_6a_4,
    nct_6b_1,
    nct_6b_2,
    nct_6c_1,
    nct_7a_1,
    nct_7b_1,
    nct_7e_1,
    nct_7c_1,
    nct_7d_1,
    nct_9a_1,
    nct_9c_1,
    nct_9c_2,
    nct_9c_3,
    nct_9c_4,
    nct_9c_5,
    nct_9c_6,
    nct_9c_7,
    nct_9c_8,
    nct_9c_9,
    nct_9c_10,
    nct_9c_11,
    nct_9c_12,
    nct_9d_1,
    nct_9d_2,
    nct_9d_3,
    nct_9d_4,
    nct_9d_5,
    nct_9d_6,
    nct_9d_7,
    nct_9d_8,
    nct_9d_9,
    nct_9d_10,
)

_PATTERN_FACTORIES = (
    clifford_2_1,
    clifford_2_2,
    clifford_2_3,
    clifford_2_4,
    clifford_3_1,
    clifford_4_1,
    clifford_4_2,
    clifford_4_3,
    clifford_4_4,
    clifford_5_1,
    clifford_6_1,
    clifford_6_2,
    clifford_6_3,
    clifford_6_4,
    clifford_6_5,
    clifford_8_1,
    clifford_8_2,
    clifford_8_3,
)

def get_all_nct_patterns() -> list[Circuit]:
    """Return fresh instances of all built-in patterns."""
    return [factory() for factory in _NCT_PATTERN_FACTORIES]

def get_all_patterns() -> list[Circuit]:
    """Return fresh instances of all built-in patterns."""
    return get_all_nct_patterns() + [factory() for factory in _PATTERN_FACTORIES]
