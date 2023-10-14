function putValues(id,name,info,key_words,type){
    form = document.getElementById("formUpdate");
    form.querySelector("input[name='name']").value = name;
    form.querySelector("textarea[name='info']").value = info;
    form.querySelector("input[name='key_words']").value = key_words;
    select = form.querySelector("select[name='type']")
    select.value = type;

    select.querySelector(`option[value="${type}"]`).selected = true;

    document.getElementById("update").addEventListener("click", function(){
        Update("formUpdate",id,"services");
    });
    document.getElementById("delete").addEventListener("click", function(){
        Delete(id,"services");
    });
}


        
// document.getElementById("updateProductButton").addEventListener("click", function(){
//     object_id = document.getElementById("updateProductButton").getAttribute("data-id");
//     console.log(object_id);
//     object_name = document.getElementById("updateProductButton").getAttribute("data-name");
//     console.log(object_name);
//     object_info = document.getElementById("updateProductButton").getAttribute("data-info");
//     console.log(object_info);
//     object_keyw = document.getElementById("updateProductButton").getAttribute("data-keyw");
//     object_type = document.getElementById("updateProductButton").getAttribute("data-type");

//     form = document.getElementById("formUpdate");
//     form.querySelector("input[name='name']").value = object_name;
//     form.querySelector("textarea[name='info']").value = object_info;
//     form.querySelector("input[name='key_words']").value = object_keyw;
//     form.querySelector("select[name='type']").value = object_type;

//     document.getElementById("update").addEventListener("click", function(){
//         Update("formUpdate",object_id,"services");
//     });
//     document.getElementById("delete").addEventListener("click", function(){
//         Delete(object_id,"services");
//     });
// });