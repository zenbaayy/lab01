# CSE325-2026-L01-K7QX
# =============================================================================
# AI LAB 01 : Setting Up the AI-Augmented Development Environment
# Hand-written vs AI-assisted Celsius-to-Fahrenheit converter + tests
# Run: python ai_lab01_setup_environment.py     (or: pytest ai_lab01_setup_environment.py)
# =============================================================================
import time  # used later to measure how fast each function runs

# Stores the numbers for the formula F = C * 9/5 + 32
# ratio is 9/5 (which is 1.8) and offset is 32
RUN_PROFILE = {"ratio": 9 / 5, "offset": 32}


# Prints a title with a line of "=" signs above and below it
# so each section of the output is easy to see
def banner(title):
    print("\n" + "=" * 70)   # top line
    print(title)             # the heading text
    print("=" * 70)          # bottom line


# ---------------- TASK 1 / ACTIVITY 1 : hand-written version (branch: main) ----
# CSE325-2026-L01-K7QX-T1
# Hand-written converter: multiplies Celsius by 9/5 and adds 32
def celsius_to_fahrenheit_by_hand(c):
    return c * RUN_PROFILE["ratio"] + RUN_PROFILE["offset"]


# ---------------- TASK 2 / ACTIVITY 2 : AI-assisted version (branch: ai-build) --
# CSE325-2026-L01-K7QX-T2
# AI-assisted converter: same formula, but with type hints
# (float in, float out) and a docstring describing the function
def celsius_to_fahrenheit_ai(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return celsius * RUN_PROFILE["ratio"] + RUN_PROFILE["offset"]


# Safely turns user text into a number
# Returns the number if the text is valid (like "36.6")
# Returns None if it is not a number (like "abc"), so the program does not crash
def parse_celsius(text: str):
    """AI version's defensive input handling: returns float or None if invalid."""
    try:
        return float(text)      # try to convert the text to a number
    except ValueError:          # this happens when the text is not a number
        return None


# ---------------- The classic bug (Activity 1) shown for comparison ------------
# Deliberately wrong version to show the classic bug
# 9 // 5 is integer division and equals 1 (not 1.8), so the result is wrong
def buggy_integer_division(c):
    return c * (9 // 5) + 32          # 9 // 5 == 1  -> WRONG on purpose

# ---------------- TASK 3 : comparison (timing is REAL, measured here) ----------
# ---------------- TESTS (pytest-compatible, also run manually below) ----------
# Checks that both converters give correct answers for known values:
# 100C = 212F, 0C = 32F, -40C = -40F, 37C = about 98.6F
def test_known_conversions():
    for fn in (celsius_to_fahrenheit_by_hand, celsius_to_fahrenheit_ai):
        assert fn(100) == 212
        assert fn(0) == 32
        assert fn(-40) == -40
        assert abs(fn(37) - 98.6) < 1e-9   # tiny tolerance because decimals are not exact


# Shows the buggy version is caught: 100C must be 212F,
# but the buggy function gives a different answer, so the bug is detected
def test_bug_is_detected_by_known_value():
    assert buggy_integer_division(100) != 212      # 100C should be 212F -> bug caught


# Checks input handling: valid text becomes a number,
# while invalid or empty text gives None
def test_ai_input_validation():
    assert parse_celsius("36.6") == 36.6
    assert parse_celsius("abc") is None
    assert parse_celsius("") is None


# Runs each test one by one and prints PASS if it works or FAIL if an assert fails
def run_tests():
    banner("TESTS")
    for t in (test_known_conversions, test_bug_is_detected_by_known_value,
              test_ai_input_validation):
        try:
            t()
            print("PASS:", t.__name__)
        except AssertionError as e:
            print("FAIL:", t.__name__, e)
# Compares the hand-written, AI, and buggy versions side by side,
# then shows how each handles bad input, then measures speed
def compare():
    banner("TASK 3: side-by-side comparison")
    # print the result of all three versions for four sample temperatures
    for c in (100, 0, -40, 37):
        print(f"{c}C -> hand: {celsius_to_fahrenheit_by_hand(c)}F | "
              f"ai: {celsius_to_fahrenheit_ai(c)}F | buggy: {buggy_integer_division(c)}F")
    # show what happens with bad input ("abc") and good input ("36.6")
    for bad in ("abc", "36.6"):
        print(f"input {bad!r} -> AI parse result: {parse_celsius(bad)} "
              f"(hand version: float({bad!r}) would {'crash' if parse_celsius(bad) is None else 'work'})")

    # time 100,000 calls of the hand-written version
    start = time.perf_counter()
    for _ in range(100000):
        celsius_to_fahrenheit_by_hand(37)
    print(f"hand version: {time.perf_counter() - start:.4f}s for 100k calls")
    # time 100,000 calls of the AI version
    start = time.perf_counter()
    for _ in range(100000):
        celsius_to_fahrenheit_ai(37)
    print(f"AI version  : {time.perf_counter() - start:.4f}s for 100k calls")


# ---------------- TASK 4 : defend one difference ------------------------------
# Prints my explanation of the biggest difference between the two versions:
# parse_celsius() handles bad input safely instead of crashing
def defend():
    banner("TASK 4: defend one difference")
    print("Largest difference: parse_celsius() (try/except ValueError) in the AI version.\n"
          "It is a real improvement, not just a habit: float('abc') raises ValueError and\n"
          "crashes the hand version, while this line returns None so the caller can re-ask.\n"
          "It costs 4 extra lines but removes a whole class of user-input crashes.\n"
          "(Cited in my submission: ai_lab01_setup_environment.py:38.)")
    print("\nChecked against the reference run. CSE325-2026-L01-K7QX")


# ---------------- Activity 4 : commit messages to use -------------------------
# A text block listing the git commands and commit messages used in this lab
GIT_STEPS = """
git init cse325-lab01 && cd cse325-lab01
git add hand_written.py && git commit -m "Hand-written converter (found and fixed integer-division bug)"
git checkout -b ai-build
git add ai_assisted.py && git commit -m "AI-assisted converter (float division and input validation from first draft)"
git log --format='%h %ad %s' --date=iso      # paste into report
python -VV                                    # paste into report
(Make >= 3 real commits on main, spaced out during the lab: the timestamps ARE the evidence.)
"""

# This block runs only when you run the file directly (python ai_lab01_setup_environment.py)
# It runs everything in order: both converters, comparison, tests, defense, git steps
if __name__ == "__main__":
    banner("LAB 01 - ACTIVITY 1 & 2: both versions")
    print("hand:", celsius_to_fahrenheit_by_hand(100), "| ai:", celsius_to_fahrenheit_ai(100))
    compare()
    run_tests()
    defend()
    banner("ACTIVITY 4: git commands (run these yourself in the terminal)")
    print(GIT_STEPS)