import numpy as np

from ... import utils

time_options = [
    "undefined/unavailable",
    "1 sec",
    "3 sec",
    "10 sec",
    "30 sec",
    "1 scan",
    "1 orbit",
    "4 orbit",
    "1 day",
]

energy_range_options = ["undefined/unavailable", [2, 4], [4, 10], [10, 20], [2, 10]]

# unit in data is in unit mCrabs; need to be converted into erg/cm^2/sec^-1
# Conversion factors are from Kawamuro et. al. (2018)
conversion_factors = [4e-12, 1.24e-11, 1.65e-11, 8.74e-12]


def parse(bin):
    bin[
        4
    ]  # Temporarily Unused. According to source code: 'Trigger ID number (only partial of the full MAXI ID number)'
    bin[10]  # Spare. According to Docs: '4 bytes for future use'.
    bin[17]  # Spare. According to Docs: '4 bytes for future use'.
    bin[20:39]  # Spare. According to Docs: '76 bytes for future use'.

    source_low, bkg_low = np.flip(bin[12:13].view(dtype=">i2"))
    source_medium, bkg_medium = np.flip(bin[13:14].view(dtype=">i2"))
    source_high, bkg_high = np.flip(bin[14:15].view(dtype=">i2"))

    time_opt, e_opt, _, _ = np.flip(bin[15:16].view(dtype="i1"))

    lon, lat = np.flip(bin[16:17].view(dtype=">i2"))

    event_flag_bits = np.flip(np.unpackbits(bin[18:19].view(dtype="u1")))

    comments = ""
    if event_flag_bits[4] == 1:
        comments += "This notice contains negative flux.\n"

    misc_bits = np.flip(np.unpackbits(bin[19:20].view(dtype="u1")))

    if misc_bits[30] == 1:
        comments += "This notice was ground-generated."

    return {
        "mission": "MAXI",
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6]),
        "messenger": "EM",
        "flux_energy_range": energy_range_options[e_opt],
        "duration": time_options[time_opt],
        "ra": bin[7] * 1e-4,
        "dec": bin[8] * 1e-4,
        "ra_dec_error": bin[11] * 1e-4,
        "source_flux_low_band": source_low * 0.1,
        "background_flux_low_band": bkg_low * 0.1,
        "source_flux_medium_band": source_medium * 0.1,
        "background_flux_medium_band": bkg_medium * 0.1,
        "source_flux_high_band": source_high * 0.1,
        "background_flux_high_band": bkg_high * 0.1,
        "systematic_included": True,
        "latitude": lat * 1e-2,
        "longitude": lon * 1e-2,
        "energy_flux": (
            bin[9] * 0.1 * conversion_factors[e_opt - 1] if e_opt != 0 else None
        ),
        "additional_info": comments if comments else None,
    }
