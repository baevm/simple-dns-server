from dataclasses import dataclass

from app.dns_header import DNSHeader
from app.dns_question import DNSQuestion


@dataclass
class DNSRequest:
    def __init__(self, data: bytes):
        self.header = DNSHeader.unpack(data)
        self.questions, _ = DNSQuestion.unpack(data, self.header.QDCOUNT)

    def pack(self) -> bytes:
        return self.header.pack() + b"".join([q.pack() for q in self.questions])
