from scapy.all import *
from file_save import fileSave
import time
from pyexcelerate import Workbook
import pyshark
import asyncio
from datetime import datetime
from datetime import timedelta

counter = 0
count = 0
isEmpty = True
length = 0 

def process_pcap_file(file,template_data):
    global counter,count
    count = 0
    inputTargetPath,outputFilePath = fileSave(file)
    pcap_file = inputTargetPath
    
    wireshark_query = wireShark_Query(template_data)
    
    start_time = time.time()  # İşlem başlangıç zamanı
    # Paketleri inceleme
    dataListExcel = main(pcap_file, wireshark_query, template_data["protocolType"])
    end_time = time.time()
    write_excel(dataListExcel,outputFilePath)

    end_time_excel = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_excel = end_time_excel - start_time
    
    print(f"Paket sayısı: {count}")
    print(f"İşlem {elapsed_time} saniye sürdü.")
    print(f"İşlem excel ile {elapsed_time_excel} saniye sürdü.")
    dataListExcel.clear()
    return outputFilePath       
                                
                                
def main(pcap_file, wireshark_query,protocol):
    loop = asyncio.new_event_loop()
    first_frame_to = pyshark.FileCapture(pcap_file, use_json=True, include_raw=True, eventloop=loop, only_summaries=True)
    first_frame_time = first_frame_to[0].sniff_time
    pcap_file = pyshark.FileCapture(pcap_file, use_json=True, include_raw=True, eventloop=loop, only_summaries=True,display_filter = wireshark_query)
    
    global count
    dataListExcel = []
    for packet in pcap_file:
        count += 1
        if protocol in packet:
            payload = getattr(packet, protocol).payload
            srcIp = packet.ip.src
            dstIp = packet.ip.dst
            timestamp = packet.sniff_time - first_frame_time
            payload = payload.replace(":", "")
            dataListExcel.append([timestamp.total_seconds(), srcIp, dstIp, payload])
            
    pcap_file.close()
    return dataListExcel
            
            
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
        wireshark_query.append(f"{protocol}.length > 0") # Bunları udp ve tcp wireshark querysi farklı olduğu için ikiye ayırdık.
    elif protocol == 'tcp':
        wireshark_query.append(f"{protocol}.len > 0")
    
    return " && ".join(filter(None, wireshark_query))
    
        
def write_excel(data,outputFilePath):
     # Workbook oluştur
    wb = Workbook()
    # Başlıkları ekle
    headers = ["Time", "SourceIP", "DestIP", "Data"]
    sheet_data = [headers] + data
    
    ws = wb.new_sheet("Sheet1",data=sheet_data)
    # Dosyayı kaydet
    wb.save(outputFilePath)