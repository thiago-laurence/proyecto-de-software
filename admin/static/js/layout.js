
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