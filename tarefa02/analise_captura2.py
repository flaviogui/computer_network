from scapy.all import rdpcap

def analisar_captura2(arquivo_pcap):
    packets = rdpcap(arquivo_pcap)

    # resumo do tráfego
    print("Resumo do tráfego:")
    for packet in packets:
        print(packet.summary())

    # contar tipos de pacotes
    from collections import Counter
    tipos = Counter([type(packet) for packet in packets])
    print("\nEstatísticas de tipos de pacotes:")
    for tipo, count in tipos.items():
        print(f"{tipo.__name__}: {count} pacotes")

# execução
analisar_captura2("captura2.pcap")