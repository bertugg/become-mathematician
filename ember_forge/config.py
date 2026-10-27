"""Ember Forge game configuration: reel symbol counts and paytable."""

from fractions import Fraction

REEL_LENGTH = 30

# Symbol counts per reel. List index 0 = reel 1.
REEL_COUNTS = [
    {"W": 0, "H1": 2, "H2": 3, "M1": 4, "M2": 5, "L1": 7, "L2": 9},  # reel 1
    {"W": 4, "H1": 2, "H2": 3, "M1": 4, "M2": 5, "L1": 6, "L2": 6},  # reel 2
    {"W": 2, "H1": 2, "H2": 3, "M1": 4, "M2": 5, "L1": 6, "L2": 8},  # reel 3
    {"W": 2, "H1": 2, "H2": 3, "M1": 4, "M2": 5, "L1": 6, "L2": 8},  # reel 4
    {"W": 0, "H1": 2, "H2": 3, "M1": 4, "M2": 5, "L1": 7, "L2": 9},  # reel 5
]

# Pays in line-bet multiples: symbol -> {run length: pay}
PAYTABLE = {
    "H1": {3: 20, 4: 100, 5: 500},
    "H2": {3: 15, 4: 60, 5: 250},
    "M1": {3: 10, 4: 40, 5: 150},
    "M2": {3: 8, 4: 25, 5: 100},
    "L1": {3: 5, 4: 15, 5: 50},
    "L2": {3: 4, 4: 10, 5: 40},
}


def p_symbol(reel: int, symbol: str) -> Fraction:
    """Probability that one row of `reel` (1-5) shows `symbol`."""
    return Fraction(REEL_COUNTS[reel - 1].get(symbol, 0), REEL_LENGTH)   


def check_config() -> None:
    """Fail loudly if the config is inconsistent."""
    for reel_index in range(len(REEL_COUNTS)):
        if sum (REEL_COUNTS[reel_index].values()) != REEL_LENGTH:
            raise ValueError(f"reel {reel_index + 1} has {sum(REEL_COUNTS[reel_index].values())} symbols, expected {REEL_LENGTH}")

if __name__ == "__main__":
    check_config()
    print("Q1:", p_symbol(1, "H1"))
    print("Q2:", p_symbol(1, "H1") * p_symbol(2, "H1") * p_symbol(3, "H1") * p_symbol(4, "H1") * p_symbol(5, "H1"))
    print("Q3:", p_symbol(1, "H1") * (p_symbol(2, "H1") + p_symbol(2, "W")) * (p_symbol(3, "H1") + p_symbol(3, "W")) * (p_symbol(4, "H1") + p_symbol(4, "W")) * p_symbol(5, "H1"))
    print("Q4:", p_symbol(1, "H1") * (p_symbol(2, "H1") + p_symbol(2, "W")) * (p_symbol(3, "H1") + p_symbol(3, "W")) * (1 - p_symbol(4, "H1") - p_symbol(4, "W")))
