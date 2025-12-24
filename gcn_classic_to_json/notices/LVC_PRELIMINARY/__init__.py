import numpy as np

from ... import utils

pipeline_opts = [
    "undefined/illegal",
    "MTBAOnline",
    "CWB",
    "CWB2G",
    "GSTLAL",
    "GSTLAL_Spiir",
    "Hardware Injection",
    "X",
    "Q",
    "Omega",
    "Ringdown",
    "LIB",
    "Fermi",
    "Swift",
    "SNEWS",
    "pycbc",
]

search_opts = [
    "undefined/illegal",
    "AllSky",
    "LowMass",
    "HighMass",
    "GRB",
    "Supernova",
    "MockDataChallenge",
    "AllSkyLong",
    "BBH",
]

group_opts = ["undefined/illegal", "CBC", "Burst", "Test"]

trig_id_description = {
    1: "This is a test Notice.\n",
    2: "This is a hardware injection event.\n",
    3: "This event has been vetted by a human.\n",
    4: "This event is an Open Alert.\n",
    5: "This is definitely a retraction.\n",
    29: "There was a temporal coincidence with another event.\n",
}

misc_descriptions = {
    0: "LIGO-Handford Observatory contributed to this candidate event.\n",
    1: "LIGO-Livingston Observatory contributed to this candidate event.\n",
    2: "Virgo Observatory contributed to this candidate event.\n",
    3: "GEO600 Observatory contributed to this candidate event.\n",
    4: "KAGRA Observatory contributed to this candidate event.\n",
    5: "LIGO-India Observaiory contributed to this candidate event.\n",
}

prefix_letters = [
    "G",
    "T",
    "M",
    "Y",
    "H",
    "E",
    "K",
    "S",
    "GW",
    "TS",
    "TGW",
    "MS",
    "MGW",
]

invalid_prob_descriptions = {
    0: "Probability of NS is invalid.\n",
    1: "Probability of REMNANT is invalid.\n",
    2: "Probability of BNS is invalid.\n",
    3: "Probability of NSBH is invalid.\n",
    4: "Probability of BBH is invalid.\n",
    5: "Probability of Mass Gap is invalid.\n",
    6: "Probability of TERRESTRIAL is invalid.\n",
}


def parse(bin):
    bin[7:9]  # Intentionally Omitted. RA/Dec is set to zero due to large localization.
    bin[15:18]  # Spare. According to Docs: '12 bytes for the future'
    bin[20]  # Unused. According to Docs: Not present in preliminary notice type.
    bin[24:29]  # Spare. According to Docs: '20 bytes for the future'

    event_type_bytes = np.flip(bin[12:13].view(dtype="u1"))
    pipeline_num, search_num, group_num, _ = event_type_bytes

    fluence = 10 ** (bin[9] * 1e-4) * 1e3
    peak_freq = bin[10] * 1e-2
    duration = bin[14] * 1e-2

    trig_id_bits = np.flip(np.unpackbits(bin[18:19].view(dtype="u1")))

    misc_bits = np.flip(np.unpackbits(bin[19:20].view(dtype="u1")))

    first_suffix = chr(np.packbits(np.flip(misc_bits[10:18]))[0])
    prefix = prefix_letters[
        np.packbits(np.pad(np.flip(misc_bits[20:24]), (4, 0)))[0] - 1
    ]
    seq_num = np.packbits(np.flip(misc_bits[24:32]))[0]

    mass_gap_and_letters_bytes = np.flip(bin[21:22].view(dtype="u1"))
    second_suffix = chr(np.packbits(mass_gap_and_letters_bytes[0])[0])
    prob_mass_gap = mass_gap_and_letters_bytes[3] * 1e-2

    class_prob_bytes = bin[22:23].view(dtype="u1")
    prob_bns, prob_nsbh, prob_bbh, prob_terrestrial = class_prob_bytes * 1e-2

    prob_invalid_flags_bits = np.flip(np.unpackbits(bin[23:24].view(dtype="u1")))

    comments = ""
    comments += "".join(
        [val for (key, val) in trig_id_description.items() if trig_id_bits[key]]
    )
    comments += "".join(
        [val for (key, val) in misc_descriptions.items() if misc_bits[key]]
    )
    comments += (
        "This Notice was ground-generated.\n"
        if misc_bits[19]
        else "This Notice was flight-generated.\n"
    )
    comments += "".join(
        [
            val
            for (key, val) in invalid_prob_descriptions.items()
            if prob_invalid_flags_bits[key]
        ]
    )

    return {
        "mission": "LVC",
        "alert_tense": "test" if trig_id_bits[1] else "current",
        "messenger": "GW",
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6] + (bin[13] * 1e-4)),
        "id": [(prefix + str(bin[4]) + first_suffix + second_suffix).strip("\u0000")],
        "record_number": seq_num,
        "fluence": fluence if group_num == 2 else None,
        "peak_frequency": peak_freq if group_num == 2 else None,
        "far": 10 ** (bin[11] * 1e-4),
        "pipeline_type": pipeline_opts[pipeline_num],
        "search_type": search_opts[search_num],
        "group_type": group_opts[group_num],
        "duration": duration if group_num == 2 else None,
        "p_astro": 1 - prob_terrestrial,
        "classification": (
            {"TERRESTRIAL": prob_terrestrial},
            {"BBH": prob_bbh},
            {"BNS": prob_bns},
            {"NSBH": prob_nsbh},
        ),
        "properties": ({"Mass Gap": prob_mass_gap},),
        "skymap_url": f"https://gracedb.ligo.org/superevents/{utils.binary_to_string(bin[29:39])}",
        "additional_info": comments if comments else None,
    }
