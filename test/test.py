import asyncio
import pyshark
import time




pcap_file = 'C:\\Users\\D65229\\Desktop\\Myapp\\uploads\\wrccdc-mss-msctrl-cap.pcap'
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
    cap = pyshark.FileCapture(pcap_file,use_json=True, include_raw=True, only_summaries=True, display_filter='ip.src == 10.100.204.145')
    
    file_write = ''
    for packet in cap:
    # Paket bilgilerini dosyaya yaz
        raw_data = packet.get_raw_packet()

        file_write += raw_data.hex()+'\n'
        """print(packet.ip.src)
        print(packet.ip.dst)
        print(packet.tcp.port)"""
        """print(packet.get_raw_packet().hex())
        break"""
    with open('packet_info.txt', 'a') as file:
        file.write(file_write)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"İşlem {elapsed_time} saniye sürdü.")
    
readPcap()




# async def create_tasks_func():
#     tasks = []
#     tasks.append(asyncio.create_task(readPcap()))


# loop.run_until_complete(create_tasks_func())
# loop.close()

# if isinstance(loop, asyncio.ProactorEventLoop):
#         print(True)
