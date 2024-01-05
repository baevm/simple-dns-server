from app.dns_answer import DNSAnswer


def test_DNSAnswer_pack():
    answer = DNSAnswer(
        ANAME=b"\x06google\x03com\x00",
        RDATA="8.8.8.8",
        ATYPE=1,
        ACLASS=1,
        TTL=3600,
        RDLENGTH=4,
    )

    expected = (
        b"\x06google\x03com\x00\x00\x01\x00\x01\x00\x00\x0e\x10\x00\x04\x08\x08\x08\x08"
    )

    assert answer.pack() == expected


def test_DNSAnswer_unpack():
    data = (
        b"\x06google\x03com\x00\x00\x01\x00\x01\x00\x00\x0e\x10\x00\x04\x08\x08\x08\x08"
    )
    offset = 0
    ANCOUNT = 1

    answers, offset = DNSAnswer.unpack(data, offset, ANCOUNT)

    assert len(answers) == 1
    assert offset == 26

    answer = answers[0]

    assert answer.ANAME == b"\x06google\x03com\x00"
    assert answer.RDATA == "8.8.8.8"
