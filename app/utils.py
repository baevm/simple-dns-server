import struct


# yandex.com => b"\x06yandex\x03com\x00"
def marshal_domain_to_bytes(name: str) -> bytes:
    parts = name.split(".")

    result = b""

    for part in parts:
        length = len(part)
        result += length.to_bytes(1, byteorder="big") + part.encode()

    result += b"\x00"

    return result


# b"\x06yandex\x03com\x00" => yandex.com
def unmarshal_bytes_to_domain(byte_string: bytes) -> str:
    result = ""
    i = 0

    while i < len(byte_string):
        length = byte_string[i]
        i += 1
        substring = byte_string[i : i + length].decode("utf-8")
        result += substring + "."
        i += length

    # remove trailing dot
    return result.rstrip(".")


def ip_to_bytes(ip: str) -> bytes:
    res = b""
    if len(ip) == 0:
        return res
    for i in ip.split("."):
        res += int(i).to_bytes(1, byteorder="big")
    return res


def parse_domain(message: bytes, offset: int) -> tuple[str, int]:
    labels = []
    while True:
        length = message[offset]

        if length & 0xC0 == 0xC0:  # Check for compression
            pointer = struct.unpack("!H", message[offset : offset + 2])[0]
            offset += 2
            pointer &= 0x3FFF  # Remove the compression flag bits
            part, _ = parse_domain(message, pointer)
            labels.append(part)
            return ".".join(labels), offset

        offset += 1  # Skip the length byte

        if length == 0:  # End of the domain name
            break

        labels.append(
            message[offset : offset + length].decode("utf-8", errors="replace")
        )
        offset += length

    return ".".join(labels), offset
