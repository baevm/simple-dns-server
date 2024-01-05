from app.dns_request import DNSRequest


def test_DNSRequest_pack():
    request = DNSRequest(
        b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01"
    )

    assert request.header != None
    assert request.questions != None

    expected = b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01"

    assert request.pack() == expected
