"""A collection of functions that are useful for models"""
from psycopg2.extras import NumericRange
from typing import Optional


def range_to_str(year_range: Optional[NumericRange]) -> str:
    """Converts a Numeric Range to a front-end friendly string
    
    Parameters
    ----------
    year_range : Optional[NumericRange]
        The numeric range
    
    Returns
    -------
    str
        The front-end friendly string
    """
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

def clean_year_range(year_range: NumericRange) -> NumericRange:
    """Ensures that a Numeric Range has both bounds filled properly
    
    Parameters
    ----------
    year_range : NumericRange
        A numeric range that might not have both bounds correct
    
    Returns
    -------
    NumericRange
        A numeric range with both bounds corrected
    """
    if year_range.lower is None and year_range.upper is not None:
        new_range = NumericRange(year_range.upper, year_range.upper + 1, bounds="[)")
        return new_range

    elif year_range.lower is not None and year_range.upper is None:
        new_range = NumericRange(year_range.lower, year_range.lower + 1, bounds="[)")
        return new_range
    
    else:
        return year_range
