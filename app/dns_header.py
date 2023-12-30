from dataclasses import dataclass
import struct


# https://www.rfc-editor.org/rfc/rfc1035#section-4.1.1
@dataclass
class DNSHeader:
    def __init__(
        self,
        ID: int,
        QR: int,
        OPCODE: int,
        RD: int,
        QDCOUNT: int,
        ANCOUNT: int,
        NSCOUNT: int = 0,
        ARCOUNT: int = 0,
        AA: int = 0,
        TC: int = 0,
        RCODE: int = 0,
        RA: int = 0,
        Z: int = 0,
    ):
        # Random id assigned to every DNS query. Used to match responses to requests.
        self.ID: int = ID
        # Query/Response flag. 0 for query, 1 for response.
        self.QR: int = QR
        # Operation code. 0 for standard query.
        self.OPCODE: int = OPCODE
        # Authoritative Answer flag. 1 if the responding server is authoritative for the domain name in question section.
        self.AA: int = AA
        # 1 if message is larger than 512 bytes and was truncated. Always 0 in UDP responses.
        self.TC: int = TC
        # Recursion Desired flag. 1 if the client wants the server to recursively resolve the domain name in question section.
        self.RD: int = RD
        # Recursion Available flag. 1 if the server supports recursion.
        self.RA: int = RA
        # Reserved field. Always 0.
        self.Z: int = Z
        # Response code. 0 for no error.
        self.RCODE: int = RCODE
        # Number of questions in the question section.
        self.QDCOUNT: int = QDCOUNT
        # Number of resource records in the answer section.
        self.ANCOUNT: int = ANCOUNT
        # Number of resource records in the authority section.
        self.NSCOUNT: int = NSCOUNT
        # Number of resource records in the additional section.
        self.ARCOUNT: int = ARCOUNT

    def pack(self) -> bytes:
        flags = (
            (self.QR << 15)
            | (self.OPCODE << 11)
            | (self.AA << 10)
            | (self.TC << 9)
            | (self.RD << 8)
            | (self.RA << 7)
            | (self.Z << 4)
            | self.RCODE
        )

        header = struct.pack(
            ">HHHHHH",
            self.ID,
            flags,
            self.QDCOUNT,
            self.ANCOUNT,
            self.NSCOUNT,
            self.ARCOUNT,
        )
        return header

    @staticmethod
    def unpack(data: bytes) -> "DNSHeader":
        start, end = 0, 12

        id, flags, qdcount, ancount, nscount, arcount = struct.unpack(
            "!HHHHHH", data[start:end]
        )

        qr = (flags >> 15) & 0x1
        opcode = (flags >> 11) & 0xF
        aa = (flags >> 10) & 0x1
        tc = (flags >> 9) & 0x1
        rd = (flags >> 8) & 0x1
        ra = (flags >> 7) & 0x1
        z = (flags >> 4) & 0x7
        rcode = 0 if opcode == 0 else 4

        header = DNSHeader(
            ID=id,
            QR=qr,
            OPCODE=opcode,
            RD=rd,
            RA=ra,
            AA=aa,
            TC=tc,
            QDCOUNT=qdcount,
            ANCOUNT=ancount,
            NSCOUNT=nscount,
            ARCOUNT=arcount,
            RCODE=rcode,
            Z=z,
        )

        return header
