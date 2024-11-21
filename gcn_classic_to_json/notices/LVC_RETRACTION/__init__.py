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


def parse(bin):
    bin[7:13]  # Spare. According to Docs:'24 bytes for the future'
    bin[14:18]  # Spare. According to Docs:'16 bytes for the future'
    bin[20:29]  # Spare. According to Docs:'36 bytes for the future'

    trig_id_bits = np.flip(np.unpackbits(bin[18:19].view(dtype="u1")))

    misc_bits = np.flip(np.unpackbits(bin[19:20].view(dtype="u1")))

    first_suffix = chr(np.packbits(np.flip(misc_bits[10:18]))[0])
    prefix = prefix_letters[
        np.packbits(np.pad(np.flip(misc_bits[20:24]), (4, 0)))[0] - 1
    ]
    seq_num = np.packbits(np.flip(misc_bits[24:32]))[0]

    letter_bytes = np.flip(bin[21:22].view(dtype="u1"))
    second_suffix = chr(np.packbits(letter_bytes[0])[0])

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

    return {
        "mission": "LVC",
        "alert_tense": "test" if trig_id_bits[1] else "current",
        "messenger": "GW",
        "alert_type": "retraction",
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6] + (bin[13] * 1e-4)),
        "id": [(prefix + str(bin[4]) + first_suffix + second_suffix).strip("\u0000")],
        "record_number": seq_num,
        "skymap_url": f"https://gracedb.ligo.org/superevents/{utils.binary_to_string(bin[29:39])}",
        "additional_info": comments if comments else None,
    }
