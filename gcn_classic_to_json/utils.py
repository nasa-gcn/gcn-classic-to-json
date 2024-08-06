import numpy as np
from astropy.time import Time


def datetime_to_iso8601(date, time):
    """Converts time to ISO 8601 format.

    The function converts input into the ISO 8601 format from
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


def binary_to_string(binary):
    """Converts a binary array to a ASCII-string.

    The function converts each field encoded as a 4-byte integer into
    four 1-byte integers and then to their corresponding ASCII value.

    Parameters
    ----------
    binary : array-like
        A array for binary values encoded as 4-byte integers.

    Returns
    -------
    string:
        returns the corresponding ASCII string.

    Notes:
    ------
    The strings in the binary packets seem to encoded little-endian.
    """
    bits_array = np.asarray(binary, dtype="<i4").view(dtype="u1")
    str_list = [chr(bits) for bits in bits_array]
    string = "".join(str_list)
    excess_char = string.count("\u0000")
    return string.replace("\u0000", "", excess_char)
