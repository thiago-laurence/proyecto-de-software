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
    .then(json => console.log(json))
    .catch(err => console.log(err))  
}
