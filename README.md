# lum-bam-foo
CLI to calculate probabilities of performing specific sequences of actions in Blood Bowl.

# Examples
`lum_bam_foo "4"` -> perform a 4+ (without a team reroll).

`lum_bam_foo "rr, 4d 2g 2g"` -> perform a 4+ dodge and 2 2+ go for its (with a team reroll).

`lum_bam_foo "d: 4d 3d"` -> with dodge perfom a 4+ dodge and a 3+ dodge (without a team reroll).

`lum_bam_foo "sf: 2g 2g, d: 2d 3d"` ->  with sure feet perform 2 2+ go for its then with dodge perform a 2+ dodge and a 3+ dodge (without a team reroll).

`lum_bam_foo "rr, loner pro: 4d [pow pp 2D av 7 ko cas]"` -> with loner and pro perform a 4+ dodge and a 2 dice block, get a pow or a pow/push then break armor value 7 then get a KO or a CAS result on the injury roll (with a team reroll).

`lum_bam_foo "[foul av 7 ko cas]"` -> Foul a player with armor value 7 and get a KO or CAS result on the injury roll.

# Grammar
``` python
expr = (team_reroll ws? comma ws?)? sequences
sequences = sequence (ws? comma ws? sequences)*
sequence = skills? rolls
skills = skill+ colon ws?
rolls = roll+

team_reroll = ~r"(rr|re?r?o?l?l?)\s*"

die_roll = ~r"[2-6]"
generic_roll = die_roll ~r"\s*"
dodge_roll = die_roll ~r"do?d?g?e?\s*"
gfi_roll = die_roll ~r"(gf?i?|go?f?o?r?i?t?)\s*"
catch_roll = die_roll ~r"ca?t?c?h?\s*"
pass_roll = die_roll ~r"pas?s?\s*"
pickup_roll = die_roll ~r"pic?k?u?p?\s*"
roll = dodge_roll / gfi_roll / catch_roll / pass_roll / pickup_roll / generic_roll / block / foul

foul = lbra ~r"foul\s*" (~r"av\s*" armor_break)? ws? rbra ws?
block = lbra block_results block_dice (~r"av\s*" armor_break)? ws? rbra ws?
armor_break = armor_value ws? armor_break_results
armor_value_single_digit = ~r"[1-9]"
armor_value_double_digits = ~r"1[0-2]"
armor_value = armor_value_double_digits / armor_value_single_digit

armor_break_results = armor_break_result*
armor_break_result_stun = ~r"stun\s*"
armor_break_result_ko = ~r"ko\s*"
armor_break_result_cas = ~r"cas\s*"
armor_break_result = armor_break_result_stun / armor_break_result_ko / armor_break_result_cas

block_dice = ~r"(-[2-3]|[1-3])D" ws?

block_results = block_result+
block_result_pow = ~r"pow\s*"
block_result_pow_push = ~r"pp\s*"
block_result_push = ~r"push\s*"
block_result_both_down = ~r"bd\s*"
block_result_skull = ~r"skull\s*"

block_result = block_result_pow / block_result_pow_push / block_result_push / block_result_both_down / block_result_skull

skill_dodge = ~r"do?d?g?e?\s*"
skill_sure_hands = ~r"(sh|sure ha?n?d?s?)\s*"
skill_sure_feet = ~r"(sf|sure fe?e?t?)\s*"
skill_pass = ~r"pas?s?\s*"
skill_catch = ~r"ca?t?c?h?\s*"
skill_pro = ~r"pro?\s*"
skill_loner = ~r"lo?n?e?r?\s*"

skill = skill_dodge / skill_sure_hands / skill_sure_feet / skill_pass / skill_catch / skill_pro / skill_loner

ws = ~r"\s*"
colon = ":"
comma = ","
lpar = "("
rpar = ")"
lbra = "["
rbra = "]"
```

# TODO
- Add MB and DP skill implementations for blocks/fouls.
- Allow for mathematical and as well statistical methods for computing the probability of the given expression.
- Ensure that impossible sequences (constrained by the game rules) cannot be written out, within reason.
