import argparse
import socket
import traceback
from app.dns_request import DNSRequest
from app.dns_response import DNSResponse
from app.dns_answer import DNSAnswer
from app.dns_header import DNSHeader
from app.utils import unmarshal_bytes_to_domain


DNS_TABLE = {
    "google.com": "8.8.8.8",
    "ya.ru": "77.88.55.242",
    "abc.longassdomainname.com": "6.6.6.6",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--resolver",
        required=False,
        default=None,
        type=str,
        help="DNS Resolver. Used to forward requests to another DNS server. Example: 8.8.8.8",
    )
    args = parser.parse_args()
    resolver_args: str = args.resolver

    print("Resolver:", resolver_args)
    if resolver_args:
        resolver_ip_port = resolver_args.split(":")
        resolver_ip = resolver_ip_port[0]
        resolver_port = int(resolver_ip_port[1]) if len(resolver_ip_port) > 1 else 53

    print("Starting server on 0.0.0.0:2053")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)

            request = DNSRequest(buf)

            questions = request.questions

            if not resolver_args:
                answers: list[DNSAnswer] = []

                for q in questions:
                    qname = unmarshal_bytes_to_domain(q.QNAME)

                    if qname in DNS_TABLE:
                        answers.append(
                            DNSAnswer(
                                ANAME=q.QNAME,
                                ATYPE=q.QTYPE,
                                ACLASS=q.QCLASS,
                                TTL=3600,
                                RDLENGTH=4,
                                RDATA=DNS_TABLE[qname],
                            )
                        )

                response_header = DNSHeader(
                    ID=request.header.ID,
                    QR=1,
                    OPCODE=request.header.OPCODE,
                    RD=request.header.RD,
                    QDCOUNT=request.header.QDCOUNT,
                    ANCOUNT=len(answers),
                    NSCOUNT=request.header.NSCOUNT,
                    ARCOUNT=request.header.ARCOUNT,
                    AA=0,
                    TC=0,
                    RCODE=request.header.RCODE,
                    RA=0,
                    Z=request.header.Z,
                )

                msg = DNSResponse(
                    header=response_header,
                    questions=questions,
                    answers=answers,
                )

                response = msg.pack()

                udp_socket.sendto(response, source)
            else:
                with socket.socket(
                    socket.AF_INET, socket.SOCK_DGRAM
                ) as resolver_socket:
                    answers: list[DNSAnswer] = []

                    for question in questions:
                        query = request.header.pack() + question.pack()

                        resolver_socket.sendto(query, (resolver_ip, resolver_port))
                        response, _ = resolver_socket.recvfrom(512)

                        unpacked_response = DNSResponse.unpack(response)
                        answers.extend(unpacked_response.answers)

                    response_header = DNSHeader(
                        ID=request.header.ID,
                        QR=1,
                        OPCODE=request.header.OPCODE,
                        RD=request.header.RD,
                        QDCOUNT=request.header.QDCOUNT,
                        ANCOUNT=len(answers),
                        NSCOUNT=request.header.NSCOUNT,
                        ARCOUNT=request.header.ARCOUNT,
                        AA=0,
                        TC=0,
                        RCODE=request.header.RCODE,
                        RA=0,
                        Z=request.header.Z,
                    )

                    resp = DNSResponse(
                        header=response_header,
                        questions=questions,
                        answers=answers,
                    )

                    response = resp.pack()

                    udp_socket.sendto(response, source)

        except Exception as e:
            print(f"Error receiving data:\n")
            try:
                raise TypeError("wtf !?!")
            except:
                pass

            traceback.print_tb(e.__traceback__)
            break


if __name__ == "__main__":
    main()
