import socket
import threading

HOST = '0.0.0.0'
PORT = 44444
BUFFER_SIZE = 1024
PASSWORD = "password123"   

def handle_client(conn, addr):
   
    with conn:
        print(f"Connessione stabilita con {addr}")
        conn.sendall(b"Benvenuto! Inserisci la password:\n")
        pwd = conn.recv(BUFFER_SIZE).decode('utf-8').strip()

        if pwd != PASSWORD:
            conn.sendall(b" Accesso negato.\n")
            print(f" {addr} ha inserito una password errata.")
            return
        else:
            conn.sendall(b" Accesso consentito! Ora puoi inviare messaggi.\n")
            print(f"{addr} autenticato con successo.")

     
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                print(f"❎ {addr} si e' disconnesso.")
                break
            message = data.decode('utf-8').strip()
            print(f" Da {addr}: {message}")
            conn.sendall(b"Messaggio ricevuto!\n")

def start_server():
   
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server avviato su {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            # Crea un thread per ogni client
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"🧵 Thread avviato per {addr} ({thread.name})")

if __name__ == "__main__":
    start_server()
