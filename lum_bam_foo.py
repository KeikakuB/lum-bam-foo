import click
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

class BloodBowlDiceSequenceVisitor(NodeVisitor):
    def visit_expr(self, node, visited_children):
        """ Returns the overall output. """
        output = {}
        for child in visited_children:
            output.update(child[0])
        return output

    def visit_entry(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        key, values = visited_children
        return {key: dict(values)}

    def visit_section(self, node, visited_children):
        """ Gets the section name. """
        _, section, *_ = visited_children
        return section.text

    def visit_pair(self, node, visited_children):
        """ Gets each key/value pair, returns a tuple. """
        key, _, value, *_ = node.children
        return key.text, value.text

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node

@click.command()
@click.argument('tokens', nargs=-1)
def cli(tokens):
    # TODO add MB and PL and DP for blocks/fouls
    # TODO make language more readable / easy to write
    # TODO Allow for mathematical and as well statistical methods for computing the probability of the given expression
    grammar = Grammar(
    r"""
    EXPR = SEQUENCES
    SEQUENCES = SEQUENCE (ws? comma ws? SEQUENCES)*
    SEQUENCE = SKILLS? ROLLS
    SKILLS = SKILL+ colon
    ROLLS = ROLL+

    FOUL = lbra ~r"foul\s*" ARMOR_BREAK rbra ws?
    BLOCK = lbra BLOCK_RESULT+ BLOCK_DICE (~r"armor\s*" ARMOR_BREAK)? rbra ws?
    ARMOR_BREAK = ARMOR_VALUE ws ARMOR_BREAK_RESULT*
    ARMOR_VALUE_SINGLE_DIGIT = ~r"[1-9]"
    ARMOR_VALUE_DOUBLE_DIGITS = ~r"1[1-2]"
    ARMOR_VALUE = ARMOR_VALUE_DOUBLE_DIGITS / ARMOR_VALUE_SINGLE_DIGIT

    ARMOR_BREAK_RESULT_STUN = ~r"stun\s*"
    ARMOR_BREAK_RESULT_KO = ~r"ko\s*"
    ARMOR_BREAK_RESULT_CAS = ~r"cas\s*"
    ARMOR_BREAK_RESULT = ARMOR_BREAK_RESULT_STUN / ARMOR_BREAK_RESULT_KO / ARMOR_BREAK_RESULT_CAS

    BLOCK_DICE = ~r"-?[1-3]" ws?

    BLOCK_RESULT_POW = ~r"pow\s*"
    BLOCK_RESULT_POW_PUSH = ~r"pp\s*"
    BLOCK_RESULT_PUSH = ~r"push\s*"
    BLOCK_RESULT_BOTH_DOWN = ~r"bd\s*"
    BLOCK_RESULT_SKULL = ~r"skull\s*"

    BLOCK_RESULT = BLOCK_RESULT_POW / BLOCK_RESULT_POW_PUSH / BLOCK_RESULT_PUSH / BLOCK_RESULT_BOTH_DOWN / BLOCK_RESULT_SKULL

    DIE_ROLL = ~r"[2-6]"
    GENERIC_ROLL = DIE_ROLL ~r"\s*"
    DODGE_ROLL = DIE_ROLL ~r"do?d?g?e?\s*"
    GFI_ROLL = DIE_ROLL ~r"(gf?i?|go?f?o?r?i?t?)\s*"
    CATCH_ROLL = DIE_ROLL ~r"ca?t?c?h?\s*"
    PASS_ROLL = DIE_ROLL ~r"pas?s?\s*"
    PICKUP_ROLL = DIE_ROLL ~r"pic?k?u?p?\s*"
    ROLL = DODGE_ROLL / GFI_ROLL / CATCH_ROLL / PASS_ROLL / PICKUP_ROLL / GENERIC_ROLL / BLOCK / FOUL

    SKILL_DODGE = ~r"do?d?g?e?\s*"
    SKILL_SURE_HANDS = ~r"(sh|sure ha?n?d?s?)\s*"
    SKILL_SURE_FEET = ~r"(sf|sure fe?e?t?)\s*"
    SKILL_PASS = ~r"pas?s?\s*"
    SKILL_CATCH = ~r"ca?t?c?h?\s*"
    SKILL_PRO = ~r"pro?\s*"

    SKILL = SKILL_DODGE / SKILL_SURE_HANDS / SKILL_SURE_FEET / SKILL_PASS / SKILL_CATCH / SKILL_PRO

    ws = ~r"\s*"
    colon = ":"
    comma = ","
    lpar = "("
    rpar = ")"
    lbra = "["
    rbra = "]"
    """)
    tree = grammar.parse(" ".join(tokens))
    print(tree)

    # iv = BloodBowlDiceSequenceVisitor()
    # output = iv.visit(tree)
    # print(output)
