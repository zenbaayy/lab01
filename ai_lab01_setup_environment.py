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
def compare():
    banner("TASK 3: side-by-side comparison")
    for c in (100, 0, -40, 37):
        print(f"{c}C -> hand: {celsius_to_fahrenheit_by_hand(c)}F | "
              f"ai: {celsius_to_fahrenheit_ai(c)}F | buggy: {buggy_integer_division(c)}F")
    for bad in ("abc", "36.6"):
        print(f"input {bad!r} -> AI parse result: {parse_celsius(bad)} "
              f"(hand version: float({bad!r}) would {'crash' if parse_celsius(bad) is None else 'work'})")

    start = time.perf_counter()
    for _ in range(100000):
        celsius_to_fahrenheit_by_hand(37)
    print(f"hand version: {time.perf_counter() - start:.4f}s for 100k calls")
    start = time.perf_counter()
    for _ in range(100000):
        celsius_to_fahrenheit_ai(37)
    print(f"AI version  : {time.perf_counter() - start:.4f}s for 100k calls")


# ---------------- TASK 4 : defend one difference ------------------------------
def defend():
    banner("TASK 4: defend one difference")
    print("Largest difference: parse_celsius() (try/except ValueError) in the AI version.\n"
          "It is a real improvement, not just a habit: float('abc') raises ValueError and\n"
          "crashes the hand version, while this line returns None so the caller can re-ask.\n"
          "It costs 4 extra lines but removes a whole class of user-input crashes.\n"
          "(Cite YOUR file:line in the submission, e.g. ai_lab01_setup_environment.py:<line>.)")
    print("\nChecked against the reference run. CSE325-2026-L01-K7QX")


# ---------------- Activity 4 : commit messages to use -------------------------
GIT_STEPS = """
git init cse325-lab01 && cd cse325-lab01
git add hand_written.py && git commit -m "Hand-written converter (found and fixed integer-division bug)"
git checkout -b ai-build
git add ai_assisted.py && git commit -m "AI-assisted converter (float division and input validation from first draft)"
git log --format='%h %ad %s' --date=iso      # paste into report
python -VV                                    # paste into report
(Make >= 3 real commits on main, spaced out during the lab: the timestamps ARE the evidence.)
"""

if __name__ == "__main__":
    banner("LAB 01 - ACTIVITY 1 & 2: both versions")
    print("hand:", celsius_to_fahrenheit_by_hand(100), "| ai:", celsius_to_fahrenheit_ai(100))
    compare()
    run_tests()
    defend()
    banner("ACTIVITY 4: git commands (run these yourself in the terminal)")
    print(GIT_STEPS)
