from scapy.all import ls,IP
dest_ip="one.one.one.one"
ip_layer=IP(dst=dest_ip)
print(ls(ip_layer))
ip_layer=IP(dst=dest_ip)
print("destination=",ip_layer.dst)
print("summary=",ip_layer.summary())
