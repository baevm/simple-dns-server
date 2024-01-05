from app.dns_answer import DNSAnswer
from app.dns_header import DNSHeader
from app.dns_question import DNSQuestion
from app.dns_response import DNSResponse


def test_DNSResponse_pack():
    response = DNSResponse(
        header=DNSHeader(
            ID=0,
            QR=1,
            OPCODE=0,
            RD=1,
            RA=0,
            AA=0,
            TC=0,
            QDCOUNT=1,
            ANCOUNT=1,
            NSCOUNT=0,
            ARCOUNT=0,
            RCODE=0,
            Z=0,
        ),
        questions=[
            DNSQuestion(
                QNAME=b"\x06google\x03com\x00",
                QTYPE=1,
                QCLASS=1,
            )
        ],
        answers=[
            DNSAnswer(
                ANAME=b"\x06google\x03com\x00",
                ATYPE=1,
                ACLASS=1,
                TTL=0,
                RDLENGTH=4,
                RDATA="8.8.8.8",
            )
        ],
    )

    packed_response = response.pack()
    assert (
        packed_response
        == b"\x00\x00\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00"
        + b"\x06google\x03com\x00\x00\x01\x00\x01"
        + b"\x06google\x03com\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x04\x08\x08\x08\x08"
    )


def test_DNSResponse_unpack():
    dns_response = (
        b"\x00\x00\x81\x00\x00\x01\x00\x01\x00\x00\x00\x00"
        + b"\x06google\x03com\x00\x00\x01\x00\x01"
        + b"\x06google\x03com\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x04\x08\x08\x08\x08"
    )

    response = DNSResponse.unpack(dns_response)

    assert response.header.ID == 0
    assert response.header.QR == 1
    assert response.header.OPCODE == 0
    assert response.header.RD == 1
    assert response.header.RA == 0
    assert response.header.AA == 0
    assert response.header.TC == 0
    assert response.header.QDCOUNT == 1
    assert response.header.ANCOUNT == 1
    assert response.header.NSCOUNT == 0
    assert response.header.ARCOUNT == 0
    assert response.header.RCODE == 0
    assert response.header.Z == 0

    assert response.questions[0].QNAME == b"\x06google\x03com\x00"
    assert response.questions[0].QTYPE == 1
    assert response.questions[0].QCLASS == 1

    assert response.answers[0].ANAME == b"\x06google\x03com\x00"
    assert response.answers[0].ATYPE == 1
    assert response.answers[0].ACLASS == 1
    assert response.answers[0].TTL == 0
    assert response.answers[0].RDLENGTH == 4
    assert response.answers[0].RDATA == "8.8.8.8"
