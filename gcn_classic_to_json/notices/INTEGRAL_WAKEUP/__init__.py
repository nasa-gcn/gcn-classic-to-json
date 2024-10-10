import numpy as np

from ... import utils


def parse_integral(bin):
    bin[9]  # Unused. According to Docs: "det_flags is unknown as yet"
    bin[17:19]  # Spare. According to Docs: "8 bytes for the future"
    bin[19]  # Unused. According to Docs: "The exact contents and format are still TBD"
    bin[20:39]  # Spare. According to Docs: "76 bytes for the future"

    id_data = bin[4:5].view(dtype="u2")
    test_bits = np.flip(np.unpackbits(bin[12:13].view(dtype="u1")))

    return {
        "id": [id_data[0]],
        "alert_datetime": utils.datetime_to_iso8601(bin[5], bin[6]),
        "ra": bin[7] * 1e-4,
        "dec": bin[8] * 1e-4,
        "ra_dec_error": bin[11] / 3600,
        "rate_snr": bin[10] * 1e-2,
        "ra_pointing": bin[14] * 1e-4,
        "dec_pointing": bin[15] * 1e-4,
        "time_scale": bin[13] * 1e-4,
        "time_error": bin[16] * 1e-4,
        "temporal_coincidence": bool(test_bits[29]),
        "spatial_coincidence": bool(test_bits[28]),
    }


def parse(bin):
    return parse_integral(bin)
