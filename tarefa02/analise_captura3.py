from scapy.all import rdpcap

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

    # estatísticas da primeira captura
    src_ips1, dst_ips1, src_ports1, dst_ports1 = estatisticas_por_captura(packets1)
    print("Estatísticas para a primeira captura:")
    print("IPs de origem:")
    for ip, count in src_ips1.items():
        print(f"{ip}: {count}")
    print("IPs de destino:")
    for ip, count in dst_ips1.items():
        print(f"{ip}: {count}")

    #estatísticas da segunda captura
    src_ips2, dst_ips2, src_ports2, dst_ports2 = estatisticas_por_captura(packets2)
    print("\nEstatísticas para a segunda captura:")
    print("IPs de origem:")
    for ip, count in src_ips2.items():
        print(f"{ip}: {count}")
    print("IPs de destino:")
    for ip, count in dst_ips2.items():
        print(f"{ip}: {count}")

    #comparação NAT
    print("\nComparação NAT:")
    print(f"IP de origem antes do NAT: {list(src_ips1.keys())}")
    print(f"IP de origem depois do NAT: {list(src_ips2.keys())}")
    print(f"Portas de origem antes do NAT: {list(src_ports1.keys())}")
    print(f"Portas de origem depois do NAT: {list(src_ports2.keys())}")

#execução
analisar_captura3("captura3-1.pcap", "captura3-2.pcap")