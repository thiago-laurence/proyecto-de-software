object_id = document.getElementById("updateProductButton").getAttribute("data-id");
object_name = document.getElementById("updateProductButton").getAttribute("data-name");
object_info = document.getElementById("updateProductButton").getAttribute("data-info");
object_keyw = document.getElementById("updateProductButton").getAttribute("data-keyw");
object_type = document.getElementById("updateProductButton").getAttribute("data-type");

        
document.getElementById("updateProductButton").addEventListener("click", function(){
    form = document.getElementById("formUpdate");
    form.querySelector("input[name='name']").value = object_name;
    form.querySelector("textarea[name='info']").value = object_info;
    form.querySelector("input[name='key_words']").value = object_keyw;
    form.querySelector("select[name='type']").value = object_type;

    document.getElementById("update").addEventListener("click", function(){
        Update("formUpdate",object_id,"services");
    });
    document.getElementById("delete").addEventListener("click", function(){
        Delete(object_id,"services");
    });
});