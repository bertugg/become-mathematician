# Session 1 — Slot Math Fundamentals & Game Specification

Status: ✅ COMPLETE (2026-10-27)

## Learner diagnostic
- Comfortable with Python.
- Basic probability.
- Has developed slot game frontends, so knows the vocabulary but not the math backend.
- Studies in the evenings and sometimes skips sessions. "Day N" means session N.

## Roadmap (~3 h per session, 21 h max)
| Session | Focus | Milestone |
|---|---|---|
| 1 | Reel strips, stops, line probabilities, EV/variance basics | Game config in Python + hand-checked probabilities |
| 2 | Combinatorics and exact RTP | Single-line RTP calculator with a per-symbol contribution table |
| 3 | Window, payline evaluator, wilds, no double counting | Tested evaluator + exact full-cycle enumeration |
| 4 | Monte Carlo, law of large numbers, confidence intervals | Simulation that agrees with exact RTP within its CI |
| 5 | Volatility, hit frequency, max win, balancing | Two configs at the target RTP with different "feel" |
| 6 | Free spins as a state model; auditing a flawed model | Feature RTP contribution + a written audit review |
| 7 | Math sheet, README, career module, mock interview | Portfolio package + competency assessment |

## The game
See `spec/design_brief.md`. Ember Forge is a fictional 5×3 slot with 10 paylines and a total bet of 10 credits (1 per line). Each reel has 30 stops, and the wild appears only on reels 2–4.

---

## Lesson 1: Where slot probabilities come from
- **Reel strip:** the fixed, ordered list of symbols on one reel. 
- **Reel stop:** the strip position the reel lands on. Every stop is equally likely.
- **P(a row of a reel shows S)** = count of S on the strip ÷ strip length. For example, P(R1 shows L2) = 9/30 = 0.30.
- **The reels are independent**, so for one payline the probabilities **multiply** across reels.
  Example: P(L2, L2, L2 on reels 1–3, no wilds) = (9/30)(8/30)(8/30) ≈ 0.0213.
- The maths is set by the **counts on the strips**, not by how many symbol types exist. Seven symbol types does not mean each has a 1/7 chance.
- **Appears vs wins vs pays** are three different events:
  - a symbol *appears* on the grid;
  - a *winning combination* forms under the rules;
  - a *payout* is awarded through the paytable.
- **RTP** = E[spin payout] ÷ total bet. It is a long-run average and says nothing about a single session.

## Lesson 2: Expected value and variance refresher
- **Random variable** X = payout of one spin.
- **Expected value:** E[X] = Σ pᵢ·xᵢ, the long-run average per spin.
- **Variance:** Var(X) = E[X²] − E[X]². Standard deviation σ = √Var. Variance is the mathematical core of *volatility*.
- **Hit frequency** = P(payout > 0). This is **not** the same as P(net win), because a payout can be smaller than the bet.

### Worked example (bet = 1)
| Outcome |  p   | payout (x) | pᵢ·xᵢ   | 
|---------|------|------------|---------|
| lose    | 0.70 |    0       | 0.70 * 0
| small   | 0.29 |    2       | 0.29 * 2
| jackpot | 0.01 |    38      | 0.01 * 38

- E[X] = 0.58 + 0.38 = **0.96**, so RTP = 96%.
- E[X²] = 1.16 + 14.44 = 15.60, so Var ≈ 14.68 and σ ≈ **3.83**. (Volatility)
- Hit frequency = 0.29 + 0.01 = **30%**.
- Lesson: the rare jackpot drives the variance, while the frequent small wins drive the hit rate. Two games can share the same RTP and still feel very different.

---

## Exercises (submit answers to Claude for review)

### Quick check
What fraction of the toy game's RTP comes from the jackpot? 
0.38 / 0.96 = around %40 of spins
What does that imply for a player who plays only 50 spins?
around 0.60 wins without jackpot. 0.60 * 0.58 => %36 RTP on 50 spins

### Exercise 1.1: by hand, on ONE payline, using fractions
1. What is P(reel 1 shows H1)?
2. What is P(H1 H1 H1 H1 H1), using real H1s only and no wilds?
3. What is P(the line pays **5-of-a-kind H1**), with wilds allowed?
4. What is P(the line pays **exactly 3-of-a-kind H1**)?
5. Give one concrete line where H1 appears 3 times but the line does **not** pay 3-of-a-kind H1.

Hints:
- Q3: on reels 2–4, which outcomes count as a match?
- Q4: rule 3 says each line pays only its longest run. Think about what reel 4 must *not* show, and whether reel 5 matters.

### Exercise 1.2: Python
Create `ember_forge/config.py` containing:
- the symbol counts for each reel;
- the paytable;
- `p_symbol(reel: int, symbol: str) -> Fraction`, using `fractions.Fraction`;
- a sanity check that each reel sums to 30.

Use `p_symbol` to verify your answers to Q1–Q4.

## Your answers / notes
1. P(R1 shows H1) is possibility to have H1 in Reel 1. H1 Count /  R1 Length
2. P(H1 H1 H1 H1 H1) is (H1/R1) * (H1/R2) * (H1/R3) * (H1/R4) * (H1/R5)
3. (H1/R1) * ((H1+W)/R2) * ((H1+W)/R3) * ((H1+W)/R4) * ((H1+W)/R5) where W is Wild
4. (H1/R1) * (H1+W/R2) * (H1+W/R3) * ((R4-(H1+ W)/R4))
5. Explain the solution

## Review feedback
**Round 1 (formulas):**
- Q1 ✅ The formula is right. Now write the number as a fraction.
- Q2 ✅ The structure is right: reels are independent, so multiply. Now give the number.
- Q3 ✅ Correct. Note that reel 5 has W = 0, so (H1+W)/R5 equals H1/R5. It works here, but say why.
- Q4 ⚠️ There are two issues to fix:
  - Reels 2–3: can a wild help form the 3-of-a-kind? (Compare with your Q3.)
  - Reel 4 must *break* the run. Which symbols on reel 4 would *continue* it?
  - Reel 5: once reel 4 breaks the run, does reel 5 still affect whether the line pays 3-of-a-kind?
- Q5 is missing.
- Next: give numbers for Q1–Q3 and a corrected Q4, then check them with `config.py`.

**Round 2:**
- Q4 ✅ The logic is now correct: reels 2–3 allow H1 or W, reel 4 must be neither H1 nor W, and reel 5 doesn't matter. Two things to tidy:
  - Bracketing: `H1+W/R2` means H1 + (W/R2). Write `(H1+W)/R2` and `(R4-H1-W)/R4`.
  - Sanity check: reel 4's factor plus the "continue the run" factor must equal 1, since (H1+W)/R4 + (R4-H1-W)/R4 = 1.
- Q5 (solution, on request): see the explanation below.
  - `H1 H1 L2 H1 L1`: H1 appears 3 times, but the run from reel 1 breaks at reel 3, so there's no win.
  - `L2 H1 H1 H1 M1`: H1 appears 3 times, but reel 1 isn't H1. Reel 1 decides the symbol, so this pays nothing.
  - `H1 H1 H1 H1 L2`: this pays 4-of-a-kind (100). A line pays only its longest run, so it is not also a 3-kind win.
  - Lesson: a win depends on **position and order along the line**, not on how many times a symbol appears. Counting symbols on the grid is not the same as evaluating wins.
- Still open:
  - numeric answers for Q2–Q4, computed with `p_symbol` in the `__main__` block;
  - `check_config` checks only reel 1 and should check all 5;
  - the quick-check question.

**Round 3 (code):** ✅ Q1–Q4 are verified by code.
| Q | Exact | ≈ 1 in |
|---|---|---|
| Q1 | 1/15 | 15 |
| Q2 | 1/759375 | 759,375 |
| Q3 | 8/759375 | 94,922 |
| Q4 | 52/50625 | 974 |

- Insight: Q3 / Q2 = 8 exactly. Each of the 3 wild reels doubles the matching chances (H1 2 → H1+W 4), so the 5-of-a-kind probability goes up by 2³ = 8. **Wild placement is a powerful lever.**
- Still open:
  - `check_config` checks only reel 1;
  - the Q4 sanity-check print;
  - the quick-check question.

**Round 4:** ✅ `check_config` checks all reels. Verified: adding one extra L1 to reel 3 raises "reel 3 has 31 symbols, expected 30".
- Style notes (optional; they match Python conventions reviewers expect):
  - Use `snake_case` for variable names (`reel_index`, not `reelIndex`).
  - Prefer `for number, counts in enumerate(REEL_COUNTS, start=1):` to looping over `range(len(...))`.
  - Delete TODO comments once they're done.
- Still open: the quick-check question.

**Round 5 (quick check):**
- Part 1 ✅ 0.38 / 0.96 ≈ 40%, but this is 40% **of the RTP (payout)**, not "of spins". The jackpot happens on only 1% of spins. Keep units precise: probability, payout and RTP are different quantities.
- Part 2 ⚠️ P(no jackpot in 50 spins) = 0.99^50 ≈ **0.605** ✅. But 0.60 × 0.58 mixes two separate things:
  - 0.60 is the **probability of being in the "no jackpot" group**. It is not a factor on the return.
  - A player in that group gets about **58%** average return, well below 96%.
  - The other ~40% hit at least one jackpot. A single jackpot pays 38 on a 50-credit stake, which is 76% of the stake from one hit, so these players end up well above 96%.
  - Averaged over everyone, the result is still 96%. The median player sits below the mean.
- **Lesson:** RTP is a long-run average. When a large share of the RTP sits in rare events, **most short sessions return less than the RTP**. That is what high volatility feels like to a player (Session 5).


---

## Session 1 wrap-up

### Knowledge test (answer briefly)
1. A colleague moves 2 stops on reel 2 from L2 to W, so reel 2 now has W = 4 and L2 = 6. By what exact factor does P(line pays 5-of-a-kind H1) change? Which other wins also become more likely?
it becomes  8/759375 to 4/253125
2. A spin pays 5 credits on a 10-credit total bet. Is it a **hit**? Is it a **net win**? Why does this distinction matter when you report hit frequency?
no it is less than the bet. so it is a lose by 5.
3. Someone says "there are 7 symbols, so P(reel 1 shows H1) = 1/7." Explain the error with the actual numbers.
 {"W": 0, "H1": 2, "H2": 3, "M1": 4, "M2": 5, "L1": 7, "L2": 9},  # reel 1
 so the reel has 2 h1 while whole reel has 30 symbols in total. that s why it is NOT 1/7

### Milestone
- `ember_forge/config.py` holds the reel counts and paytable, provides exact `p_symbol`, and validates the config.
- Hand-derived line probabilities are verified exactly by code.

### How this maps to the job
- A slot mathematician's first deliverable is a **par sheet / math spec**: reel configuration, paytable, and the probability of each winning event. That is what you started today.
- A config validation like `check_config` mirrors real practice. Strip typos are one of the most common causes of RTP mismatches in production.

### Key lessons
- Probabilities come from **strip counts**, not from the number of symbol types.
- Independent reels → **multiply**; "run stops here" → use the **complement**.
- Wins depend on **position and order** along a line, not on how often a symbol appears.
- RTP is a **long-run mean**. When RTP is concentrated in rare wins, most short sessions return less than the RTP.

### Next session starts with
Session 2: turn probabilities into an **exact RTP**. For every symbol and run length: P(win) × pay = contribution to RTP. You'll build the full contribution table for one line.

### Knowledge test review
1. ⚠️ Partial. 4/253125 = 12/759375 is the right value, but give the **factor**: 12/8 = **1.5**, which comes from reel 2's H1 matches going from 2+2 to 2+4, i.e. 6/4.
   - Missed part: H2, M1, M2 and L1 wins also become more likely, because W counts for every symbol.
   - Trap: **L2 wins don't change**. L2+W on reel 2 is 8+2 = 10 before and 6+4 = 10 after.
   - Lesson: converting a symbol into a wild redistributes probability. It doesn't just add wins.
2. ⚠️ Partial. It **is a hit**, because hit = any payout > 0. It is **not a net win** (net −5). That's why hit frequency always overstates how often players actually come out ahead, and why reports must keep the two separate.
3. ✅ Correct: 2/30 = 1/15 ≈ 6.7%, not 1/7 ≈ 14.3%. Bonus: reel 1 has no W, so it doesn't even have 7 symbol types, only 6.

### Session 1 assessment
- Strengths: you translate rules into probability formulas quickly and verify them in code.
- Watch: **units and definitions** (hit vs net win, share of RTP vs share of spins). Interviews test these directly.

