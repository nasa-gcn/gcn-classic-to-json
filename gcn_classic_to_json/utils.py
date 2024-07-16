from astropy.time import Time
import numpy as np


def datetime_to_iso8601(date, time):
    """Converts time to ISO 8601 format.

    The function convert datetime into the ISO 8601 format from
    Truncated Julian Date by first converting it to Julian Date.

    Parameters
    ----------
    date : int
        Date must be in Truncated Julian Date format.
    time : int
        Time of day must in Seconds of Day format.

    Returns
    -------
    string
        returns datetime in ISO8601 format.

    Notes
    -----
    The zero point for Truncated Julian Day is given in https://en.wikipedia.org/wiki/Julian_day.
    """
    TJD0 = (2440000, 0.5)
    return Time(date + TJD0[0], time / 8640000 + TJD0[1], format="jd").isot + "Z"
