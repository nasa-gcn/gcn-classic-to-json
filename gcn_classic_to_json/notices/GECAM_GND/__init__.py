import numpy as np
from scipy.stats import norm

from ... import utils

src_class_vals = ["GRB", "SFLARE", "KNOWN_SOURCE", "GENERIC_SOURCE"]

containment_prob = norm().cdf(1) - norm.cdf(-1)


def parse(bin):
    bin[15]  # Unused. According to docs: '4 bytes for the future'
    bin[20:39]  # Unused. According to docs: '76 bytes for the future'

    soln_status_bits = np.flip(np.unpackbits(bin[18:19].view(dtype="u1")))

    return {
        "mission": "GECAM",
        "id": [bin[4]],
        "messenger": "EM",
        "mission_type": chr(bin[19] + 64),
        # There is an error here; You are supposed to divide by 8640000 to get the correct value
        # But it only seems to work if you divide by 864000000; I'm assuming it's some error in encoding the packets
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6] * 1e-2),
        "trigger_type": "rate",
        "net_count_rate": bin[9],
        "rate_duration": bin[14] * 1e-4,
        "ra": bin[7] * 1e-4,
        "dec": bin[8] * 1e-4,
        "ra_dec_error": bin[10] * 1e-4,
        "containment_probability": containment_prob,
        "instrument_phi": bin[12] * 1e-2,
        "instrument_theta": bin[13] * 1e-2,
        "latitude": bin[16] * 1e-2,
        "longitude": bin[17] * 1e-2,
        "classification": ({src_class_vals[bin[11] - 1]: 1},),
        "additional_info": (
            "This is a test notice." if soln_status_bits[0] == 1 else None
        ),
    }
