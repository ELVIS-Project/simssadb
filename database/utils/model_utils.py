"""A collection of functions that are useful for models"""
from psycopg2.extras import NumericRange
from typing import Optional


def clean_range(year_range: Optional[NumericRange]) -> str:
    if year_range:
        if year_range.lower and year_range.upper:
            lower = year_range.lower
            upper = year_range.upper - 1
            if lower == upper:
                return str(lower)
            else:
                return "({0}-{1})".format(str(lower), str(upper))
        else:
            return str(year_range)
    else:
        return ""
