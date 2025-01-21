# Questão 1
from scapy.all import rdpcap

def analisar_captura1(arquivo_pcap):
    packets = rdpcap(arquivo_pcap)

    # Exibir o número de pacotes capturados
    print(f"Número de pacotes capturados: {len(packets)}")

    # Resumo dos pacotes capturados
    print("Resumo dos pacotes:")
    for packet in packets:
        print(packet.summary())

    # Exibir endereços de origem e destino
    for i, packet in enumerate(packets):
        if packet.haslayer("IP"):
            print(f"Pacote {i+1}:")
            print(f"  Origem: {packet['IP'].src}")
            print(f"  Destino: {packet['IP'].dst}")

# Exemplo de execução
# analisar_captura1("captura1.pcap")

# Questão 2
def analisar_captura2(arquivo_pcap):
    packets = rdpcap(arquivo_pcap)

    # Resumo geral do tráfego
    print("Resumo do tráfego:")
    for packet in packets:
        print(packet.summary())

    # Contar tipos de pacotes
    from collections import Counter
    tipos = Counter([type(packet) for packet in packets])
    print("\nEstatísticas de tipos de pacotes:")
    for tipo, count in tipos.items():
        print(f"{tipo.__name__}: {count} pacotes")

# Exemplo de execução
# analisar_captura2("captura2.pcap")

# Questão 3
def analisar_captura3(arquivo_pcap1, arquivo_pcap2):
    packets1 = rdpcap(arquivo_pcap1)
    packets2 = rdpcap(arquivo_pcap2)

    def estatisticas_por_captura(packets):
        src_ips = Counter()
        dst_ips = Counter()
        src_ports = Counter()
        dst_ports = Counter()

        for packet in packets:
            if packet.haslayer("IP"):
                src_ips[packet['IP'].src] += 1
                dst_ips[packet['IP'].dst] += 1
            if packet.haslayer("TCP") or packet.haslayer("UDP"):
                src_ports[packet.sport] += 1
                dst_ports[packet.dport] += 1

        return src_ips, dst_ips, src_ports, dst_ports

    # Estatísticas da primeira captura
    src_ips1, dst_ips1, src_ports1, dst_ports1 = estatisticas_por_captura(packets1)
    print("Estatísticas para a primeira captura:")
    print("IPs de origem:")
    for ip, count in src_ips1.items():
        print(f"{ip}: {count}")
    print("IPs de destino:")
    for ip, count in dst_ips1.items():
        print(f"{ip}: {count}")

    # Estatísticas da segunda captura
    src_ips2, dst_ips2, src_ports2, dst_ports2 = estatisticas_por_captura(packets2)
    print("\nEstatísticas para a segunda captura:")
    print("IPs de origem:")
    for ip, count in src_ips2.items():
        print(f"{ip}: {count}")
    print("IPs de destino:")
    for ip, count in dst_ips2.items():
        print(f"{ip}: {count}")

    # Comparação NAT
    print("\nComparação NAT:")
    print(f"IP de origem antes do NAT: {list(src_ips1.keys())}")
    print(f"IP de origem depois do NAT: {list(src_ips2.keys())}")
    print(f"Portas de origem antes do NAT: {list(src_ports1.keys())}")
    print(f"Portas de origem depois do NAT: {list(src_ports2.keys())}")

# Exemplo de execução
# analisar_captura3("captura3-1.pcap", "captura3-2.pcap")
