# Ember Forge — Design Brief v0.1 (fictional)

Status: DRAFT. The paytable and strips are a starting point and will be rebalanced on Day 5.

## Grid and bet
- 5 reels × 3 rows. Each reel stops on one of its strip positions uniformly at random, and reels are independent.
- The visible window on each reel is 3 consecutive strip positions (row 0 = stop, rows 1 and 2 = the next positions, wrapping around).
- 10 fixed paylines. 1 credit per line, so **total bet = 10 credits**.
- Pays are in **line-bet multiples** (credits per 1-credit line).

## Symbols
| ID | Name   | Role |
|----|--------|------|
| W  | Wild   | Substitutes for every symbol. Appears only on reels 2–4. Pays nothing on its own. |
| H1 | Crown  | High |
| H2 | Anvil  | High |
| M1 | Hammer | Mid |
| M2 | Tongs  | Mid |
| L1 | Ember  | Low |
| L2 | Ash    | Low |

## Symbol counts per reel (30 stops each)
| Symbol | R1 | R2 | R3 | R4 | R5 |
|--------|----|----|----|----|----|
| W      | 0  | 2  | 2  | 2  | 0  |
| H1     | 2  | 2  | 2  | 2  | 2  |
| H2     | 3  | 3  | 3  | 3  | 3  |
| M1     | 4  | 4  | 4  | 4  | 4  |
| M2     | 5  | 5  | 5  | 5  | 5  |
| L1     | 7  | 6  | 6  | 6  | 7  |
| L2     | 9  | 8  | 8  | 8  | 9  |
| Total  | 30 | 30 | 30 | 30 | 30 |

(The exact strip order comes on Day 3. Counts are enough for single-line probabilities, but order matters for the 3-row window and for multi-line behaviour.)

## Paytable (× line bet)
| Symbol | 3-kind | 4-kind | 5-kind |
|--------|--------|--------|--------|
| H1     | 20     | 100    | 500    |
| H2     | 15     | 60     | 250    |
| M1     | 10     | 40     | 150    |
| M2     | 8      | 25     | 100    |
| L1     | 5      | 15     | 50     |
| L2     | 4      | 10     | 40     |

## Win rules
1. A line win counts consecutive matching symbols starting from reel 1, going left to right. W counts as a match.
2. Reel 1 has no wilds, so the symbol on reel 1 always decides which symbol a line can pay.
3. Each line pays only its longest qualifying run, for example 5-kind and not 5-kind + 3-kind.
4. Wins from different lines are added together.
5. Spin payout = sum of line wins × line bet. **RTP = E[spin payout] / total bet.**

## Paylines (row index per reel, 0 = top)
| # | R1 | R2 | R3 | R4 | R5 |
|---|----|----|----|----|----|
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 0 | 0 | 0 | 0 | 0 |
| 3 | 2 | 2 | 2 | 2 | 2 |
| 4 | 0 | 1 | 2 | 1 | 0 |
| 5 | 2 | 1 | 0 | 1 | 2 |
| 6 | 0 | 0 | 1 | 2 | 2 |
| 7 | 2 | 2 | 1 | 0 | 0 |
| 8 | 1 | 0 | 0 | 0 | 1 |
| 9 | 1 | 2 | 2 | 2 | 1 |
| 10| 0 | 1 | 1 | 1 | 0 |

## Planned extension (Day 6)
Scatter-triggered free spins. Not part of v0.1.
