import numpy as np

from ... import utils

detectors = ["Super-K", "LVD", "IceCube", "KamLAND", "Borexino", "Daya Bay", "HALO"]
detector_quality_opts = ["did not contribute", "possible", "good", "override"]


def parse(bin):
    bin[10]  # Spare. According to Docs: '4 bytes for the future'
    bin[14:18]  # Spare. According to Docs: '16 bytes for the future'
    bin[20:39]  # Spare. According to Docs: '76 bytes for the future'

    trig_id_bits = np.flip(np.unpackbits(bin[18:19].view(dtype="u1")))
    # trig_id_bits[0] contains if the detection in individual or coincidence.
    # I've intentially omitted this since it can be infered from detector quality

    ra, dec = bin[7] * 1e-4, bin[8] * 1e-4

    misc_bits = np.flip(np.unpackbits(bin[19:20].view(dtype="u1")))

    detector_quality = {}
    for idx in range(len(detectors)):
        if not misc_bits[4 * idx]:
            detector_quality[detectors[idx]] = detector_quality_opts[0]
        elif misc_bits[4 * idx + 1]:
            detector_quality[detectors[idx]] = detector_quality_opts[1]
        elif misc_bits[4 * idx + 2]:
            detector_quality[detectors[idx]] = detector_quality_opts[2]
        elif misc_bits[4 * idx + 3]:
            detector_quality[detectors[idx]] = detector_quality_opts[3]

    return {
        "alert_type": "retraction" if trig_id_bits[5] else "initial",
        "alert_tense": "test" if trig_id_bits[1] else "current",
        "messenger": "Neutrino",
        "id": [bin[4]],
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6]),
        "ra": None if trig_id_bits[2] else ra,
        "dec": None if trig_id_bits[2] else dec,
        "ra_dec_error": bin[11] * 1e-4,
        "systematic_included": True,
        "containment_probability": bin[12] * 1e-2,
        "n_events": bin[9],
        "duration": bin[13] * 1e-2,
        "detector_quality": detector_quality,
    }
