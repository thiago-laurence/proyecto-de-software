function delete_institution(id){

    var url =`/institutions/institution-delete/${id}`;
    console.log(url);

    fetch(url, {
    method: "DELETE",
    })
    .then(response =>
    { 
        if (!response.ok) {
            throw new Error('La solicitud no fue exitosa');
        }
        return response.json();
        //return window.location.href('')
    })
    .then(data => window.location.href = data.url )
    .catch(err => {
        console.log(err)
    })  
}

document.getElementById('formUpdate').addEventListener('submit', function(event) {
    event.preventDefault();
    var id = this.getAttribute('data-id');
    var url=`/institutions/institution-edit/${id}`;

    fetch(url,{
        method:'PUT',
        body:JSON.stringify({
            name:document.getElementById('name').value,
            info:document.getElementById('info').value,
            adress:document.getElementById('adress').value,
            web:document.getElementById('web').value,
            social_networks:document.getElementById('social_networks').value,
            phone:document.getElementById('phone').value,
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
});