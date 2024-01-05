from app.dns_question import DNSQuestion


def test_DNSQuestion_pack():
    question = DNSQuestion(
        QNAME=b"\x06google\x03com\x00",
        QTYPE=1,
        QCLASS=1,
    )

    packed_question = question.pack()
    assert packed_question == b"\x06google\x03com\x00\x00\x01\x00\x01"


def test_DNSQuestion_unpack():
    dns_question_with_header = (
        b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        + b"\x06google\x03com\x00\x00\x01\x00\x01"
    )

    questions, offset = DNSQuestion.unpack(dns_question_with_header, 1)

    assert questions[0].QNAME == b"\x06google\x03com\x00"
    assert questions[0].QTYPE == 1
    assert questions[0].QCLASS == 1
    assert offset == 28
