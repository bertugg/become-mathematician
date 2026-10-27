# Session 1 — Slot Math Fundamentals & Game Specification

Status: IN PROGRESS. Exercises 1.1, 1.2 and the quick check are not yet submitted.

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
- **Reel strip:** the fixed, ordered list of symbols on one reel. **Reel stop:** the strip position the reel lands on. Every stop is equally likely.
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
| Outcome | p | payout |
|---|---|---|
| lose | 0.70 | 0 |
| small | 0.29 | 2 |
| jackpot | 0.01 | 38 |

- E[X] = 0.58 + 0.38 = **0.96**, so RTP = 96%.
- E[X²] = 1.16 + 14.44 = 15.60, so Var ≈ 14.68 and σ ≈ **3.83**.
- Hit frequency = **30%**.
- Lesson: the rare jackpot drives the variance, while the frequent small wins drive the hit rate. Two games can share the same RTP and still feel very different.

---

## Exercises (submit answers to Claude for review)

### Quick check
What fraction of the toy game's RTP comes from the jackpot? What does that imply for a player who plays only 50 spins?

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
(Write your work here if you like.)

## Review feedback
(Claude fills this in after reviewing your submission.)
