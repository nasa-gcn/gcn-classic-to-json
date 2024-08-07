from ... import utils


def parse(bin):
    bin[15]  # Unused. According to docs: '4 bytes for the future'
    bin[27:39]  # Unused. According to docs: '32 bytes for the future'
    bin[
        11
    ]  # Temporarily Unused. Should have a int->class_type mapping but incomplete documentation
    bin[
        18
    ]  # Temporarily Unused. Should have a bit->flag mapping but incomplete documenation
    bin[21]  # Temporarily Unused. How is it different from burst_dur?
    bin[22:24]  # Unused. Equivalent to rate_energy_range
    bin[
        26
    ]  # Temporarily Unused. Presumably which detectors activated but incomplete documenation
    return {
        "mission": "GECAM",
        "id": [bin[4]],
        "messenger": "EM",
        "mission_type": chr(bin[19] + 64),  # mission type is A or B
        # There is an error here; You are supposed to divide by 8640000 to get the correct value
        # But it only seems to work if you divide by 864000000; I'm assuming it's some error in encoding the packets
        "trigger_time": utils.datetime_to_iso8601(bin[5], bin[6] * 1e-2),
        "trigger_type": "rate",
        "rate_energy_range": [bin[24], bin[25]],
        "rate_snr": bin[20] * 1e-2,
        "net_count_rate": int(bin[9]),
        "rate_duration": bin[14] * 1e-4,
        "ra": bin[7] * 1e-4,
        "dec": bin[8] * 1e-4,
        "ra_dec_error": bin[10] * 1e-4,
        "containment_probability": 0.68,
        "instrument_phi": bin[12] * 1e-2,
        "instrument_theta": bin[13] * 1e-2,
        "latitude": bin[16] * 1e-2,
        "longitude": bin[17] * 1e-2,
    }
