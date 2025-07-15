from scapy.all import sniff  # Importa la funzione sniff dalla libreria Scapy per catturare pacchetti di rete

# Dizionario per memorizzare le associazioni tra indirizzi MAC e indirizzi IP osservati
IP_MAC_Map = {}

# Funzione chiamata ogni volta che viene intercettato un pacchetto ARP
def processPacket(packet):
    if packet.haslayer('ARP'):  # Verifica se il pacchetto contiene un livello ARP
        src_IP = packet['ARP'].psrc         # Estrae l'indirizzo IP sorgente dal pacchetto ARP
        src_MAC = packet['Ether'].src       # Estrae l'indirizzo MAC sorgente dal livello Ethernet

        if src_MAC in IP_MAC_Map:  # Se il MAC è già noto
            if IP_MAC_Map[src_MAC] != src_IP:  # Se l'IP associato al MAC è cambiato
                old_IP = IP_MAC_Map.get(src_MAC, "unknown")  # Recupera l'IP precedente associato al MAC
                message = ("\nPossible ARP attack detected!\n"
                           + f"Machine with IP {old_IP} is pretending to be {src_IP}\n")
                print(message)  # Stampa un messaggio di allerta per possibile attacco ARP Spoofing
            else:
                IP_MAC_Map[src_MAC] = src_IP  # Aggiorna l'associazione MAC-IP se coerente
        else:
            IP_MAC_Map[src_MAC] = src_IP  # Registra un nuovo MAC-IP mai visto prima

        # Log informativo per ogni pacchetto ARP ricevuto
        print(f"Received ARP packet: IP={src_IP}, MAC={src_MAC}")

# Avvia il packet sniffer:
# - count=0: nessun limite, cattura infinita
# - filter="arp": cattura solo pacchetti ARP
# - store=0: non conserva i pacchetti in memoria
# - prn=processPacket: chiama la funzione per ogni pacchetto ricevuto
sniff(count=0, filter="arp", store=0, prn=processPacket)
