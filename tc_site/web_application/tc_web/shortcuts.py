from copy import copy


def merge_instances(obj_1, obj_2):
    buff_obj = copy(obj_1)
    for key, value in obj_2.__dict__.items():
        setattr(buff_obj, key, value)

    return buff_obj
