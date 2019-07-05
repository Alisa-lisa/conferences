""" Helper functions """


def repr(in_dict):
    return "\n".join(v.to_string() for v in in_dict.values())

