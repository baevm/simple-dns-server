from dataclasses import dataclass

from app.dns_answer import DNSAnswer
from app.dns_header import DNSHeader
from app.dns_question import DNSQuestion


@dataclass
class DNSResponse:
    def __init__(
        self, header: DNSHeader, questions: list[DNSQuestion], answers: list[DNSAnswer]
    ):
        self.header: DNSHeader = header
        self.questions: list[DNSQuestion] = questions
        self.answers: list[DNSAnswer] = answers

    def pack(self) -> bytes:
        packed_questions = b"".join([q.pack() for q in self.questions])
        packed_answers = b"".join([a.pack() for a in self.answers])

        return self.header.pack() + packed_questions + packed_answers

    @staticmethod
    def unpack(data: bytes) -> "DNSResponse":
        header = DNSHeader.unpack(data)
        questions, offset = DNSQuestion.unpack(data, header.QDCOUNT)
        answers, _ = DNSAnswer.unpack(data, offset, header.ANCOUNT)

        dns_response = DNSResponse(header=header, questions=questions, answers=answers)

        return dns_response
