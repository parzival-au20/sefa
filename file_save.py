import os
import datetime

def fileSave(file):
    if not os.path.exists("uploads"): #uploads yoksa dizin oluşturacak
        os.makedirs("uploads")

  # Dosyayı yükle
    inputFileName = file.filename
    inputTargetPath = "uploads/{}".format(inputFileName)

    # Dosyayı kaydet file.save(os.path.join("uploads", filename))
    file.save(inputTargetPath)    

    # Şimdiki zamanı alın.
    now = datetime.datetime.now()

    # Dosya adını oluşturun.
    outputFileName = now.strftime("%Y%m%d_%H%M%S_"+inputFileName+".xlsx")

    if not os.path.exists("output"): #output yoksa dizin oluşturacak
      os.makedirs("output")
    # Dosyanın yolunu oluşturun.
    outputFilePath = os.path.join("output", outputFileName)


    # Kullanıcıya bir yanıt döndür
    print("Dosya başarıyla yüklendi.")
    return inputTargetPath,outputFilePath