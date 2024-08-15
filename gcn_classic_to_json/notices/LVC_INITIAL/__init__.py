from ..LVC_PRELIMINARY import parse as parse_lvc_prelim


def parse(bin):
    property_bytes = bin[20:21].view(dtype=">u2")
    prob_ns, prob_remnant = property_bytes * 1e-2
    return {
        **parse_lvc_prelim(bin),
        "alert_type": "initial",
        "properties": ({"NS": prob_ns}, {"REMNANT": prob_remnant}),
    }
