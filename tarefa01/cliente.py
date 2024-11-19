import socket
from nsip import *  

def run_client():
    server_address = ('localhost', 2102)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # timeout para evitar travamentos

    try:
        query = int(input("Digite o código da consulta (ex: 0 para SYS_PROCNUM): "))
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
            print(f"Resposta do servidor: {response_packet.result}")
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
