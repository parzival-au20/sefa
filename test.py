"""import pandas as pd

df = pd.read_excel('dosya_adı.xlsx')

print(df)

# Belirli bir sütunu bastırma
print(df['Sütun_Adı'])

# Belirli bir satırı bastırma
print(df.iloc[0])  # İlk satırı bastırma"""

import asyncio
import pyshark
import time

from scapy.all import *




pcap_file = r'C:\Users\TAI\Desktop\Myapp -temp\uploads\wrccdc-mss-msctrl-cap.pcap'
# import pyshark
# cap = pyshark.FileCapture('C:\\Users\\D65229\\Desktop\\Myapp\\uploads\\wrccdc-mss-msctrl-cap.pcap')
# cap
# print(cap[0])

# cap = pyshark.FileCapture('C:\\Users\\D65229\\Desktop\\Myapp\\uploads\\wrccdc-mss-msctrl-cap.pcap')


#loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
start_time = time.time() # İşlem başlangıç zamanı
# cap = pyshark.FileCapture(pcap_file,use_json=True, include_raw=True, display_filter='ip.src == 10.100.204.145')

def readPcap():
    cap = pyshark.FileCapture(pcap_file,use_json=True, include_raw=True, only_summaries=True, display_filter='ip.src == 192.168.220.60 && tcp.len>0 ')
    
    file_write = ''
    for packet in PcapReader(pcap_file):
    # Paket bilgilerini dosyaya yaz
        #raw_data = packet.get_raw_packet()

        print(packet)
        """print(packet.ip.src)
        print(packet.ip.dst)
        print(packet.tcp.port)"""
        """print(packet.get_raw_packet().hex())
        break"""
        """with open('packet_info.txt', 'a') as file:
            file.write(packet)"""

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"İşlem {elapsed_time} saniye sürdü.")
    
readPcap()