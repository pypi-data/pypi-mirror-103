
from .predicates import Context
from .operations import BOOLEANS, MATH, COMPARISONS


common = Context()

common.bulk_register(COMPARISONS)
common.bulk_register(MATH)
common.bulk_register(BOOLEANS)
