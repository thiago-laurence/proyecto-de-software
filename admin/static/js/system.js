function update(idForm){
    var form = document.getElementById(idForm);

    var id = form.getAttribute('data-id');
    var action = form.getAttribute('data-action');
    var module = form.getAttribute('data-module');
    var url = `/` + module + `/` + module + `-` + action + `/${id}`;

    var elements = form.elements;
    var data = {};
    for (var i = 0; i < elements.length -1; i++) { // -1 para no tomar el boton de submit
        var input = elements[i];
        data[input.name] = input.value; 
    }

    fetch(url,{
        method:'PUT',
        body:JSON.stringify({
            data
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    }).then(response =>
        { 
            if (!response.ok) {
                throw new Error('La solicitud no fue exitosa');
            }
            return response.json();
        })
        .then(data => window.location.href = data.url)
        .catch(err => {
            console.log(err)
        }) 
}


// // --> RESET DE FORMULARIOS MEDIANTE BOTON CANCELAR <--
// function ResetFormulario(boton){
//     var formulario = boton.closest("form");
//     var campos = formulario.querySelectorAll(".InputText, .InputDate, .InputSelect, .InputNumber, .InputFoto");

//     campos.forEach(function (campo) {
//         campo.value = '';
//         if (campo.classList.contains("is-valid")) {
//             campo.classList.remove("is-valid");
//         } 
//         if (campo.classList.contains("is-invalid")) {
//             campo.classList.remove("is-invalid");
//         }
//     });

//     var botonEnvio = formulario.querySelector(".BtnEnvioForm");
//     botonEnvio.disabled = true;
// }
// var botonesCancelar = document.querySelectorAll(".BtnCancelarForm");
// botonesCancelar.forEach(function (elemento) {
//     elemento.addEventListener('click', function () {
//         ResetFormulario(this);
//     });
// });

// // --> VALIDACION DE FORMULARIOS PARA BOTON ACEPTAR <--
// var formularios = document.querySelectorAll(".Formulario");
// var botonesEnvio = document.querySelectorAll(".BtnEnvioForm");

// function ValidarFormulario() {
//     var formulario = this;
//     var campos = formulario.querySelectorAll(".InputText, .InputDate, .InputSelect, .InputNumber");
//     var todosValidos = true;

//     campos.forEach(function (campo) {
//         if (!campo.classList.contains("is-valid")) {
//             todosValidos = false;
//             return;
//         }
//     });

//     var botonEnvio = formulario.querySelector(".BtnEnvioForm");
//     if (todosValidos) {
//         botonEnvio.disabled = false;
//     } else {
//         botonEnvio.disabled = true;
//     }
// }

// // --> VALIDACION DE INPUT TEXT <--
// function ValidarInputText() {
//     if (this.value.trim() !== '') {
//         this.classList.remove('is-invalid');
//         this.classList.add('is-valid');
//     } else {
//         this.classList.remove('is-valid');
//         this.classList.add('is-invalid');
//     }
// }

// // --> VALIDACION DE INPUT DATE <--
// function ValidarInputDate(fechaActual) {
//     if (this.value.trim() !== '' && (this.value <= fechaActual)) {
//         this.classList.remove('is-invalid');
//         this.classList.add('is-valid');
//     } else {
//         this.classList.remove('is-valid');
//         this.classList.add('is-invalid');
//     }
// }

// // --> VALIDACION DE INPUT SELECT <--
// function ValidarInputSelect() {
//     if (this.selectedIndex !== -1) {
//         this.classList.remove('is-invalid');
//         this.classList.add('is-valid');
//     } else {
//         this.classList.remove('is-valid');
//         this.classList.add('is-invalid');
//     }
// }

// // --> VALIDACION DE INPUT NUMBER <--
// function ValidarInputNumber() {
//     if (/^[0-9]+([.][0-9]+)?$/.test(this.value)) {
//         var pesoNum = parseFloat(this.value);
//         var enteroMin = 0; // Valor mínimo para la parte entera
//         var enteroMax = 100; // Valor máximo para la parte entera
//         var decimalMin = 0; // Valor mínimo para la parte decimal
//         var decimalMax = 999; // Valor máximo para la parte decimal

//         var entero = Math.floor(pesoNum);
//         var decimal = Math.round((pesoNum - entero) * 100);

//         if (entero >= enteroMin && entero <= enteroMax && decimal >= decimalMin && decimal <= decimalMax) {
//             this.classList.remove("is-invalid");
//             this.classList.add("is-valid");
//         } else {
//             this.classList.remove("is-valid");
//             this.classList.add("is-invalid");
//         }
//     } else {
//         this.classList.remove("is-valid");
//         this.classList.add("is-invalid");
//     }
// }

// var fechaActual = new Date();
// fechaActual.setUTCHours(fechaActual.getUTCHours() - 3); // Modifica la fecha para que sea la actual de Argentina
// var valorActual = fechaActual.toISOString().split("T")[0];
// formularios.forEach(function (formulario) {
//     var campos = formulario.querySelectorAll(".InputText, .InputDate, .InputSelect, .InputNumber");
//     campos.forEach(function (campo) {
//         campo.addEventListener("input", function () {
//             if (campo.classList.contains("InputText")) {
//                 ValidarInputText.call(campo);
//             } else if (campo.classList.contains("InputDate")) {
//                 campo.setAttribute("max", valorActual);
//                 ValidarInputDate.call(campo, valorActual);
//             } else if (campo.classList.contains("InputSelect")) {
//                 ValidarInputSelect.call(campo);
//             } else if (campo.classList.contains("InputNumber")) {
//                 ValidarInputNumber.call(campo);
//             }
//             ValidarFormulario.call(formulario);
//         });
//     });
// });