from scapy.all import *
from file_save import fileSave
import time
from pyexcelerate import Workbook


counter = 0
count = 0
isEmpty = True
dataListExcel = []

def process_pcap_file(file,template_data):
    global counter,count
    global isEmpty
    counter = 0
    count = 0
    inputTargetPath,outputFilePath = fileSave(file)
    pcap_file = inputTargetPath
 
    #case function belirleme 
    control_str = ["0", "0", "0", "0"]  # Kontrol listesi

    # İlgili key'ler için kontrol yapma
    for idx, key in enumerate(['sourceIp','sourcePort' , 'destinationIp', 'destinationPort'], start=0):
        value = template_data.get(key)
        if value:  # Eğer değer boş değilse
            control_str[idx] = "1"  # Kontrol listesine değeri işaretleme

    case_function = control_case("".join(control_str))

    
    start_time = time.time()  # İşlem başlangıç zamanı
    
    # Paketleri inceleme
    first_time_counter = 0
    for packet in PcapReader(pcap_file):
            counter+=1
            source_ip = None
            destination_ip = None
            protocol = None
            source_port = None
            destination_port = None
            
            if(first_time_counter == 0):
                first_packet_time = packet.time
                first_time_counter+=1
            # Paket verilerini işleme
            #if(counter<100):
            if packet.haslayer('Raw'):
                raw_data = packet.getlayer('Raw').load
            else:
                continue
            # Raw verileri işleme
            if packet.haslayer('IP'):
                ip_packet = packet['IP']
                # IP adreslerini al
                source_ip = ip_packet.src
                destination_ip = ip_packet.dst
    
                # Protokol bilgisini al
                protocol = template_data['protocolType']
                
                # Kaynak ve hedef port bilgilerini al
                if packet.haslayer(protocol):  # Eğer UDPya da TCP var ise
                    protocol_packet = ip_packet[protocol]
                    source_port = protocol_packet.sport
                    destination_port = protocol_packet.dport
                        
            packet_data = {
                'sourceIp': source_ip,
                'destinationIp': destination_ip,
                'sourcePort': str(source_port),
                'destinationPort': str(destination_port)
                }
                
            result = case_function(template_data, packet_data)
            if(result):
                count+=1
                #print(str(counter)+" ------Packet started--------"+str(count)+"\n\n")
                dataListExcel.append([counter, packet.time - first_packet_time, source_ip, destination_ip, raw_data.hex()])
                isEmpty = False
                
                
    end_time = time.time()                                       
    if(isEmpty):
        with io.open(outputFilePath, "a", encoding="utf-8") as file:
            file.write("Hiçbir eşleşme bulunamadı\n")
    write_excel(dataListExcel,outputFilePath)
                    
    end_time_excel = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_excel = end_time_excel - start_time
    print(f"İşlem {count} paket döndü hepsini okudu")
    print(f"İşlem {elapsed_time} saniye sürdü.")
    print(f"İşlem Excel ile {elapsed_time_excel} saniye sürdü.")
    dataListExcel.clear()
    return outputFilePath
 

def control_case(control_str):
    if(control_str=="1010"):  #src_ip - dst_ip
        return case1
    if(control_str=="1100"):  #src_ip - src_port
        return case2
    if(control_str=="0011"):  #dst_ip - dest_port
        return case3
    if(control_str=="1111"):  #src_ip and src_port - dst_ip and dst_port
        return case4
    if(control_str=="1000"):  #src_ip
        return case5
    if(control_str=="0010"):  #dst_ip
        return case6
    
def case1(template_data, packet_data):  #src_ip - dst_ip
    if((template_data['sourceIp']==packet_data['sourceIp'] and template_data['destinationIp']==packet_data['destinationIp'])):
        return True
    
def case2(template_data, packet_data):  #src_ip - src_port
    if((template_data['sourceIp']==packet_data['sourceIp'] and template_data['sourcePort']==packet_data['sourcePort'])):
       return True
        
def case3(template_data, packet_data):  #dst_ip - dest_port
    if((template_data['destinationIp']==packet_data['destinationIp'] and template_data['destinationPort']==packet_data['destinationPort'])):
       return True
    
def case4(template_data, packet_data):  #src_ip and src_port - dst_ip and dst_port
    if((template_data['sourceIp']==packet_data['sourceIp'] and template_data['sourcePort']==packet_data['sourcePort']) and (template_data['destinationIp']==packet_data['destinationIp'] and template_data['destinationPort']==packet_data['destinationPort'])): # burada tüm alanlar doluysa bu condition kullan
        return True
        
def case5(template_data, packet_data):  #src_ip 
    if(template_data['sourceIp']==packet_data['sourceIp'] ):
        return  True
        
def case6(template_data, packet_data):  #dst_ip
    if(template_data['destinationIp']==packet_data['destinationIp']):
        return True

def write_excel(data,outputFilePath):
     # Workbook oluştur
    wb = Workbook()
    # Başlıkları ekle
    headers = ["Time", "SourceIP", "DestIP", "Data"]
    sheet_data = [headers] + data
    
    ws = wb.new_sheet("Sheet1",data=sheet_data)
    
    # Dosyayı kaydet
    wb.save(outputFilePath)