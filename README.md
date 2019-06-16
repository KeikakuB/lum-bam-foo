# lum-bam-foo
CLI to calculate probabilities of performing specific sequences of actions in Blood Bowl.

# Examples
`4` -> perform a 4+ (without a team reroll).

`rr, 4d 2g 2g` -> perform a 4+ dodge and 2 2+ go for its (with a team reroll).

`d: 4d 3d` -> with dodge perfom a 4+ dodge and a 3+ dodge (without a team reroll).

`sf: 2g 2g, d: 2d 3d` ->  with sure feet perform 2 2+ go for its then with dodge perform a 2+ dodge and a 3+ dodge (without a team reroll).

`rr, loner pro: 4d [pow pp 2D av 7 ko cas]` -> with loner and pro perform a 4+ dodge and a 2 dice block, get a pow or a pow/push then break armor value 7 then get a KO or a CAS result on the injury roll (with a team reroll).

`[foul av 7 ko cas]` -> Foul a player with armor value 7 and get a KO or CAS result on the injury roll.

# TODO
- Add MB and DP skill implementations for blocks/fouls.
- Allow for mathematical and as well statistical methods for computing the probability of the given expression.
- Ensure that impossible sequences (constrained by the game rules) cannot be written out, within reason.
