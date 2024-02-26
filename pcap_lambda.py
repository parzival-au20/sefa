from scapy.all import *
import time


packets = PcapReader(r'C:\Users\TAI\Desktop\Myapp -temp\uploads\wrccdc-mss-msctrl-cap.pcap')

# Filtreleme yaparak istediğiniz paketleri seç
#♫filtered_packets = packets.filter(lambda x: x.haslayer('TCP') and (x['TCP'].sport == 50070 and x['TCP'].dport == 1514))
start_time = time.time()
#filtered_packets = (pkt for pkt in packets if pkt.haslayer('TCP') and (pkt['TCP'].sport == 50070 or pkt['TCP'].dport == 1514))

filtered_packets = (pkt for pkt in packets if pkt.haslayer('IP') and pkt.haslayer('TCP') and
                    pkt['IP'].src == '10.100.204.145' and len(pkt['TCP'].payload) > 0)

end_time = time.time()
print(f"işlem1 ${end_time-start_time}saniye sürdü")
i=0
# Seçilen paketleri göster
start_time = time.time()
for packet in filtered_packets:
    i+=1
    #print(packet.summary())
end_time = time.time()
print(f"işlem2 ${end_time-start_time}saniye sürdü")
print(i,"paket okundu")