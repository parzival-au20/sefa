const uploadFile = document.getElementById('uploadFile');
const protocolType = document.getElementById('protocolType');
const sourceIp = document.getElementById('sourceIp');
const destinationIp = document.getElementById('destinationIp');
const form = document.getElementById('allForm');

const send = document.getElementById('send');


$(document).ready(function () {
  $("#sourceIp").inputmask("ip", {
    //placeholder: "255.255.255.255",
    alias: "ip",
    greedy: false,
  });

  $("#destinationIp").inputmask("ip", {
    //placeholder: "255.255.255.255",
    alias: "ip",
    greedy: false,
  });
});

var sourcePort = document.getElementById("sourcePort");

sourcePort.addEventListener("input", function () {
  var inputValue = sourcePort.value;

  if (inputValue.length > 5) {
    sourcePort.value = inputValue.slice(0, 5);
  }

  if (!isNaN(inputValue) && inputValue >= 1 && inputValue <= 65535) {
    // Girilen değer geçerli bir port numarasıysa, hiçbir değişiklik yapma
    // Burada, 1 ile 65535 arasında bir port numarası olarak kabul ediliyor
  } else {
    // Geçerli bir port numarası değilse veya boşsa, input değerini temizle
    //sourcePort.value = "";
  }
});

var destinationPort = document.getElementById("destinationPort");

destinationPort.addEventListener("input", function () {
  var inputValue = destinationPort.value;
  
  if (inputValue.length > 5) {
    destinationPort.value = inputValue.slice(0, 5);
  }

  if (!isNaN(inputValue) && inputValue >= 1 && inputValue <= 65535) {
    // Girilen değer geçerli bir port numarasıysa, hiçbir değişiklik yapma
    // Burada, 1 ile 65535 arasında bir port numarası olarak kabul ediliyor
  } else {
    // Geçerli bir port numarası değilse veya boşsa, input değerini temizle
    //destinationPort.value = "";
  }

});


window.onload = function () {
  // Sayfa yüklendikten sonra bu kod çalışır
  // DOM ağacı tamamen oluşturulmuş ve içerik yüklenmiştir
  hideLoader();
  
}

function showLoader() {
  const loader = document.querySelector(".loader");
  loader.style.display = "flex";
}

function hideLoader() {
  const loader = document.querySelector(".loader");
  loader.style.display = "none";
}

if(send!=null){
  send.addEventListener("click", function () {
    // alanların kontrolü
      // Dosya türünü kontrol et
    uploadFile.onchange = (event) => {
      // Dosya türünü al
      const uploadFileExtension = uploadFile.value.split(".").pop();
      // Dosya türü istediğimiz değilse, bir hata mesajı göster
      if (uploadFileExtension != "pcap" && uploadFileExtension != "pcapng") {
        alert("Yalnızca pcap veya pcapng dosyaları yükleyebilirsiniz.");
        uploadFile.value = '';
        uploadFile.classList.add('invalid');
        event.preventDefault();
        return false;
      }
    };
    formContol();
    showLoader();

    //form.submit(); // Formu manuel olarak gönder
  });
}
else{
    disabledInputValues();  // Send gönder butonuna bağlı eğer null olursa  result htmlde olmadığı için disabled özellğini açıyoruz.
}

function disabledInputValues() {
  document.querySelectorAll("input").forEach(input => input.disabled = true);
  const protocolType = document.getElementById("protocolType");
  protocolType.disabled = true;
}


function formContol(){

    const selectedProtocol = protocolType.value;
    const sourceIpAddress = sourceIp.value;
    const destinationIpAddress = destinationIp.value;
    const sourcePortNumber = sourcePort.value;
    const destinationPortNumber = destinationPort.value;
	const genislik = window.innerWidth;
        
    const sourceCont = document.getElementById('sourceCont');
    const invalidSource = document.getElementById('invalidSource');
    const destCont = document.getElementById('destCont');
    const invalidDest = document.getElementById('invalidDest');
	const containerForm = document.getElementById('container-form');

	const inputs = [sourceIpAddress, sourcePortNumber, destinationIpAddress, destinationPortNumber];

	const validate_control = {
		"0100": function() {
			warning_sourceIp();
			sourcePort.setCustomValidity('');
			wanrnig_off_destinationIp();
			destinationPort.setCustomValidity('');
		},
		"0001": function() {
			warning_destinationIp();
			warning_off_sourceIp();
			sourcePort.setCustomValidity('');
			destinationPort.setCustomValidity('');
		},
		"0101": function() {
			warning_sourceIp();
			warning_destinationIp();
			sourcePort.setCustomValidity('');
			destinationPort.setCustomValidity('');
		},
		"0000": function() {
			warning_sourceIp();
			warning_destinationIp();
			destinationPort.setCustomValidity('');
			sourcePort.setCustomValidity('');
		},
		"0110": function() {
			warning_sourceIp();
			wanrnig_off_destinationIp();
			sourcePort.setCustomValidity('');
			destinationPort.setCustomValidity('false');
		},
		"0111": function() {
			warning_sourceIp();
			wanrnig_off_destinationIp();
			destinationPort.setCustomValidity('');
			sourcePort.setCustomValidity('');
		},
		"1001": function() {
			warning_off_sourceIp();
			warning_destinationIp();
			sourcePort.setCustomValidity('false');
			destinationPort.setCustomValidity('');
		},
		"1011": function() {
			warning_off_sourceIp();
			wanrnig_off_destinationIp();
			sourcePort.setCustomValidity('false');
			destinationPort.setCustomValidity('');
		},
		"1110": function() {
			warning_off_sourceIp();
			wanrnig_off_destinationIp();
			sourcePort.setCustomValidity('');
			destinationPort.setCustomValidity('false');
		},
		"1101": function() {
			warning_off_sourceIp();
			warning_destinationIp();
			destinationPort.setCustomValidity('');
			sourcePort.setCustomValidity('');
		},
	};

	const validationCode = inputs.map(input => input.trim() === '' ? '0' : '1').join('');

	if (validate_control.hasOwnProperty(validationCode)) {
		validate_control[validationCode]();
		if(genislik <1910){
			containerForm.style.height = '550px';
		}
		
	} else {
		destinationPort.setCustomValidity('');
		sourcePort.setCustomValidity('');
		if(sourceIpAddress!="" && destinationIpAddress == ""){  // burası dest ip önceden false kalmış olabilir bunu düzelt aynısı source ip içinde geçerli
			if (!validateIpAddress(sourceIpAddress)) { //1000 durumu
				warning_sourceIp();
				wanrnig_off_destinationIp();
				}
			else{ 
				warning_off_sourceIp();
				wanrnig_off_destinationIp();
			}
		}

		else if(destinationIpAddress !="" && sourceIpAddress == ""){  //0010 durumu
			if (!validateIpAddress(destinationIpAddress)){
				warning_destinationIp();
				warning_off_sourceIp();
			}
			else{
				wanrnig_off_destinationIp();
				warning_off_sourceIp();		
			}
		}

		else{
			if (!validateIpAddress(destinationIpAddress)){
				warning_destinationIp();
			}
			else{
				wanrnig_off_destinationIp();		
			}

			if (!validateIpAddress(sourceIpAddress)) {
				warning_sourceIp();
				}
			else{ 
				warning_off_sourceIp();
			}
		}
		
	}
	
	function warning_sourceIp() {
		sourceIp.setCustomValidity('false');
		sourceCont.style.marginBottom = '0';
		invalidSource.style.display = 'block';
	}

	function warning_destinationIp() {
		destinationIp.setCustomValidity('false');
		destCont.style.marginBottom = '0';
		invalidDest.style.display = 'block';
	}

	function warning_off_sourceIp(){
		sourceIp.setCustomValidity('');
		sourceCont.style.marginBottom = '1rem';
		invalidSource.style.display = 'none';
	}

	function wanrnig_off_destinationIp(){
		destinationIp.setCustomValidity('');
		destCont.style.marginBottom = '1rem';
		invalidDest.style.display = 'none';
	}

}


function validateIpAddress(ipAddress) {
    // IP adresinin geçerli bir formatta olup olmadığını kontrol edin
    const pattern = /^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/;
    return pattern.test(ipAddress);
  }


(() => {
'use strict'

// Fetch all the forms we want to apply custom Bootstrap validation styles to
const forms = document.querySelectorAll('.allForm')

// Loop over them and prevent submission
Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        hideLoader();
    }

    form.classList.add('was-validated');
    }, false)
})
})()