import socket
from nsip import *  

# mapeando os de códigos de consulta para criar descrições
QUERY_DESCRIPTIONS = {
    SYS_PROCNUM: "Número de processos em execução",
    SYS_BOOTIME: "Tempo desde a inicialização do servidor",
    CPU_COUNT: "Número de CPUs do servidor",
    CPU_PERCT: "Percentual de uso da CPU",
    CPU_STATS: "Estatísticas da CPU (trocas de contexto e interrupções)",
    MEM_TOTAL: "Memória total do servidor",
    MEM_FREE: "Memória disponível no servidor",
    MEM_PERCT: "Porcentagem de uso da memória",
    DISK_PARTS: "Partições do disco",
    DISK_USAGE: "Uso das partições do disco",
    NET_IFACES: "Interfaces de rede do servidor",
    NET_IPS: "IPs das interfaces de rede",
    NET_MACS: "MACs das interfaces de rede",
    NET_TXBYTES: "Bytes enviados pela rede",
    NET_RXBYTES: "Bytes recebidos pela rede",
    NET_TXPACKS: "Pacotes enviados pela rede",
    NET_RXPACKS: "Pacotes recebidos pela rede",
    NET_TCPCONS: "Quantidade de portas TCP ouvindo conexões",
    NET_TCPLIST: "Lista de portas TCP ouvindo conexões",
    NET_UDPCONS: "Quantidade de portas UDP ouvindo conexões",
    NET_UDPLIST: "Lista de portas UDP ouvindo conexões"
}

def run_client():
    server_address = ('localhost', 2102)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # timeout para evitar travamentos

    try:
        query = int(input("Digite o código da consulta (ex: 0 para SYS_PROCNUM): "))
        if query not in QUERY_DESCRIPTIONS:
            print("Erro: Código de consulta inválido.")
            return

        # aqui cria o pacote de requisição
        packet = NSIPPacket(id=1, type=NSIP_REQ, query=query, result="")
        packet.checksum = checksum(packet.to_packet())

        # envia a requisição
        sock.sendto(packet.to_packet(), server_address)

        # recebe a resposta
        data, _ = sock.recvfrom(4096)
        response_packet = NSIPPacket()
        response_packet.from_packet(data)

        # verifica o checksum
        if response_packet.checksum != checksum(data):
            print("Erro: Checksum inválido.")
            return

        if response_packet.type == NSIP_REP:
            description = QUERY_DESCRIPTIONS.get(response_packet.query, "Consulta desconhecida")
            print(f"{description}: {response_packet.result}")
        elif response_packet.type == NSIP_ERR:
            print("Erro no processamento da requisição.")
    except socket.timeout:
        print("Erro: Timeout ao aguardar resposta do servidor.")
    except ValueError:
        print("Erro: Entrada inválida para o código de consulta.")
    finally:
        sock.close()

if __name__ == "__main__":
    run_client()
