import numpy as np

from ..GECAM_GND import parse as parse_gecam_gnd


def parse(bin):
    bin[15]  # Unused. According to docs: '4 bytes for the future'
    bin[27:39]  # Unused. According to docs: '32 bytes for the future'
    bin[21]  # Temporarily Unused. This is trigger_duration; currently no keyword
    bin[22:24]  # Unused. Equivalent to rate_energy_range

    detector_options = ["on", "triggered"]
    detector_bits = np.flip(np.unpackbits(bin[26:27].view(dtype="u1")))
    detector_status = [detector_options[bit] for bit in detector_bits[:25]]
    detectors = dict(zip(list(np.arange(25.0) + 1), detector_status))

    return {
        **parse_gecam_gnd(bin),
        "rate_snr": bin[20] * 1e-2,
        "rate_energy_range": [bin[24], bin[25]],
        "detector_status": detectors,
    }
