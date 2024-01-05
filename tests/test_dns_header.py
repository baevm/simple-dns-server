from app.dns_header import DNSHeader


def test_DNSHeader_pack():
    header = DNSHeader(
        ID=0,
        QR=0,
        OPCODE=0,
        RD=1,
        RA=0,
        AA=0,
        TC=0,
        QDCOUNT=1,
        ANCOUNT=0,
        NSCOUNT=0,
        ARCOUNT=0,
        RCODE=0,
        Z=0,
    )

    packed_header = header.pack()
    assert packed_header == b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"


def test_DNSHeader_unpack():
    header = DNSHeader.unpack(b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00")

    assert header.ID == 0
    assert header.QR == 0
    assert header.OPCODE == 0
    assert header.RD == 1
    assert header.RA == 0
    assert header.AA == 0
    assert header.TC == 0
    assert header.QDCOUNT == 1
    assert header.ANCOUNT == 0
    assert header.NSCOUNT == 0
    assert header.ARCOUNT == 0
    assert header.RCODE == 0
    assert header.Z == 0
