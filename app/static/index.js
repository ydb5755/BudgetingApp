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

    const handleKeydown = (e) => {
        if (e.key === 'Enter') {
            document.removeEventListener('keydown', handleKeydown);
            const vendor = document.getElementById(`vendor-line-${id}`);
            const vendorInput = document.getElementById(`vendor-input-${id}`);
            vendor.innerText = vendorInput.value;
            if (vendorInput.parentNode) {
                vendorInput.parentNode.removeChild(vendorInput);
            }
            
            for(let i = 0; i < reassignButtons.length; i++){
                reassignButtons[i].disabled = false;
            }
        }
    };

    document.addEventListener('keydown', handleKeydown);

    const vendor = document.getElementById(`vendor-line-${id}`);
    var placeholderText = vendor.innerText
    vendor.innerText = ''
    var inputElem = document.createElement("input");
    inputElem.value = placeholderText;
    inputElem.id = `vendor-input-${id}`
    vendor.appendChild(inputElem);
    inputElem.focus()
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