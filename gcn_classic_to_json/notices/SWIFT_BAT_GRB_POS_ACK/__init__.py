from ... import utils


def parse(bin):
    return {
        "trigger_time": utils.tjd_to_jd(bin[5], bin[6]),
        "ra": 1e-4 * bin[7],
        "dec": 1e-4 * bin[8],
        "ra_dec_error": 1e-4 * bin[11],
    }
