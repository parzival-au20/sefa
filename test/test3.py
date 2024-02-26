import pyshark
import concurrent.futures
import threading
import time
import asyncio

def process_packet(packet):
    raw_data = packet.get_raw_packet()
    return raw_data.hex() + '\n'

def process_packets(pcap_file):
    loop = asyncio.new_event_loop()
    with pyshark.FileCapture(pcap_file, use_json=True, include_raw=True, only_summaries=True, eventloop=loop) as cap:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_packet, packet) for packet in cap]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            with open('packet_info.txt', 'a') as file:
                file.writelines(results)

def main(pcap_file):
    start_time = time.time()
    # Örneğin, 4 iş parçacığı oluşturup işlemleri paralel yürütebilirsiniz
    threads = []
    for i in range(10):
        thread = threading.Thread(target=process_packets, args=(pcap_file,))
        threads.append(thread)
        thread.start()

    # Tüm iş parçacıklarının tamamlanmasını bekleyin
    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"İşlem {elapsed_time} saniye sürdü.")

if __name__ == "__main__":
    pcap_file = 'C:\\Users\\D65229\\Desktop\\Myapp\\uploads\\wrccdc-mss-msctrl-cap.pcap'
    main(pcap_file)
