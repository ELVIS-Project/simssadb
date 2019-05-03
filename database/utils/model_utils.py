"""A collection of functions that are useful for models"""
from typing import Union

from psycopg2._range import DateRange


def clean_date(date_range: DateRange) -> Union[str, bool]:
    """Format a date_range object to a nice string

    Parameters
    ----------
    date_range : postgres.fields.DateRange

    Returns
    -------
    date : str
        A nicely formatted date, either YYYY or YYYY-YYYY
    """
    if date_range is not None:
        try:
            if date_range.lower is not None and date_range.upper is not None:
                if date_range.lower == date_range.upper:
                    date = str(date_range.upper.year)
                else:
                    date = '(' + str(date_range.lower.year) + '-' + str(
                        date_range.upper.year) + ')'
            elif date_range.lower is not None and date_range.upper is None:
                date = str(date_range.lower.year)
            elif date_range.lower is None and date_range.upper is not None:
                date = str(date_range.upper.year)
            else:
                return False
            return date
        except ValueError:
            return False
    return False
