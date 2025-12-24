import numpy as np

from ... import utils


def parse(bin):
    bin[7:9]  # Spare. According to Docs: "8 bytes for the future"
    bin[9]  # Unused. According to Docs: "det_flags is unknown as yet"
    bin[11]  # Spare. According to Docs: "4 bytes for the future"
    bin[14:16]  # Spare. According to Docs: "8 bytes for the future"
    bin[17:19]  # Spare. According to Docs: "8 bytes for the future"
    bin[19]  # Unused. According to Docs: "The exact contents and format are still TBD"
    bin[20:39]  # Spare. According to Docs: "8 bytes for the future"

    id_data = bin[4:5].view(dtype="u2")
    test_bits = np.flip(np.unpackbits(bin[12:13].view(dtype="u1")))

    return {
        "id": [id_data[0]],
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6]),
        "alert_tense": "test" if test_bits[31] else "current",
        "alert_type": "retraction" if test_bits[30] else "initial",
        "rate_snr": bin[10] * 1e-2,
        "binning_interval": bin[13] * 1e-4,
        "binning_interval_error": bin[16] * 1e-4,
        "temporal_coincidence": bool(test_bits[29]),
    }
