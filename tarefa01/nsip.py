# manipulacao de vetores
# https://docs.python.org/3/library/array.html
import array

# criacao de structs em Python
# https://docs.python.org/3/library/struct.html
import struct

# obtencao das informacoes do sistema
# https://psutil.readthedocs.io/en/latest/
import psutil

# Tipos dos pacotes
NSIP_REQ = 0x0
NSIP_REP = 0x1
NSIP_ERR = 0x2

# Tipos das consultas

# SYSTEM
SYS_PROCNUM = 0x0
SYS_BOOTIME = 0x1
# CPU
CPU_COUNT   = 0x2
CPU_PERCT   = 0x3
CPU_STATS   = 0x4
# MEM
MEM_TOTAL   = 0x5
MEM_FREE    = 0x6
MEM_PERCT   = 0x7
# DISK
DISK_PARTS  = 0x8
DISK_USAGE  = 0x9
# NET
NET_IFACES  = 0x10
NET_IPS     = 0x11
NET_MACS    = 0x12
NET_TXBYTES = 0x13
NET_RXBYTES = 0x14
NET_TXPACKS = 0x15
NET_RXPACKS = 0x16
NET_TCPCONS = 0x17
NET_TCPLIST = 0x18
NET_UDPCONS = 0x19
NET_UDPLIST = 0x20

# Constantes uteis
NSIP_LEN = 54  # tamanho do pacote NSIP em bytes

# calculo do checksum
# OBS:
# - recebe um pacote para ser calculado
# - o calculo do checksum zera os valores do checksum do pacote para nao
# interfereir no calculo
def checksum(packet):
    """
    Calcula a checksum do pacote
    """
    # convertendo em um array de bytes
    a = array.array("B", packet)
    # zerando os valores do checksum (para nao interferir na soma)
    a[2] = a[3] = 0
    # somando todos os valores e calculando o modulo
    res = sum(a) % 2**16
    return res


# classe para o pacote NSIP
class NSIPPacket:

    """
    Classe para o pacote do NSIP
    """
    def __init__(self, id=0, type=0, query=0, result=""):
        self.id = id
        self.type = type
        self.checksum = 0
        self.query = query
        self.result = result

    def to_packet(self):
        """
        Transforma o objeto em um pacote (struct)
        """
        packet = struct.pack(
            "BBHH48s",
            self.id,        # 1  byte
            self.type,      # 1  byte
            self.checksum,  # 2  bytes
            self.query,     # 2  bytes
            self.result.encode("utf-8").ljust(48, b"\0"),    # 48 bytes
        )
        return packet

    def from_packet(self, p):
        """
        Transforma um pacote (struct) no objeto
        """
        self.id = p[0]
        self.type = p[1]
        self.checksum = struct.unpack("H", p[2:4])[0]
        self.query = struct.unpack("H", p[4:6])[0]
        self.result = (struct.unpack("48s", p[6:])[0]).decode("UTF-8")

    def to_string(self):
        """
        Imprime os valores dos atributos
        """
        print("Imprimindo os atributos:")
        print(f"\tid: {self.id}")
        print("\ttype: 0x%x" % self.type)
        print(f"\tchecksum: {self.checksum}")
        print("\tquery: 0x%x" % self.query)
        print(f"\tresult: {self.result}")

    def print(self):
        """
        Imprime o pacote
        """
        p = self.to_packet()

        print("Imprimindo o pacote (struct):")
        print("\tid: %02d" % p[0])
        print("\ttype: 0x%02x" % p[1])
        print("\tchecksum: 0x%04x" % struct.unpack("H", p[2:4]))
        print("\tquery: 0x%04x" % struct.unpack("H", p[4:6])[0])
        print("\tresult: %s" % struct.unpack("48s", p[6:])[0].decode("utf-8"))

#
# OBS.: abaixo estão alguns exemplos de utilizacao da classe NSIP, suas funções
# e constantes
# OBS.: Para criar o cliente.py e servidor.py, é preciso incluir este arquivo:
#       from nsip import *
if __name__ == "__main__":
    # criando um pacote de requisicao
    packet1 = NSIPPacket(3, NSIP_REQ, SYS_PROCNUM, "")
    packet1.checksum = checksum(packet1.to_packet())
    print("Pacote 1:")
    packet1.print()

    # criando um pacote de resposta
    print("Pacote 2:")
    packet2 = NSIPPacket(3, NSIP_REP, SYS_PROCNUM, "")
    packet2.result = str(len(psutil.pids()))
    packet2.checksum = checksum(packet2.to_packet())
    packet2.print()

    # preenchedo a instancia de um pacote a partir de um pacote (struct) recebido
    packet3 = NSIPPacket()
    packet3.from_packet(packet2.to_packet())
    print("Pacote 3 (Construido do Pacote 2)")
    packet3.print()

    # enviando um pacote pela rede
    # s.sendto(packet3.to_packet(), (IP, PORTA))
