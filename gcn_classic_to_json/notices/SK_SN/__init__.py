import numpy as np

from ... import utils

# Will have to rename schema after the location is decided
# Distance is given in a range instead of a value, need to store it as Mpc, it's in kpc in file
# energy limit is only minumum; energy has to be in kev, it's in Mev in the file
# There is a duration in notices but not in the packets


def parse(bin_arr):
    output = {
        "$schema": "",
        "mission": "Super-Kamiokande",
        "alert_type": "initial",
        "messenger": "Neutrino",
        "id": [int(bin_arr[4])],
        "trigger_time": utils.tjd_to_jd(bin_arr[5], bin_arr[6]),
        "ra": bin_arr[7] * 1e-4,
        "dec": bin_arr[8] * 1e-4,
        "ra_dec_error": bin_arr[16] * 1e-4,
        "containment_probability": 0.95,
        # new event
        "n_events": int(bin_arr[9]),
        "distance_range": [bin_arr[13] * 1e-3, bin_arr[14] * 1e-3],
    }

    trig_id_bits = np.flip(np.unpackbits(bin_arr[18:19].view(dtype="u1")))

    # check if the notice is real or test
    if trig_id_bits[1] == 1:
        output["alert_tense"] = "test"
        output["additional_info"] = "This is a test notice.\n"
    else:
        output["additional_info"] = "This is a real event.\n"

    return output
