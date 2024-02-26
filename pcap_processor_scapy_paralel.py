from scapy.all import *
from file_save import fileSave
import time
from pyexcelerate import Workbook
import concurrent.futures

counter = 0
count = 0
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
    
    read_scapy = PcapReader(pcap_file)
    
    # Paketleri inceleme
    dataListExcel = make_parallel(read_scapy, template_data, case_function)
    
    dataListExcel = sorted(dataListExcel, key=lambda index : index[0]) #Datalar paralel processing ile eklendiği için time stamp'e göre sort et.
    
    end_time = time.time()                                       
    write_excel(dataListExcel,outputFilePath)
                    
    end_time_excel = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_excel = end_time_excel - start_time
    print(f"İşlem {count} paket döndü hepsini okudu")
    print(f"İşlem {elapsed_time} saniye sürdü.")
    print(f"İşlem Excel ile {elapsed_time_excel} saniye sürdü.")
    dataListExcel.clear()
    return outputFilePath
 
 
def make_parallel(pcap_file, template_data, case_function):
    for packet in PcapReader(pcap_file):
        first_frame_time = packet.time
        break
    with pcap_file  as cap:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_packet, packet, template_data, case_function, first_frame_time) for packet in cap]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            # print(results)
             
    clean_results = [result for result in results if result and any(result)]  #none gelen ve boş listeleri temizle
    return clean_results
            
def process_packet(packet, template_data, case_function, first_frame_time):
    global counter,count
    counter+=1
    source_ip = None
    destination_ip = None
    protocol = None
    source_port = None
    destination_port = None
    
    # Paket verilerini işleme
    if packet.haslayer('Raw'):
        raw_data = packet.getlayer('Raw').load
    else:
        return
    
    if packet.haslayer('IP'):
        ip_packet = packet['IP']
        # IP adreslerini al
        source_ip = ip_packet.src
        destination_ip = ip_packet.dst
        
        #User Protokol bilgisini al
        protocol = template_data['protocolType']
        
        # Kaynak ve hedef port bilgilerini al
        if packet.haslayer(protocol):  # Eğer UDP ya da TCP ise
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
        return [(packet.time - first_frame_time).total_seconds(), source_ip, destination_ip,raw_data.hex()]
    
    else:
        return []

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
    return False
    
def case2(template_data, packet_data):  #src_ip - src_port
    if((template_data['sourceIp']==packet_data['sourceIp'] and template_data['sourcePort']==packet_data['sourcePort'])):
       return True
    return False
def case3(template_data, packet_data):  #dst_ip - dest_port
    if((template_data['destinationIp']==packet_data['destinationIp'] and template_data['destinationPort']==packet_data['destinationPort'])):
       return True
    return False
def case4(template_data, packet_data):  #src_ip and src_port - dst_ip and dst_port
    if((template_data['sourceIp']==packet_data['sourceIp'] and template_data['sourcePort']==packet_data['sourcePort']) and (template_data['destinationIp']==packet_data['destinationIp'] and template_data['destinationPort']==packet_data['destinationPort'])): # burada tüm alanlar doluysa bu condition kullan
        return True
    return False 
def case5(template_data, packet_data):  #src_ip 
    if(template_data['sourceIp']==packet_data['sourceIp'] ):
        return  True
    return False 
def case6(template_data, packet_data):  #dst_ip
    if(template_data['destinationIp']==packet_data['destinationIp']):
        return True
    return False
def write_excel(data,outputFilePath):
     # Workbook oluştur
    wb = Workbook()
    # Başlıkları ekle
    headers = ["Time", "SourceIP", "DestIP", "Data"]
    sheet_data = [headers] + data
    
    ws = wb.new_sheet("Sheet1",data=sheet_data)
    # Dosyayı kaydet
    wb.save(outputFilePath)