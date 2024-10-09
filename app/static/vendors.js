const delButtons = document.getElementsByClassName('del-button');

async function deleteVendor(id){
    var result = await fetch(`/delete_vendor/${id}`, {method:'POST'});
    var data = await result.json();
    document.getElementById(`${id}-row`).remove();
}
document.addEventListener("DOMContentLoaded", (event) => {
    for(let i = 0; i < delButtons.length; i++){
        delButtons[i].addEventListener('click', e => {
            deleteVendor(parseInt(e.target.id));
        })
    }
  });