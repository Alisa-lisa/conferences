""" Helper functions """
import random

def repr(in_dict):
    return "\n".join(v.to_string() for v in in_dict.values())



def get_random_position(conf):
    """
    Helper function
    :return: tuple int
    """
    return random.randint(0, conf["x"]), random.randint(0, conf["y"])