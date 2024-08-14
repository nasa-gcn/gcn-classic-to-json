import numpy as np

from ... import utils


def parse(bin_arr):
    output = {
        "$schema": "",
        "alert_type": "initial",
        "messenger": "Neutrino",
        "id": [int(bin_arr[4])],
        "trigger_time": utils.tjd_to_jd(bin_arr[5], bin_arr[6]),
        # "rate_snr" : time_and_energy_data,
        # "net_count_rate" : int(bin[9]),
        # "duration" : float(bin_arr[]),
        "ra": bin_arr[7] * 1e-4,
        "dec": bin_arr[8] * 1e-4,
        "ra_dec_error": bin_arr[11] * 1e-4,
        "containment_probability": bin_arr[12] * 1e-2,
        # new event
        "n_events": int(bin_arr[9]),
        "duration": bin_arr[13] * 1e-2,
    }

    trig_id_bits = np.flip(np.unpackbits(bin_arr[18:19].view(dtype="u1")))

    comments = ""
    if trig_id_bits[0] == 1:
        comments += "This is an Individual detection.\n"
    else:
        comments += "This is an Coincidence detection.\n"

    if trig_id_bits[1] == 1:
        comments += "This is a test notice.\n"
    else:
        comments += "This is a real notice.\n"

    if trig_id_bits[2] == 1:
        comments += "RA/Dec is undefined.\n"
    else:
        comments += "RA/Dec is defined.\n"

    if trig_id_bits[5] == 1:
        comments += "This is definitely not a core-collapse Supernova.\n"

    misc_bits = np.flip(np.unpackbits(bin_arr[19:20].view(dtype="u1")))

    misc_descriptions = {
        0: "Super-K contributed to this notice.\n",
        1: "Super-K quality factor is possible.\n",
        2: "Super-K quality factor is good.\n",
        3: "Super-K quality factor is override.\n",
        4: "LVD contributed to this notice.\n",
        5: "LVD quality factor is possible.\n",
        6: "LVD quality factor is good.\n",
        7: "LVD quality factor is override.\n",
        8: "IceCube contributed to this notice.\n",
        9: "IceCube quality factor is possible.\n",
        10: "IceCube quality factor is good.\n",
        11: "IceCube quality factor is override.\n",
        12: "KamLAND contributed to this notice.\n",
        13: "KamLAND quality factor is possible.\n",
        14: "KamLAND quality factor is good.\n",
        15: "KamLAND quality factor is override.\n",
        16: "Borexino contributed to this notice.\n",
        17: "Borexino quality factor is possible.\n",
        18: "Borexino quality factor is good.\n",
        19: "Borexino quality factor is override.\n",
        20: "Daya Bay contributed to this notice.\n",
        21: "Daya Bay quality factor is possible.\n",
        22: "Daya Bay quality factor is good.\n",
        23: "Daya Bay quality factor is override.\n",
        24: "HALO contributed to this notice.\n",
        25: "HALO quality factor is possible.\n",
        26: "HALO quality factor is good.\n",
        27: "HALO quality factor is override.\n",
    }

    comments += "".join(
        [val for (key, val) in misc_descriptions.items() if misc_bits[key] == 1]
    )

    output["additional_info"] = comments

    return output
