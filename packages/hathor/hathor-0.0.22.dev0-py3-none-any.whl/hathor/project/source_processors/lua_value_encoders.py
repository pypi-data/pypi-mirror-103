import json
from typing import List


def stringify_arg_list(arg_list):
    return list(map(str, arg_list))


def roblox_userdata(userdata_name: str, arg_list: List[str]):
    arg_list_str = ", ".join(arg_list)
    return f"{userdata_name}.new({arg_list_str})"


def roblox_userdata_str_args(userdata_name: str, arg_list: List):
    return roblox_userdata(userdata_name, stringify_arg_list(arg_list))


def vector3(arg_list):
    return roblox_userdata_str_args("Vector3", arg_list)


def brick_color(arg_list):
    arg_list_str = ", ".join(stringify_arg_list(arg_list[-3:]))

    return f"BrickColor.new({arg_list_str})"


def c_frame(arg_list):
    return roblox_userdata_str_args("CFrame", arg_list)


def color_3(arg_list):
    return roblox_userdata_str_args("Color3", arg_list)


def string(v):
    v = str(v)

    if "\n" in v:
        return f"[[==[[{str(v)}]]==]]"

    else:
        return f"\"{str(v)}\""


def vector2(arg_list):
    return roblox_userdata_str_args("Vector2", arg_list)


def color_sequence_keypoint(arg_list):
    time = arg_list[0]
    color = color_3(arg_list[1])

    return f"ColorSequenceKeypoint.new({time}, {color})"


def color_sequence(arg_list):
    arg_list = ", ".join(stringify_arg_list(map(color_sequence_keypoint, arg_list)))
    return "ColorSequence.new { " + arg_list + " }"


def number_sequence_keypoint(arg_list):
    return roblox_userdata_str_args("NumberSequenceKeypoint", arg_list)


def number_sequence(arg_list):
    arg_list = ", ".join(stringify_arg_list(map(number_sequence_keypoint, arg_list)))
    return "NumberSequence.new { " + arg_list + " }"


VALUE_ENCODERS = {
    "Primitive": {
        "bool": lambda v: "true" if v else "false",
        "string": string,
    },
    "DataType": {
        "BrickColor": brick_color,
        "Content": string,
        "ColorSequenceKeypoint": color_sequence_keypoint,
        "ColorSequence": color_sequence,
        "NumberSequenceKeypoint": number_sequence_keypoint,
        "NumberSequence": number_sequence
    }
}


class NoEncoder(RuntimeError):
    def __init__(self, value_type):
        super().__init__(json.dumps(value_type, indent=2))


def value_encoder(category: str, type_name: str):
    try:
        encoder = VALUE_ENCODERS[category][type_name]

    except KeyError:
        if category == "DataType":
            return lambda v: roblox_userdata_str_args(type_name, v)

        elif category == "Primitive":
            return str

        raise NoEncoder({
            "Category": category,
            "Name": type_name
        })

    return encoder
