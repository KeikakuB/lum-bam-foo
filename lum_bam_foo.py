import random
import logging

import click

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

FORMAT = '%(levelname)-8s:%(funcName)-20s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('lum_bam_foo')

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
    def __init__(self):
        self.skills = set()
        self.used_skills = set()
        self.has_team_reroll = False
        self.used_team_reroll = False
        self.started_rolling = False
        self.result = True

    def try_use_reroll(self, roll):
        skill = ROLLS_TO_SKILL[roll]
        if skill in self.skills and skill not in self.used_skills:
            logger.debug(f"\tUsing {skill} reroll")
            self.used_skills.add(skill)
            return True

        if self.has_team_reroll and not self.used_team_reroll:
            logger.debug("\tUsing team reroll")
            self.used_team_reroll = True
            if "loner" in self.skills:
                if random.randint(1, 2) is 1:
                    logger.debug("\tLoner roll suceeded")
                    return True
                else:
                    logger.debug("\tWasted team reroll due to loner")
                    return False
            return True

        if "pro" in self.skills and "pro" not in self.used_skills:
            self.used_skills.add("pro")
            if random.randint(1, 2) is 1:
                logger.debug("\tUsing pro reroll")
                return True
            else:
                logger.debug("\tFailed to use pro reroll")
                return False
        return False

    def generic_visit(self, node, visited_children):
        if not self.result:
            return False
        if node.expr_name == "team_reroll":
            self.has_team_reroll = True
            logger.debug(f"Has team reroll")
        if node.expr_name == "sequence" and self.started_rolling:
            # This is a new player, so reset the skills
            logger.debug("Resetting Player skills")
            self.started_rolling = False
            self.skills = set()
            self.used_skills = set()
        if node.expr_name.startswith(SKILL_PREFIX):
            skill = node.expr_name[len(SKILL_PREFIX):]
            logger.debug(f"Adding player skill: {skill}")
            self.skills.add(skill)
        if node.expr_name in ROLLS:
            self.started_rolling = True
            die_roll = node.children[0].text
            needed_value = int(die_roll)
            logger.debug(f"{node.expr_name}: {node.text}")
            logger.debug(f"\tRolling d6, need {needed_value}+")
            rng_value = random.randint(1, 6)
            if rng_value < needed_value:
                logger.debug(f"\tFail: Rolled {rng_value}")
                if self.try_use_reroll(node.expr_name):
                    logger.debug(f"\tRerolling d6, need {needed_value}+")
                    rng_value = random.randint(1, 6)
                    if rng_value < needed_value:
                        logger.debug(f"\tFail: Rerolled {rng_value}")
                        self.result = False
                    else:
                        logger.debug(f"\tSuccess: Rerolled {rng_value}")
                else:
                    self.result = False
            else:
                logger.debug(f"\tSuccess: Rolled {rng_value}")
        return True

class BloodBowlProbabilityComputer:
    def __init__(self, test_count, seed=None):
        self.test_count = test_count
        self.seed = seed

        self.grammar = Grammar(
            r"""
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
        """)

    def get_probability(self, tokens):
        if self.seed == None:
            random.seed()
        else:
            random.seed(self.seed)
        tree = self.grammar.parse(tokens)
        logger.info(f"Running {self.test_count} tests on {tokens}")
        n_successes = 0
        n_fails = 0
        for i in range(self.test_count):
            logger.debug(f"Running test: {i}")
            iv = BloodBowlDiceSequenceVisitor()
            if iv.visit(tree):
                n_successes += 1
            else:
                n_fails += 1

        if iv.has_team_reroll:
            msg = "with team reroll"
        else:
            msg = "without team reroll"
        n_total = n_successes + n_fails
        success_probability = n_successes / n_total
        logger.info(f"Success Probability {msg}")
        return success_probability

@click.command()
@click.argument('tokens')
@click.option('-t', '--test_count', default=10000)
@click.option('-v', '--verbose', is_flag=True)
def cli(tokens, test_count, verbose):
    # TODO add MB and PL and DP for blocks/fouls
    # TODO make language more readable / easy to write
    # TODO Allow for mathematical and as well statistical methods for computing the probability of the given expression
    # TODO ensure that impossible sequences (constrained by the game rules) cannot be written out, within reason
    if verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(f"'{tokens}'")
    comp = BloodBowlProbabilityComputer(test_count)
    success_probability = comp.get_probability(tokens)
    print(success_probability)
