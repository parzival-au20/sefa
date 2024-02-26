from flask import Flask, render_template, request, session, send_file
from flask_session import Session
from scapy.all import *
import os
#from pcap_processor_scapy_seri import process_pcap_file
#from pcap_processor_scapy_paralel import process_pcap_file
from pcap_processor_pyshark_seri_copy import process_pcap_file
#from pcap_processor_pyshark_paralel import process_pcap_file
import asyncio
# import ray 
# ray.init(dashboard_port=9000)


app = Flask(__name__)

# Gizli anahtar (secret key) ayarı
app.secret_key = 'gizli_anahtar'  

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/upload", methods=["POST"])
def upload_post():
  # Dosyayı yükle
  file = request.files["file"]
  
  template_data = {
    'fileName': file.filename,
    'sourceIp': request.form["sourceIp"],
    'destinationIp': request.form["destinationIp"],
    'protocolType': request.form["protocolType"],
    'sourcePort': request.form["sourcePort"],
    'destinationPort': request.form["destinationPort"]
  }
  
  try:
    result_file_path = process_pcap_file(file,template_data)  
    session["result"] = result_file_path
  except Exception as e:
    print(e)
    return "Bir hata oluştu."


  # Form verilerini session değişkenine kaydet
  session["file"] = file.filename
  session["source_ip"] = request.form["sourceIp"]
  session["destination_ip"] = request.form["destinationIp"]
  session["protocol_type"] = request.form["protocolType"]
  session["source_port"] = request.form["sourcePort"]
  session["destination_port"] = request.form["destinationPort"]

  return render_template('result.html', template_data=template_data)

@app.route('/download/')
def return_files_tut():
   try:
    result = session.get("result", None)
    mimetype = 'text/plain'
    file_path = result
    file_name = os.path.basename(file_path)
    return send_file(file_path, mimetype=mimetype, as_attachment=True, download_name=file_name)
   except Exception as e:
    return str(e)


if __name__ == '__main__':
    app.run(debug=True, port=8000)

    
    """ http://localhost:5000 """