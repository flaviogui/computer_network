from scapy.all import rdpcap

def analisar_captura1(arquivo_pcap):
    packets = rdpcap(arquivo_pcap)

    # exibir o número de pacotes capturados
    print(f"Número de pacotes capturados: {len(packets)}")

    # mostra o resumo dos pacotes capturados
    print("Resumo dos pacotes:")
    for packet in packets:
        print(packet.summary())

    # exibir endereços de origem e destino
    for i, packet in enumerate(packets):
        if packet.haslayer("IP"):
            print(f"Pacote {i+1}:")
            print(f"  Origem: {packet['IP'].src}")
            print(f"  Destino: {packet['IP'].dst}")

# execução
analisar_captura1("captura1.pcap")
