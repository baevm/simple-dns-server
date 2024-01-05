from dataclasses import dataclass
import struct

from app.utils import marshal_domain_to_bytes, parse_domain


# https://www.rfc-editor.org/rfc/rfc1035#section-4.1.2
@dataclass
class DNSQuestion:
    def __init__(self, QNAME: bytes, QTYPE: int, QCLASS: int):
        # Domain name
        # TODO: use string instead of bytes 
        self.QNAME: bytes = QNAME
        # https://www.rfc-editor.org/rfc/rfc1035#section-3.2.2
        self.QTYPE: int = QTYPE
        # https://www.rfc-editor.org/rfc/rfc1035#section-3.2.4
        self.QCLASS: int = QCLASS

    def pack(self) -> bytes:
        question = self.QNAME + struct.pack(">HH", self.QTYPE, self.QCLASS)

        return question

    @staticmethod
    def unpack(data: bytes, qdcount: int) -> tuple[list["DNSQuestion"], int]:
        questions = []
        offset = 12  # Start after the header

        for _ in range(qdcount):
            domain, offset = parse_domain(data, offset)

            qtype, qclass = struct.unpack("!HH", data[offset : offset + 4])

            bytes_domain = marshal_domain_to_bytes(domain)

            questions.append(
                DNSQuestion(QNAME=bytes_domain, QTYPE=qtype, QCLASS=qclass)
            )
            offset += 4

        return questions, offset
