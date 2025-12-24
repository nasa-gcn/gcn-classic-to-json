import numpy as np

from ... import utils

trig_id_descriptions = {
    5: "This is not a real event.\n",
    29: "There was a temporal coincidence with another event.\n",
    30: "This is a test submission.\n",
}


def parse(bin):
    assert bin[12] == 0, "Unused. According to docs: 'Always 0 for FLT_LC'"
    bin[13:16]  # Unused. According to docs: '12 bytes for the future'
    bin[20:29]  # Unused. According to docs: '36 bytes for the future'

    lat, lon = bin[16:17].view(">i2")

    trig_id_bits = np.flip(np.unpackbits(bin[18:19].view(dtype="u1")))

    comments = "".join(
        [val for (key, val) in trig_id_descriptions.items() if trig_id_bits[key] == 1]
    )

    detector_options = ["on", "triggered"]
    detectors_bits = np.flip(np.unpackbits(bin[19:20].view(dtype="u1")))[:3]
    detectors_status = [detector_options[bit] for bit in detectors_bits]
    detectors = dict(zip(["HXM1", "HMX2", "SGM"], detectors_status))

    return {
        "mission": "CALET",
        "instrument": "GBM",
        "id": [bin[4]],
        "messenger": "EM",
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6]),
        "trigger_type": "rate",
        "rate_energy_range": np.flip(bin[17:18].view(">i2")),
        "rate_snr": bin[9] * 1e-2,
        "foreground_duration": bin[10] * 1e-2,
        "background_duration": bin[11] * 1e-2,
        "ra": bin[7] * 1e-4,
        "dec": bin[8] * 1e-4,
        "latitude": lat * 1e-2,
        "longitude": lon * 1e-2,
        "detector_status": detectors,
        "url": f"http://cgbm.calet.jp/cgbm_trigger/flight/{bin[4]}/"
        + utils.binary_to_string(bin[29:39]),
        "additional_info": comments if comments else None,
    }
