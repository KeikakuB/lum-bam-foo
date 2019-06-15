from lum_bam_foo import BloodBowlProbabilityComputer

import math
import fractions

relative_tolerance = 0.01
comp = BloodBowlProbabilityComputer(25000, 123917280)


def check(tokens, failure_numerator, failure_denominator):
    success_probability_fraction = fractions.Fraction(
        failure_denominator - failure_numerator, failure_denominator)
    assert math.isclose(comp.get_probability(tokens),
                        success_probability_fraction,
                        rel_tol=relative_tolerance)


def test_first():
    check("2", 1, 6)
    check("3", 2, 6)
    check("4", 3, 6)
    check("5", 4, 6)
    check("6", 5, 6)

    check("rr,2", 1, 36)
    check("rr,3", 1, 9)
    check("rr,4", 1, 4)
    check("rr,5", 4, 9)
    check("rr,6", 25, 36)

    check("[pow pp 1D]", 2, 3)
    check("[pow pp push 1D]", 1, 3)
    check("[pow 1D]", 5, 6)
