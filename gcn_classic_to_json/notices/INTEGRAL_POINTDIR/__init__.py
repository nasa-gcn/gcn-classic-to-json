import numpy as np

from ... import utils


def parse(bin):
    bin[7:12]  # Unused. According to Docs: "20 bytes for the future"
    bin[13]  # Unused. According to Docs: "4 bytes for the future"
    bin[16:19]  # Unused. According to Docs: "12 bytes for the future"
    bin[19]  # Intentionally Omitted. According to Docs: "format are still TBD"
    bin[20:39]  # Unused. According to Docs: "76 bytes for the future"

    id_data = bin[4:5].view(dtype="u2")
    test_bits = np.flip(np.unpackbits(bin[12:13].view(dtype="u1")))

    return {
        "id": [id_data[0]],
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6]),
        "alert_tense": "test" if test_bits[31] else "current",
        "next_sc_ra": bin[14] * 1e-4,
        "next_sc_dec": bin[15] * 1e-4,
    }
