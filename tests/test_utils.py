from app.utils import (
    ip_to_bytes,
    marshal_domain_to_bytes,
    parse_domain,
    unmarshal_bytes_to_domain,
)


def test_marshal_domain_to_bytes():
    domain = "yandex.com"

    assert marshal_domain_to_bytes(domain) == b"\x06yandex\x03com\x00"


def test_unmarshal_bytes_to_domain():
    bytes = b"\x06yandex\x03com\x00"

    assert unmarshal_bytes_to_domain(bytes) == "yandex.com"


def test_ip_to_bytes():
    ip1 = "8.8.8.8"
    ip2 = "77.88.55.77"

    assert ip_to_bytes(ip1) == b"\x08\x08\x08\x08"
    assert ip_to_bytes(ip2) == b"\x4d\x58\x37\x4d"


def test_parse_domain():
    bytes = b"\x06yandex\x03com\x00"

    assert parse_domain(bytes, 0) == ("yandex.com", 12)
