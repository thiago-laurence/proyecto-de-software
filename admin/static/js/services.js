console.log('services.js loaded...');

document.getElementById('formUpdate').addEventListener('submit', function(event) {
    event.preventDefault();
    var id = this.getAttribute('data-id');
    var url=`/services/service-edit/${id}`;

    fetch(url,{
        method:'PUT',
        body:JSON.stringify({
            name:document.getElementById('name').value,
            info:document.getElementById('info').value,
            key_words:document.getElementById('key_words').value,
            type:document.getElementById('type').value
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


function delete_service(id){

    var url =`/services/service-delete/${id}`;
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