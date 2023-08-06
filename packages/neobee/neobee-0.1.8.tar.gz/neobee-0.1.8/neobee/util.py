def uint32_to_float(data):
    return ((data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]) / 100


def HighByte(val: int):
    return (val >> 8) & 0xFF


def LowByte(val: int):
    return val & 0xFF


def HighWord(val: int):
    return (val >> 16) & 0xFFFF


def LowWord(val: int):
    return val & 0xFFFF


def print_hex_buffer(buffer):
    print(":".join("{:02x}".format(x) for x in buffer))


def f100(arr):
    """
    Decodes a four bytes encoded signed float
    value.
    The highest bit of the first byte indicates
    wether the value is negative (1) or not (0).
    """
    NEGFLAG = arr[0] & 0b10000000
    if NEGFLAG:
        # Clear the negative flag
        value = ((arr[0] & 0b01111111) << 24) | (arr[1] << 16) | (arr[2] << 8) | arr[3]
        return (-1 * value) / 100.0

    return ((arr[0] << 24) | (arr[1] << 16) | (arr[2] << 8) | arr[3]) / 100


def unpack_hive_data(buffer):
    """
    Unpacks the raw data payload of an neobee measurement payload.
    The function returns an dict with th following keys:

    - mac
    - weight
    - temperature_inside
    - temperature_outside

    """
    return {
        "mac": ":".join([hex(b)[2:4].upper() for b in buffer[:6]]),
        "weight": f100(buffer[6:10]),
        "temperature_inside": f100(buffer[10:14]),
        "temperature_outside": f100(buffer[14:18]),
    }
