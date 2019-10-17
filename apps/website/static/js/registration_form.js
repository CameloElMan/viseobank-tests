/* Float Label Pattern Plugin for Bootstrap 3.1.0 by Travis Wilson
**************************************************/
var valid = false;
var tries = 0;
var MAX_TRIES = 3;
var firstTime = true;
var timeLeft = 10;
var intervalId;
var video;
var countdown;
var preview = document.createElement("img");
const VerificationStatus = Object.freeze({"NON_VERIFIED":0, "VERIFYING":1, "VERIFICATION_SUCCESS":2, "VERIFICATION_FAILURE":3});
var currentVerificationStatus = VerificationStatus.NON_VERIFIED;
const imWidth = 800;

function fileValidation(){
    var fileInput = document.getElementById('cardInput');
    if(fileInput.value==""){
        //alert('Por favor ingrese un archivo en formato JPG/PNG');
        fileInput.value = '';
        return false;
    }else{
     return true;
 }
}

function imageToDataUri(img, width, imtitle) {
    let height = (width/img.width) * img.height;
    // create an off-screen canvas
    var canvas = document.createElement('canvas'),
    ctx = canvas.getContext('2d');
    var srcOrientation;

    // set its dimension to target size
    canvas.width = width;
    canvas.height = height;

    EXIF.getData(img, function() {
        srcOrientation = EXIF.getTag(this, "Orientation");
    });

    // transform context before drawing image
    switch (srcOrientation) {
      case 2: ctx.transform(-1, 0, 0, 1, width, 0); break;
      case 3: ctx.transform(-1, 0, 0, -1, width, height); break;
      case 4: ctx.transform(1, 0, 0, -1, 0, height); break;
      case 5: ctx.transform(0, 1, 1, 0, 0, 0); break;
      case 6: ctx.transform(0, 1, -1, 0, height, 0); break;
      case 7: ctx.transform(0, -1, -1, 0, height, width); break;
      case 8: ctx.transform(0, -1, 1, 0, 0, width); break;
      default: break;
    }
    
    // draw source image into the off-screen canvas:
    ctx.drawImage(img, 0, 0, width, height);

    // encode image to data-uri with base64 version of compressed image
    return canvas.toDataURL('image/jpeg');
}

function disablePreviousButton() {
    var els = document.querySelectorAll("a[href='#previous']");
    for (var i = 0, l = els.length; i < l; i++) {
      var el = els[i];
      el.style.display = "none";
    }
}

function disableNextButton() {
    var els = document.querySelectorAll("a[href='#next']");
    for (var i = 0, l = els.length; i < l; i++) {
      var el = els[i];
      el.style.display = "none";
    }
}

function enablePreviousButton() {
    var els = document.querySelectorAll("a[href='#previous']");
    for (var i = 0, l = els.length; i < l; i++) {
      var el = els[i];
      el.style.display = "";
    }
}

function enableNextButton() {
    var els = document.querySelectorAll("a[href='#next']");
    for (var i = 0, l = els.length; i < l; i++) {
      var el = els[i];
      el.style.display = "";
    }
}

function previewFile() {
    /*
  var preview = document.querySelector('#cardPreview');
  var file    = document.querySelector('input[type=file]').files[0];
  var reader  = new FileReader();

  reader.onloadend = function () {
    preview.src = reader.result;
}

if (file) {
    reader.readAsDataURL(file);
} else {
    preview.src = "";
}*/
}

//-------------------------------------------------------------

function createCountdown() {
    var countdownNumberEl = document.getElementById('countdown-number');
    var contdownEl = document.getElementById('countdown');
    countdown = 10;
    var svgEl = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    var circleEl = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circleEl.setAttribute("r","18");
    circleEl.setAttribute("cx","20");
    circleEl.setAttribute("cy","20");

    countdownNumberEl.textContent = countdown;
    svgEl.appendChild(circleEl);
    contdownEl.appendChild(svgEl);
}

function removeCameraContainer() {
    video.srcObject.getTracks()[0].stop();
    const camContainerEl = document.getElementById("cam-container");
    while (camContainerEl.firstChild) {
        camContainerEl.removeChild(camContainerEl.firstChild);
    }
}


function setValidationMessage(success) {
    var validationMessageEl = $("#validation-msg");
    var validationButtonEl = $("#validation-button");

    if(success) {
        validationMessageEl.text("Verificación completada con éxito.");
        enableNextButton();
    } else {
        validationMessageEl.text("Desafortunadamente, no hemos podido validar su identidad. Por favor, inténtelo de nuevo con una foto de mayor calidad y en un lugar adecuadamente iluminado, o acuda a su sucursal más cercana.");
        validationButtonEl.show();
    }
}
function onEverySecond() {
    var countdownNumberEl = document.getElementById('countdown-number');

    // if there's time and still not verified
    if(countdown > 0 && currentVerificationStatus != VerificationStatus.VERIFICATION_SUCCESS ) {
        // if there isn't a validation in progress, throw a new one.
        if(currentVerificationStatus != VerificationStatus.VERIFYING) {
            var cardPhoto = imageToDataUri(preview, imWidth, 'card');
            var camFrame = imageToDataUri(document.getElementById('video'),imWidth,'cam');
            validate_photo(cardPhoto, camFrame);
        }
    // if there's no time
    } else {
        removeCameraContainer();
        setValidationMessage(currentVerificationStatus == VerificationStatus.VERIFICATION_SUCCESS);
        clearInterval(intervalId);
    }    

    countdown = (countdown - 0.2) < 0 ? 0 : (countdown - 0.2);
    countdownNumberEl.textContent = Math.floor(countdown);
}

function enableCam() {
    // Grab elements, create settings, etc.
    video = document.getElementById('video');

    // Get access to the camera!
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Not adding `{ audio: true }` since we only want video now
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            //video.src = window.URL.createObjectURL(stream);
            video.srcObject = stream;
            video.play();

              var file    = document.querySelector('input[type=file]').files[0];
              var reader  = new FileReader();

            reader.onloadend = function () {
                preview.src = reader.result;
            }

            if (file) {
                reader.readAsDataURL(file);
            } else {
                preview.src = "";
            }

            createCountdown();

            intervalId = setInterval(onEverySecond, 200);
        });
    }
}



function nextStep(steps){
    if(steps==5){
        if(fileValidation()){
            $("#step-"+steps).fadeOut("slow", function() {
               $("#progressBar").css("width", "66%"); 

                    // create video element
                    enableCam();
                    $("#step-"+(steps+1)).fadeIn("fast");
                    var video = document.getElementById('video');
                    video.play();
                });
        }
    }else{
      if(checkSteps(steps)){
         console.log("aqui");
         $("#step-"+steps).fadeOut("slow", function() {
            $("#progressBar").css("width", "33%");
            $("#step-"+(steps+1)).fadeIn("fast");
        });
         $("#step-"+(steps+1)+" :input, select" ).focusout(function() {
            checkSteps(steps+1);
        });
     }
 }
}
function validate_photo(cardPhoto, camFrame) {//THIS //DONE
    $.ajax({
        url: 'ajax/validate_photo/',
        type: 'post',
        data: {
            'cardPhoto': cardPhoto,
            'camFrame': camFrame,
            'firstName': $("#first_name").val(),
            'lastName': $("#last_name").val(),  
        },
        dataType: 'json',
        success: function (data) {
            console.log(data.match);
            if(data.match){
                currentVerificationStatus = VerificationStatus.VERIFICATION_SUCCESS;
            } else {
                currentVerificationStatus = VerificationStatus.VERIFICATION_FAILURE;
            }
        }
    });
    currentVerificationStatus =  VerificationStatus.VERIFYING;
}

function create_lead() {//THIS //DONE
    leadData = {
        "first_name": document.getElementById("first_name").value,
        "last_name": document.getElementById("last_name").value,
        "second_last_name": document.getElementById("second_last_name").value,
        "email": document.getElementById("email").value,
        "phone": document.getElementById("phone").value,
        "estado_civil": document.getElementById("estado_civil").value,
        "sexo": document.getElementById("sexo").value,
        "birth_date": document.getElementById("birth_date").value,
        "birth_month": document.getElementById("birth_month").value,
        "birth_year": document.getElementById("birth_year").value,
        "ciudadania": document.getElementById("ciudadania").value,
        "direccion": document.getElementById("direccion").value,
        "documentType": document.getElementById("documentType").value,
        "documentNumber": document.getElementById("documentNumber").value,
        "residencia": document.getElementById("residencia").value,
        "productType": document.getElementById("productType").value,
        "necesidad": document.getElementById("necesidad").value,
        "image__c" : imageToDataUri(preview, imWidth, 'card')
    };

    $.ajax({
        url: 'ajax/create_lead/',
        type: 'post',
        data: leadData,
        dataType: 'json',
        success: function (data) {
            document.location.href="/";
        }
    });
}

function captureFrame(video) { //THIS //DONE
    var canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    var canvasContext = canvas.getContext("2d");
    canvasContext.drawImage(video, 0, 0);
    var b64 = canvas.toDataURL('image/png');
    return b64;
}

async function onPlay(videoEl) { //THIS //DONE
    setTimeout(() => onPlay(videoEl));
}

function showStatusPopup(success, title, message, millis, redirect) { //THIS //DONE
    if(success) {
        $("#successIcon").css({ 'display' : ''});
        $("#failureIcon").css({ 'display' : 'none' });
    } else {
        $("#successIcon").css({ 'display' : 'none' });
        $("#failureIcon").css({ 'display' : '' });
    }

    $("#modalTitle").text(title);
    $("#modalMessage").text(message);

    $("#modal").fadeIn("slow", function() {

        setTimeout(function(){
            $("#modal").fadeOut("slow", function() {
                if(redirect) {
                  window.location.href = "/";
              }
          });
        }, millis); 
        
    });
}




//-------------------------------------------Validaciones----------------------------------------

function checkSteps(step){
    var validationRules = []; // True: has err condition ; False: no err condition.
    switch(step) {      
        case 0:

        break;

        case 1:
        break;

        case 2:
            validationRules.push($("#documentType").val() == "");
            validationRules.push($("#documentNumber").val() == "");
            validationRules.push($('#cardInput').get(0).files.length == 0);
            validationRules.push($("#residencia").val() == "");

            if(!validationRules.includes(true)) {
               disablePreviousButton();
                disableNextButton();
                enableCam();  
            }
            
        break;

        case 3:
        break;

        case 4:
        break;    

    }
    window.location.hash = '#signup-form';

    return true;
}

function changeField(validaciones, campo, salida){
    validaciones.push(salida);
    if(salida){
        $('#'+campo).css("border-bottom","1px solid #009e06");
        $('#'+campo).parent().find(".alert").remove();
        
    }else{
        $('#'+campo).css("border-bottom","1px solid #f00");
        if($('#'+campo).parent().find(".alert").length){

        }else{
         $( '#'+campo ).after( "<p class='alert'>"+errorMesages(campo)+"</p>");
     }           
 }   
}


function errorMesages(caso){
    var mensage="";
    switch(caso) {
        case "productType":
        mensage="Escoja un tipo de producto.";
        break;          
        case "documentType":
        mensage="Escoja un documento.";
        break;
        case "documentNumber":
        mensage="Identificacion incorrecta.";
        break;        
        case "lastName":
        mensage="Campo apellido vacio.";
        break;
        case "birthDate":
        mensage="La fecha no es correcta.";
        break;
        case "cardInput":
        mensage="Por favor ingrese un archivo en formato JPG/PNG.";
        break;
        case "fecha":
        mensage="La edad no puede ser menor a 18 años.";
        break;
        case "email":
        mensage="Formato del email incorrecto.";
        break;
        case "phone":
        mensage="Movil no valido.";
        break;
        default:
        mensage="Este valor no puede estar vacio.";
    }
    return mensage;
}

function calcularEdad(year,month,day) {
    var hoy = new Date();
    var fecha=(year=="" ||month=="" ||day=="") ? "": year+"-"+month+"-"+day;
    var cumpleanos = new Date(fecha);
    var edad = hoy.getFullYear() - cumpleanos.getFullYear();
    var m = hoy.getMonth() - cumpleanos.getMonth();

    if (m < 0 || (m === 0 && hoy.getDate() < cumpleanos.getDate())) {
        edad--;
    }
    if(edad<18 || fecha==""){
        return false;
    }else{
        return true;
    }
    
}


function validate(value) {
  var validChars = 'TRWAGMYFPDXBNJZSQVHLCKET';
  var nifRexp = /^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKET]{1}$/i;
  var nieRexp = /^[XYZ]{1}[0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKET]{1}$/i;
  var str = value.toString().toUpperCase();

  if (!nifRexp.test(str) && !nieRexp.test(str)) return false;

  var nie = str
  .replace(/^[X]/, '0')
  .replace(/^[Y]/, '1')
  .replace(/^[Z]/, '2');

  var letter = str.substr(-1);
  var charIndex = parseInt(nie.substr(0, 8)) % 23;

  if (validChars.charAt(charIndex) === letter) return true;

  return false;
}

function _goToStep(wizard, options, state, index)
{
    return paginationClick(wizard, options, state, index);
}


/*--------------------------Bar Style--------------------------------*/

$(function() {
    $( ".steps.clearfix" ).prepend( "<div id='logo'> <img src='https://viseofaces.herokuapp.com/static/images/v-dbank-logo-w.svg' height='100'> </div>" );

    $(".steps.clearfix").append(
        '<div id="terms"> <img src="https://viseofaces.herokuapp.com/static/images/ill-bank.svg" height="190"></div>'
        );
});