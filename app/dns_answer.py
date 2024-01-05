from dataclasses import dataclass
import struct

from app.utils import ip_to_bytes, marshal_domain_to_bytes, parse_domain


# https://www.rfc-editor.org/rfc/rfc1035#section-4.1.3
@dataclass
class DNSAnswer:
    def __init__(
        self,
        ANAME: bytes,
        ATYPE: int,
        ACLASS: int,
        TTL: int,
        RDLENGTH: int,
        RDATA: str,
    ):
        # domain name
        # TODO: use string instead of bytes
        self.ANAME = ANAME
        # https://www.rfc-editor.org/rfc/rfc1035#section-3.2.2
        self.ATYPE = ATYPE
        # https://www.rfc-editor.org/rfc/rfc1035#section-3.2.4
        self.ACLASS = ACLASS
        # cache time for record
        self.TTL = TTL
        # length of RDATA
        self.RDLENGTH = RDLENGTH
        # IP address
        self.RDATA = RDATA

    def pack(self) -> bytes:
        ATYPE = self.ATYPE.to_bytes(2, byteorder="big")
        ACLASS = self.ACLASS.to_bytes(2, byteorder="big")
        TTL = self.TTL.to_bytes(4, byteorder="big")
        RDLENGTH = self.RDLENGTH.to_bytes(2, byteorder="big")
        RDATA = ip_to_bytes(self.RDATA)

        answer = self.ANAME + ATYPE + ACLASS + TTL + RDLENGTH + RDATA

        return answer

    @staticmethod
    def unpack(data: bytes, offset: int, ANCOUNT: int) -> tuple[list["DNSAnswer"], int]:
        answers: list[DNSAnswer] = []

        for _ in range(ANCOUNT):
            name, offset = parse_domain(data, offset)

            atype, aclass, ttl, rdlength = struct.unpack(
                "!HHIH", data[offset : offset + 10]
            )
            offset += 10
            rdata = data[offset : offset + rdlength]

            # If type is A (1), convert rdata to an IP address
            if atype == 1:
                ip = ".".join(map(str, rdata))
            else:
                ip = ""

            answers.append(
                DNSAnswer(
                    ANAME=marshal_domain_to_bytes(name),
                    RDATA=ip,
                    ATYPE=atype,
                    ACLASS=aclass,
                    TTL=ttl,
                    RDLENGTH=rdlength,
                )
            )
            offset += rdlength

        return answers, offset
