import socket
import psutil
from nsip import *  

def process_query(query):
    """
    Processa a consulta e retorna o resultado apropriado
    """
    try:
        if query == SYS_PROCNUM:
            return str(len(psutil.pids()))  # número de processos em execução
        elif query == SYS_BOOTIME:
            return str(psutil.boot_time())  # tempo de inicialização do servidor
        elif query == CPU_COUNT:
            return str(psutil.cpu_count())  # número de CPUs
        elif query == CPU_PERCT:
            return str(psutil.cpu_percent(interval=1))  # percentual de uso da CPU
        elif query == CPU_STATS:
            stats = psutil.cpu_stats()
            return f"{stats.ctx_switches},{stats.interrupts}"  # trocas de contexto, interrupções
        elif query == MEM_TOTAL:
            return str(psutil.virtual_memory().total)  # memória total
        elif query == MEM_FREE:
            return str(psutil.virtual_memory().available)  # memória disponível
        elif query == MEM_PERCT:
            return str(psutil.virtual_memory().percent)  # porcentagem de uso da memória
        elif query == DISK_PARTS:
            parts = psutil.disk_partitions()
            return ",".join([p.mountpoint for p in parts])  # lista de partições
        elif query == DISK_USAGE:
            usages = psutil.disk_partitions()
            return ",".join([str(psutil.disk_usage(p.mountpoint).percent) for p in usages])  # Uso das partições
        elif query == NET_IFACES:
            return ",".join(psutil.net_if_addrs().keys())  # lista de interfaces de rede
        elif query == NET_IPS:
            return ",".join([
                addr.address for iface in psutil.net_if_addrs().values()
                for addr in iface if addr.family == socket.AF_INET
            ])  # lista de IPs
        elif query == NET_MACS:
            return ",".join([
                addr.address for iface in psutil.net_if_addrs().values()
                for addr in iface if addr.family == psutil.AF_LINK
            ])  # lista de MACs
        elif query == NET_TXBYTES:
            return str(psutil.net_io_counters().bytes_sent)  # Bytes enviados
        elif query == NET_RXBYTES:
            return str(psutil.net_io_counters().bytes_recv)  # Bytes recebidos
        elif query == NET_TXPACKS:
            return str(psutil.net_io_counters().packets_sent)  # Pacotes enviados
        elif query == NET_RXPACKS:
            return str(psutil.net_io_counters().packets_recv)  # Pacotes recebidos
        elif query == NET_TCPCONS:
            return str(len(psutil.net_connections(kind="tcp")))  # Conexões TCP
        elif query == NET_TCPLIST:
            return ",".join([str(c.laddr.port) for c in psutil.net_connections(kind="tcp")])  # Portas TCP
        elif query == NET_UDPCONS:
            return str(len(psutil.net_connections(kind="udp")))  # Conexões UDP
        elif query == NET_UDPLIST:
            return ",".join([str(c.laddr.port) for c in psutil.net_connections(kind="udp")])  # Portas UDP
        else:
            return None  # Consulta não suportada
    except Exception as e:
        return f"Erro: {str(e)}"

def run_server():
    server_address = ('', 2102)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    print("Servidor aguardando requisições na porta 2102...")

    while True:
        data, address = sock.recvfrom(4096)
        packet = NSIPPacket()
        packet.from_packet(data)

        # Verifica o checksum
        if packet.checksum != checksum(data):
            response_packet = NSIPPacket(id=packet.id, type=NSIP_ERR, query=packet.query, result="Checksum inválido")
            sock.sendto(response_packet.to_packet(), address)
            continue

        if packet.type == NSIP_REQ:
            query = packet.query
            result = process_query(query)

            if result is not None:
                # Cria a resposta
                response_packet = NSIPPacket(id=packet.id, type=NSIP_REP, query=query, result=result)
            else:
                # Resposta para consulta não suportada
                response_packet = NSIPPacket(id=packet.id, type=NSIP_ERR, query=query, result="Consulta não suportada")
            
            response_packet.checksum = checksum(response_packet.to_packet())
            sock.sendto(response_packet.to_packet(), address)

if __name__ == "__main__":
    run_server()
