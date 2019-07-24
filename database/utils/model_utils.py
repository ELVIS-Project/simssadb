"""A collection of functions that are useful for models"""
from psycopg2.extras import NumericRange


def clean_range(year_range: NumericRange) -> str:
    if year_range:
        if year_range.lower is not None and year_range.upper is not None:
            if year_range.lower == year_range.upper:
                return str(year_range.lower)
            else:
                return "(" + str(year_range.lower) + "-" + str(year_range.upper) + ")"
        elif year_range.upper is None and year_range.lower is not None:
            return str(year_range.lower)
        elif year_range.lower is None and year_range.upper is not None:
            return str(year_range.upper)
        else:
            return ""
    else:
        return ""
