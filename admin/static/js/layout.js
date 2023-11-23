
function selectInstitution(id){
    let data = {
        institution_id: id,
    }

    fetch('/login/update-actual-institution', {
    method: "POST",
    body: JSON.stringify(data),
    headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    .then(response =>
    { 
        if (!response.ok) {
            throw new Error('La solicitud no fue exitosa');
       
        }
        return response.json();
    })
    .then(json => window.location.href = json['url'])
    .catch(err => {
        console.log(err)
    })  
}

function Update(idForm, idObject, module){
    var form = document.getElementById(idForm);
    var url = `/` + module + `/` + module + `-update/${idObject}`;
    var elements = form.elements;

    var data = {};
    for (var i = 0; i < elements.length; i++) {
        var input = elements[i];
        data[input.name] = input.value; 
    }
    console.log(data);
    if(module == "institutions"){
        console.log(data['phone']);
        checkparams_institutions(data['phone'],data['localization']);
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

function Delete(idObject, module){
    var url =`/` + module + `/` + module + `-delete/${idObject}`;

    fetch(url, {
    method: "DELETE",
    })
    .then(response =>
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

function checkparams_institutions(phone, localization){

    const patron_phone = /^[0-9-]+$/;
    const patron_localization = /^[-0-9,.]+$/;
    var msjPhone = document.getElementById("phoneError");
    var msjLoc = document.getElementById("localizationError");

    if (patron_phone.test(phone)) {
        // El valor es válido, no hacer nada
        msjPhone.style.display = "none"; // Ocultar el mensaje de error

    } else {
        // El valor no es válido, mostrar un mensaje de error o realizar alguna acción
        msjPhone.style.display = "block"; // Mostrar el mensaje de error
        input.focus(); // Enfocar nuevamente el campo
        return false;
    }
    if(patron_localization.test(localization)){
        // El valor es válido, no hacer nada
        msjLoc.style.display = "none"; // Ocultar el mensaje de error
    }
    else{
        // El valor no es válido, mostrar un mensaje de error o realizar alguna acción
        msjLoc.style.display = "block"; // Mostrar el mensaje de error
        input.focus(); // Enfocar nuevamente el campo
        return false;
    }
}
