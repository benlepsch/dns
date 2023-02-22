from socket import *
from dnsPacket import DNSPacket
from Utilities import Util
from answerSection import AnswerSection

class DNSPacketModifier:

  

    def __init__(self, _file, _serverName, _DNS_UDP_PORT, _BUFFERSIZE):
        self.DNS_UDP_PORT = _DNS_UDP_PORT
        self.BUFFERSIZE = _BUFFERSIZE
        self.serverName = _serverName
        self.urlIPMap = self.parseFile(_file)
        self.socket_DNS_out = socket(AF_INET, SOCK_DGRAM)
        self.dnsCache = {}

        
         
    def parseFile(self, _file):
        """
            This function parsers the file. 
            This file currently only supports IPV4 address.
        """
        urlIPMap = {}
        lines = open(_file,'r').readlines()
        for line in  lines: 
            splitLine = line.split(' ')
            urlIPMap[splitLine[0]] = splitLine[1]
        return urlIPMap

    def modify(self, dnsPacket): 
        """
            This function is responsible for representing the modify module in the write
            It should take in a DNSPacket. Do a recursive query and get the result.
            If intercept.txt file contains the QNAME found it query it should replace the answer
            section with IPV4 address from the intercept file. 
            Finally it should cache the result and then check the cache before doing future recursive queries. 
        """
        
        self.socket_DNS_out.sendto(dnsPacket.serializePacket(), ('8.8.8.8', 53))
        data, addr = self.socket_DNS_out.recvfrom(2048)
        dnsPacket = DNSPacket(data)

        print('in modify: arraylen: {}\tancount: {}'.format(len(dnsPacket.ArrayOfAnswers), dnsPacket.get_ANCOUNT()))
        
        if (q := dnsPacket.ArrayOfQuestions[0].get_QNAME()) in self.dnsCache:
            pass
        elif q in self.urlIPMap:
            mod_ip = self.urlIPMap[q]
            print('it\'s in: {}'.format(mod_ip))
        else:
            print('qname: {}'.format(q))
            return dnsPacket
        
        for i, a in enumerate(dnsPacket.ArrayOfAnswers):
            print('type: {}'.format(a.get_TYPE()))
            if (at := a.get_TYPE()) == 1: # ipv4
                a.set_RDATA(mod_ip)
                dnsPacket.replaceAnswerSection(a, i)
                print('setting data')
                
            if at == 28:
                # print('leaving')
                pass # ipv6

        print('----------')
        return dnsPacket
        
        # for i, a in enumerate(dnsPacket.ArrayOfAnswers):

        #     # step 1 if it's looking for a cached address return that
        #     if dnsPacket.ArrayOfQuestions[i].get_QNAME() in self.dnsCache:
        #         pass
        #     else:
        #         if dnsPacket.ArrayOfQuestions[i].get_QNAME() in self.urlIPMap:
        #             # modify corresponding answer section
        #             print('MODIFYING ANCOUNT: {}'.format(dnsPacket.get_ANCOUNT()))
        #             if a.get_RDLENGTH() != 4:
        #                 a.set_RDLENGTH(4)
        #             a.set_RDATA(self.urlIPMap[dnsPacket.ArrayOfQuestions[i].get_QNAME()])
                    
        #             dnsPacket.replaceAnswerSection(a, i)
        #             if not dnsPacket.get_ANCOUNT() == 1:
        #                 dnsPacket.set_ANCOUNT(1)
                    
        # return dnsPacket
