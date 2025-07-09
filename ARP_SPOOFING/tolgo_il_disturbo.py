# Importiamo le funzioni necessarie da Scapy
from scapy.all import ARP, send

# Funzione per ripristinare le tabelle ARP (mitigazione post spoofing)
def tolgo_il_disturbo():
    # Ripristiniamo la tabella ARP del router
    # Creiamo un oggetto ARP per ripristinare la voce corretta nella cache ARP del router
    risposta_arp = ARP()
    
    # Definiamo il tipo di operazione ARP (2 = "risposta ARP")
    risposta_arp.op = 2
    
    # Impostiamo l'indirizzo IP del router come destinazione
    risposta_arp.pdst = "192.168.176.2"  # IP del router
    
    # Impostiamo l'indirizzo MAC del router
    risposta_arp.hwdst = "00:50:56:ec:86:d6"  # MAC del router
    
    # Impostiamo il MAC corretto della vittima, per ripristinare la sua voce nella tabella ARP
    risposta_arp.hwsrc = "00:0c:29:27:17:b1"  # MAC della vittima
    
    # Impostiamo l'indirizzo IP della vittima
    risposta_arp.psrc = "192.168.176.128"  # IP della vittima
    
    # Inviamo il pacchetto ARP al router per ripristinare la tabella
    send(risposta_arp)
    
    # Ripristiniamo la tabella ARP di Windows (vittima)
    # Creiamo un altro pacchetto ARP per ripristinare la voce ARP della macchina Windows
    risposta_arp = ARP()
    
    # Definiamo il tipo di operazione ARP (2 = "risposta ARP")
    risposta_arp.op = 2
    
    # Impostiamo l'indirizzo IP della vittima (Windows) come destinazione
    risposta_arp.pdst = "192.168.176.128"  # IP della vittima Windows
    
    # Impostiamo l'indirizzo MAC della vittima
    risposta_arp.hwdst = "00:0c:29:27:17:b1"  # MAC della vittima
    
    # Impostiamo il MAC del router per ripristinare la voce corretta nella cache ARP di Windows
    risposta_arp.hwsrc = "00:50:56:ec:86:d6"  # MAC del router
    
    # Impostiamo l'indirizzo IP del router
    risposta_arp.psrc = "192.168.176.2"  # IP del router
    
    # Inviamo il pacchetto ARP alla vittima per ripristinare la tabella
    send(risposta_arp)

# Se il programma viene interrotto manualmente (Ctrl + C), gestiamo l'evento
try:
    # Simuliamo l'esecuzione principale, ad esempio, eseguire lo spoofing o altre operazioni
    while True:
        # (codice principale, per esempio spoofing in corso)
        pass  # Qui ci sarebbe il codice attivo che vogliamo eseguire
except KeyboardInterrupt as err:
    # Se si verifica un'interruzione da tastiera, chiamiamo la funzione per ripristinare le tabelle ARP
    tolgo_il_disturbo()
    print("Uscita, tabelle ARP ripristinate.")




