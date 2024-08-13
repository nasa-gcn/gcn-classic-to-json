import numpy as np

from ... import utils

# Will have to rename schema after the location is decided
# trigger number has wierd things that have to be worked out
# energy does not accurately work
# DDDd in tjd, but if the first digits are 0 pad it out


def parse(bin_arr):
    # Define all time and energy range values as a list
    # the index coreesponds to the integer value associated with that time/energy range
    time_options = [
        "undefined/unavailable",
        "1 sec",
        "3 sec",
        "10 sec",
        "30 sec",
        "1 scan",
        "1 orbit",
        "4 orbit",
        "1 day",
    ]
    energy_range_options = ["undefined/unavailable", [2, 4], [4, 10], [10, 20], [2, 10]]
    # Time and energy_range are encoded in the same 4-btye integer
    # Energy is the first byte and time is the energy is the second byte
    t_and_e_data = np.flip(bin_arr[15:16].view(dtype="i1"))
    time_opt, e_opt = t_and_e_data[0], t_and_e_data[1]
    # unit in data is in unit mCrabs; need to be converted into erg/cm^2/sec^-1
    # Conversion factors are from Kawamuro et. al. (2018)
    conversion_factors = [4e-12, 1.24e-11, 1.65e-11, 8.74e-12]
    # Similarly, Latitude is the last 2 bytes and longitude is the first 2 in the same int
    latitude_longitude_data = np.flip(bin_arr[16:17].view(dtype=">i2"))
    lat, lon = latitude_longitude_data[1], latitude_longitude_data[0]
    output = {
        # "$schema" : "",
        "mission": "MAXI",
        # "alert_type" : "initial", # value cannot be calculated with packets
        # "record_number" : 0, # value cannot be calculated with packets
        "id": [int(bin_arr[4])],
        "trigger_time": utils.tjd_to_jd(bin_arr[5], bin_arr[6]),
        "messenger": "EM",
        "flux_energy_range": energy_range_options[e_opt],
        "duration": time_options[time_opt],
        "ra": bin_arr[7] * 1e-4,
        "dec": bin_arr[8] * 1e-4,
        "ra_dec_error": bin_arr[11] * 1e-4,
        "systematic_included": True,
        "latitude": lat * 1e-2,
        "longitude": lon * 1e-2,
    }
    # add energy range if available
    if e_opt != 0:
        # -1 since there is no conversion associated with "undefined/unavailable"
        output["energy_flux"] = bin_arr[9] * 0.1 * conversion_factors[e_opt - 1]

    event_flag_bits = np.flip(np.unpackbits(bin_arr[18:19].view(dtype="u1")))

    comments = ""
    if event_flag_bits[4] == 1:
        comments += "This notice contains negative flux.\n"

    misc_bits = np.flip(np.unpackbits(bin_arr[19:20].view(dtype="u1")))

    if misc_bits[30] == 1:
        comments += "This notice was ground-generated.\n"

    if comments:
        output["additional_info"] = comments

    return output
