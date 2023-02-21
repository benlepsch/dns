# This is skeleton code for Networking Project Implementing a DNS server
# Uploading distributing the code or solution to this code will be consider an
# Honor code violation
# You should work on this project individually 
# -Best Daniel Graham PhD


# Task Implement DNS server that will act as an intermediary between user and other dns. 
# Your server will intercept and relay the traffic to the other DNS server. 
# However, for request to address in intercept.txt file the DNS should instead from it own request 
# relay the response.  For web request that the DNS server has already see it should 
# reply directly to responses without query the other server. 

import sys
import argparse
import logging
import socket
from  dnsPacket import DNSPacket
from dnsPacketModifier import DNSPacketModifier

DNS_UDP_PORT = 53 #Port 53 is the agreed on standard for DNS
BUFFERSIZE = 1024

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rServer',
                        help='the DNS server to forward recursive queries to')
    #Fun example of an intercept
    parser.add_argument('iFile', 
                        help='the containing list of urls to intercep example www.vt.edu @ 128.143.67.11')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose output')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)


    #Setup UDP socket that will  receice DNS request
    sock_DNS_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_DNS_in.bind(('127.0.0.1', DNS_UDP_PORT))

    #New instance of the Modifier
    modifier = DNSPacketModifier(args.iFile, args.rServer, DNS_UDP_PORT, BUFFERSIZE)

    #Don't worry about making this async yet.
    while True:
        try:
            data, addr = sock_DNS_in.recvfrom(BUFFERSIZE) # buffer size is 1024 bytes
            # print(data)
            logging.info('DNS Server State: %s', 'started and recieved first packet', extra={'bufferSize': BUFFERSIZE})
            dnsPacket = DNSPacket(data)
            print("----------------Packet Recieved------------\n " + str(dnsPacket))
            dnsPacketModified = modifier.modify(dnsPacket)
            print("----------------Packet Sent--------------\n " + str(dnsPacket))
            print(str(dnsPacketModified))
            sock_DNS_in.sendto(dnsPacketModified.serializePacket(),addr)
        except KeyboardInterrupt:
            sys.exit()

main()