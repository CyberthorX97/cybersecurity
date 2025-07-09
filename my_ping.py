from scapy.all import ICMP,IP,sr

if __name__=="__main__":
    src_ip="192.168.176.131" # indirizzo di partenza
    dest_ip="1.1.1.1"    # indirizzo ricevente il pacchetto
    ip_layer=IP(src=src_ip, dst=dest_ip)
    print(ip_layer.show())
    icmp_req=ICMP(id=100)
    packet=ip_layer/icmp_req
    response,_=sr(packet,iface="eth0")
    # def sr(:packet, iface):
    #.....
    #returnresponse1,response2
    if response:
        response.show()
