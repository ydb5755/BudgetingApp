const delButtons = document.getElementsByClassName('del-button');
const reassignButtons = document.getElementsByClassName('reassign-button');

async function deleteCategory(id){
    var result = await fetch(`/delete_budget_category/${id}`, {method:'POST'});
    var data = await result.json();
    document.getElementById(`${id}-row`).remove();
}
function startEditMode(id){
    for(let i = 0; i < reassignButtons.length; i++){
        reassignButtons[i].disabled = true;
    }
    document.addEventListener('')
    const vendor = document.getElementById(`vendor-line-${id}`);
    var placeholderText = vendor.innerText
    vendor.innerText = ''
    var inputElem = document.createElement("input");
    inputElem.value = placeholderText;
    vendor.appendChild(inputElem);
}

document.addEventListener("DOMContentLoaded", (event) => {
    for(let i = 0; i < delButtons.length; i++){
        delButtons[i].addEventListener('click', e => {
            deleteCategory(parseInt(e.target.id))
        })
    }
    for(let i = 0; i < reassignButtons.length; i++){
        reassignButtons[i].addEventListener('click', e => {
            startEditMode(parseInt(e.target.id))
        })
    }
  });