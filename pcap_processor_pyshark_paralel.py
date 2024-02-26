from scapy.all import *
from file_save import fileSave
import time
from pyexcelerate import Workbook
import concurrent.futures
import pyshark
import asyncio

counter = 0
count = 0
isEmpty = True


def process_pcap_file(file,template_data):
    global counter,count
    count = 0
    inputTargetPath,outputFilePath = fileSave(file)
    pcap_file = inputTargetPath
    
    wireshark_query = wireShark_Query(template_data)
    
    start_time = time.time()  # İşlem başlangıç zamanı
    # Paketleri inceleme
    dataListExcel = make_parallel(pcap_file, wireshark_query, template_data["protocolType"])
    end_time = time.time()
    dataListExcel = sorted(dataListExcel, key=lambda index : index[0]) #Datalar paralel processing ile eklendiği için time stamp'e göre sort et.
    end_time_sorted = time.time()
    write_excel(dataListExcel,outputFilePath)
    len(dataListExcel)
    end_time_excel = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_excel = end_time_excel - start_time
    elapsed_time_sorted = end_time_sorted - start_time
    print(f"Paket sayısı: {count}")
    print(f"İşlem {elapsed_time} saniye sürdü.")
    print(f"İşlem sorted ile {elapsed_time_sorted} saniye sürdü.")
    print(f"İşlem excel ile {elapsed_time_excel} saniye sürdü.")
    dataListExcel.clear()
    return outputFilePath       
                                
 
def process_packet(packet,protocol, first_frame_time):
    global count
    count += 1
    if hasattr(packet, 'sniff_time'):
        timestamp = (packet.sniff_time - first_frame_time).total_seconds()
  
    if protocol in packet:
            payload = getattr(packet, protocol).payload  #TCP ya da UDP 'ye göre payloadını excele ekle.
            payload = payload.replace(":", "")
            srcIp = packet.ip.src
            dstIp = packet.ip.dst
            return [timestamp, srcIp, dstIp, payload]
    

    return [timestamp,"", "", "", "eşleşme bulunamadı", "", ""]


def make_parallel(pcap_file, wireshark_query, protocol):
    loop = asyncio.new_event_loop()
    first_frame_to = pyshark.FileCapture(pcap_file, use_json=True, include_raw=True, eventloop=loop, only_summaries=True)
    first_frame_time = first_frame_to[0].sniff_time
    
    with pyshark.FileCapture(pcap_file, use_json=True, include_raw=True, only_summaries=True,eventloop=loop, display_filter = wireshark_query) as cap:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_packet, packet, protocol, first_frame_time) for packet in cap]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
    
    return results
            
def wireShark_Query(template_data):
    wireshark_query = []
    
    protocol = template_data['protocolType'].lower()
    
    conditions = {
        'ip.src': template_data['sourceIp'],
        f'{protocol}.srcport': template_data['sourcePort'],
        'ip.dst': template_data['destinationIp'],
        f'{protocol}.dstport': template_data['destinationPort'],
    }
    
    for key, value in conditions.items():
        if value:
            wireshark_query.append(f"{key} == {value}")
    if protocol == 'udp':
        wireshark_query.append(f"{protocol}.length > 0")
    elif protocol == 'tcp':
        wireshark_query.append(f"{protocol}.len > 0")
    
    return " && ".join(filter(None, wireshark_query))
    
        
def write_excel(data,outputFilePath):
     # Workbook oluştur
    wb = Workbook()
    # Başlıkları ekle
    headers = ["TimeStamp", "SourceIP", "DestIP", "Data"]
    sheet_data = [headers] + data
    
    ws = wb.new_sheet("Sheet1",data=sheet_data)
    # Dosyayı kaydet
    wb.save(outputFilePath)