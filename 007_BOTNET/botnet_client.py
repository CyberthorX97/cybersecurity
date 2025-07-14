#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importazione dei moduli necessari
import socket     # modulo per la comunicazione di rete TCP/IP
import sys        # modulo per l'accesso agli argomenti della riga di comando

# Funzione principale che gestisce la connessione client-server
def start_client(server_ip: str, server_port: int) -> None:
    try:
        # Crea un socket TCP (SOCK_STREAM) su IPv4 (AF_INET) usando il context manager 'with'
        # In questo modo il socket verrà chiuso automaticamente al termine del blocco
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print(f"Tentativo di connessione a {server_ip} porta {server_port}...")
            
            # Connessione al server specificato
            sock.connect((server_ip, server_port))
            print("Connessione stabilita.")

            # Loop principale per l'interazione utente-server
            while True:
                # Chiede all'utente di inserire un messaggio da inviare al server
                message = input("Inserisci un messaggio (può contenere più parole, 'exit' per uscire): ")

                # Se l'utente scrive 'exit', si esce dal ciclo e il socket verrà chiuso
                if message.lower() == 'exit':
                    break

                # Invia il messaggio codificato in byte (UTF-8) al server
                sock.sendall(message.encode('utf-8'))

                # Attende la risposta dal server
                # recv(4096) legge fino a 4096 byte (può essere meno se la risposta è breve)
                response_data = sock.recv(4096)

                # Se non riceviamo nulla, significa che il server ha chiuso la connessione
                if not response_data:
                    print("La connessione è stata chiusa dal server.")
                    break

                # Decodifica i byte ricevuti e li stampa come stringa
                print(f"Risposta dal server: {response_data.decode('utf-8')}")

    # Gestione degli errori comuni durante la connessione
    except ConnectionRefusedError:
        print(f"Errore: Connessione rifiutata. Assicurati che il server sia in ascolto su {server_ip}:{server_port}.")
    except socket.gaierror:
        print(f"Errore: L'indirizzo IP '{server_ip}' non è valido o non risolvibile.")
    except socket.error as e:
        print(f"Errore del socket: {e}")
    except KeyboardInterrupt:
        # Permette di interrompere il client con CTRL+C
        print("\nClient interrotto dall'utente.")
    finally:
        # Questo messaggio viene sempre stampato alla fine, qualunque sia l'esito
        print("Client terminato.")


# Funzione eseguita all'avvio del programma
def main():
    # Controlla che il numero di argomenti passati da linea di comando sia corretto
    # Deve ricevere esattamente 2 argomenti: IP e porta
    if len(sys.argv) != 3:
        print(f"Uso: python {sys.argv[0]} <indirizzo_ip_server> <porta_server>")
        sys.exit(1)

    # Estrae i parametri dalla riga di comando
    server_ip = sys.argv[1]
    
    try:
        # Converte la porta da stringa a intero e controlla che sia valida (1-65535)
        server_port = int(sys.argv[2])
        if not 0 < server_port < 65536:
            raise ValueError
    except ValueError:
        print("Errore: La porta deve essere un numero intero tra 1 e 65535.")
        sys.exit(1)

    # Avvia il client con i parametri ricevuti
    start_client(server_ip, server_port)


# Punto d'ingresso del programma: esegue main() solo se lo script è eseguito direttamente
if __name__ == "__main__":
    main()
