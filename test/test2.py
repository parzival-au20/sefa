import pyshark
import concurrent.futures
import time

def process_packet(packet):
    """if 'UDP' in packet:
        udp_payload = packet.udp.payload
        if udp_payload:
            hex_data = udp_payload.replace(':', '')  # Eğer gerekiyorsa ":" karakterlerini kaldırabilirsiniz
            print(f"UDP Payload in Hex: {hex_data}")
    
    # TCP paketini kontrol etme
    if 'TCP' in packet:
        tcp_payload = packet.tcp.payload
        if tcp_payload:
            hex_data = tcp_payload.replace(':', '')  # Eğer gerekiyorsa ":" karakterlerini kaldırabilirsiniz
            print(f"TCP Payload in Hex: {hex_data}")"""
    raw_data = packet.get_raw_packet()
    print(raw_data)
    return raw_data.hex() + '\n'

def main(pcap_file):
    with pyshark.FileCapture(pcap_file, use_json=True, include_raw=True, only_summaries=True, display_filter='ip.src == 10.100.204.145') as cap:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_packet, packet) for packet in cap]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            with open('packet_info.txt', 'a') as file:
                file.writelines(results)

if __name__ == "__main__":
    pcap_file = 'C:\\Users\\D65229\\Desktop\\Myapp\\uploads\\wrccdc-mss-msctrl-cap.pcap'
    start_time = time.time()
    main(pcap_file)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"İşlem {elapsed_time} saniye sürdü.")
    
