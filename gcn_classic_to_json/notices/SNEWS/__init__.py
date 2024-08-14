import numpy as np

from ... import utils

misc_descriptions = {
    0: "Super-K contributed to this notice.",
    1: "Super-K quality factor is possible.",
    2: "Super-K quality factor is good.",
    3: "Super-K quality factor is override.",
    4: "LVD contributed to this notice.",
    5: "LVD quality factor is possible.",
    6: "LVD quality factor is good.",
    7: "LVD quality factor is override.",
    8: "IceCube contributed to this notice.",
    9: "IceCube quality factor is possible.",
    10: "IceCube quality factor is good.",
    11: "IceCube quality factor is override.",
    12: "KamLAND contributed to this notice.",
    13: "KamLAND quality factor is possible.",
    14: "KamLAND quality factor is good.",
    15: "KamLAND quality factor is override.",
    16: "Borexino contributed to this notice.",
    17: "Borexino quality factor is possible.",
    18: "Borexino quality factor is good.",
    19: "Borexino quality factor is override.",
    20: "Daya Bay contributed to this notice.",
    21: "Daya Bay quality factor is possible.",
    22: "Daya Bay quality factor is good.",
    23: "Daya Bay quality factor is override.",
    24: "HALO contributed to this notice.",
    25: "HALO quality factor is possible.",
    26: "HALO quality factor is good.",
    27: "HALO quality factor is override.",
}


def parse(bin):
    bin[10]  # Spare. According to Docs: '4 bytes for the future'
    bin[14:18]  # Spare. According to Docs: '16 bytes for the future'
    bin[20:39]  # Spare. According to Docs: '76 bytes for the future'

    trig_id_bits = np.flip(np.unpackbits(bin[18:19].view(dtype="u1")))

    comments = ""
    comments += (
        "This is an Individual detection.\n"
        if trig_id_bits[0] == 1
        else "This is an Coincidence detection.\n"
    )
    comments += (
        "This is a test notice.\n"
        if trig_id_bits[1] == 1
        else "This is a real notice.\n"
    )
    comments += (
        "RA/Dec is undefined.\n" if trig_id_bits[2] == 1 else "RA/Dec is defined.\n"
    )
    if trig_id_bits[5] == 1:
        comments += "This is definitely not a core-collapse Supernova."

    misc_bits = np.flip(np.unpackbits(bin[19:20].view(dtype="u1")))

    comments += "\n".join(
        [val for (key, val) in misc_descriptions.items() if misc_bits[key]]
    )

    return {
        "alert_type": "initial",
        "alert_tense": "test" if trig_id_bits[1] else "current",
        "messenger": "Neutrino",
        "id": [bin[4]],
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6]),
        "ra": bin[7] * 1e-4,
        "dec": bin[8] * 1e-4,
        "ra_dec_error": bin[11] * 1e-4,
        "containment_probability": bin[12] * 1e-2,
        "n_events": bin[9],
        "duration": bin[13] * 1e-2,
        "additional_info": comments if comments else None,
    }
