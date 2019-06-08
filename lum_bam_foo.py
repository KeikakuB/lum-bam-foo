import click
import random

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

SKILL_PREFIX = "skill_"
ROLLS = ["generic_roll", "dodge_roll", "gfi_roll", "catch_roll", "pass_roll", "pickup_roll"]

ROLLS_TO_SKILL = {
    "generic_roll": None,
    "dodge_roll": "dodge",
    "gfi_roll": "sure_feet",
    "catch_roll": "catch",
    "pass_roll": "pass",
    "pickup_roll": "sure_hands"
}

class BloodBowlDiceSequenceVisitor(NodeVisitor):
    def __init__(self, has_reroll=True):
        self.skills = set()
        self.used_skills = set()
        self.has_reroll = has_reroll
        self.result = True

    def try_use_reroll(self, roll):
        skill = ROLLS_TO_SKILL[roll]
        if skill in self.skills and skill not in self.used_skills:
            self.used_skills.add(skill)
            return True
        if self.has_reroll:
            self.has_reroll = False
            return True
        return False

    def generic_visit(self, node, visited_children):
        if not self.result:
           return False
        if node.expr_name.startswith(SKILL_PREFIX):
            skill = node.expr_name[len(SKILL_PREFIX):]
            self.skills.add(skill)
        if node.expr_name in ROLLS:
            die_roll = node.children[0].text
            needed_value = int(die_roll)
            rng_value = random.randint(1, 6)
            #print(f"Rolling d6, need {needed_value}+")
            if rng_value >= needed_value:
                #print(f"Success: Rolled {rng_value}")
                pass
            else:
                #print(f"Fail: Rolled {rng_value}")
                if self.try_use_reroll(node.expr_name):
                    rng_value = random.randint(1, 6)
                    #print(f"Rolling d6, need {needed_value}+")
                    if rng_value >= needed_value:
                        pass
                    else:
                        self.result = False
                else:
                    self.result = False
        return True

@click.command()
@click.argument('tokens', nargs=-1)
@click.option('-test_count', default=10000)
def cli(tokens, test_count):
    # TODO add MB and PL and DP for blocks/fouls
    # TODO make language more readable / easy to write
    # TODO Allow for mathematical and as well statistical methods for computing the probability of the given expression
    # TODO ensure that impossible sequences (constrained by the game rules) cannot be written out, within reason
    random.seed()
    grammar = Grammar(
        r"""
        expr = sequences
        sequences = sequence (ws? comma ws? sequences)*
        sequence = skills? rolls
        skills = skill+ colon
        rolls = roll+

        foul = lbra ~r"foul\s*" armor_break rbra ws?
        block = lbra block_result+ block_dice (~r"armor\s*" armor_break)? rbra ws?
        armor_break = armor_value ws armor_break_result*
        armor_value_single_digit = ~r"[1-9]"
        armor_value_double_digits = ~r"1[1-2]"
        armor_value = armor_value_double_digits / armor_value_single_digit

        armor_break_result_stun = ~r"stun\s*"
        armor_break_result_ko = ~r"ko\s*"
        armor_break_result_cas = ~r"cas\s*"
        armor_break_result = armor_break_result_stun / armor_break_result_ko / armor_break_result_cas

        block_dice = ~r"-?[1-3]D" ws?

        block_result_pow = ~r"pow\s*"
        block_result_pow_push = ~r"pp\s*"
        block_result_push = ~r"push\s*"
        block_result_both_down = ~r"bd\s*"
        block_result_skull = ~r"skull\s*"

        block_result = block_result_pow / block_result_pow_push / block_result_push / block_result_both_down / block_result_skull

        die_roll = ~r"[2-6]"
        generic_roll = die_roll ~r"\s*"
        dodge_roll = die_roll ~r"do?d?g?e?\s*"
        gfi_roll = die_roll ~r"(gf?i?|go?f?o?r?i?t?)\s*"
        catch_roll = die_roll ~r"ca?t?c?h?\s*"
        pass_roll = die_roll ~r"pas?s?\s*"
        pickup_roll = die_roll ~r"pic?k?u?p?\s*"
        roll = dodge_roll / gfi_roll / catch_roll / pass_roll / pickup_roll / generic_roll / block / foul

        skill_dodge = ~r"do?d?g?e?\s*"
        skill_sure_hands = ~r"(sh|sure ha?n?d?s?)\s*"
        skill_sure_feet = ~r"(sf|sure fe?e?t?)\s*"
        skill_pass = ~r"pas?s?\s*"
        skill_catch = ~r"ca?t?c?h?\s*"
        skill_pro = ~r"pro?\s*"

        skill = skill_dodge / skill_sure_hands / skill_sure_feet / skill_pass / skill_catch / skill_pro

        ws = ~r"\s*"
        colon = ":"
        comma = ","
        lpar = "("
        rpar = ")"
        lbra = "["
        rbra = "]"
    """)
    tree = grammar.parse(" ".join(tokens))
    # print(tree)

    print(f"Running {test_count} tests on {tokens}")
    print_results(tree, test_count, False)
    print_results(tree, test_count, True)

def print_results(tree, test_count, has_reroll):
    n_successes = 0
    n_fails = 0
    for i in range(test_count):
        iv = BloodBowlDiceSequenceVisitor(has_reroll)
        if iv.visit(tree):
            n_successes += 1
        else:
            n_fails += 1
    if has_reroll:
        msg = "with team reroll"
    else:
        msg = "without team reroll"
    n_total = n_successes + n_fails
    success_percentage = n_successes / n_total
    print(f"Success Percentage {msg}: {success_percentage}%")
