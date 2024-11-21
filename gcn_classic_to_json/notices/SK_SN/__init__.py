import numpy as np

from ... import utils


def parse(bin):
    bin[10]  # Unused. According to Docs:'4 bytes for the future'.
    bin[12]  # Unused. According to Docs:'4 bytes for the future'.
    bin[17]  # Unused. According to Docs:'4 bytes for the future'.
    bin[
        19
    ]  # Intentionally Omitted. Defined as miscellaneous bits, but does not have any information.
    bin[22:39]  # Unused. According to Docs:'68 bytes for the future'.

    trig_id_bits = np.flip(np.unpackbits(bin[18:19].view(dtype="u1")))

    return {
        "mission": "Super-Kamiokande",
        "alert_type": "initial",
        "alert_tense": "test" if trig_id_bits[1] else "current",
        "messenger": "Neutrino",
        "id": [bin[4]],
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6]),
        "ra": bin[7] * 1e-4,
        "dec": bin[8] * 1e-4,
        "ra_dec_error": bin[15] * 1e-4,
        "ra_dec_error_68": bin[11] * 1e-4,
        "ra_dec_error_95": bin[16] * 1e-4,
        "n_events": bin[9],
        "collection_duration": bin[21] * 1e-4,
        "energy_limit": bin[20] * 1e-1,
        "distance_range": [bin[13] * 1e-5, bin[14] * 1e-5],
    }
