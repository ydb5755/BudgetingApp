const delButtons = document.getElementsByClassName('del-button');
const reassignButtons = document.getElementsByClassName('reassign-button');

async function deleteVendor(id){
    var result = await fetch(`/delete_vendor/${id}`, {method:'POST'});
    var data = await result.json();
    document.getElementById(`${id}-row`).remove();
}

async function updateBudgetCategory(id, updatedName){
    var result = await fetch(`/delete_vendor/${id}/${updatedName}`, {method:'POST'});
    var data = await result.json();
}



async function startEditMode(id){
    for(let i = 0; i < reassignButtons.length; i++){
        reassignButtons[i].disabled = true;
    }

    const handleKeydown = async (e) => {
        if (e.key === 'Enter') {
            document.removeEventListener('keydown', handleKeydown);
            const vendor = document.getElementById(`bc-line-${id}`);
            const vendorInput = document.getElementById(`bc-input-${id}`);
            vendor.innerText = vendorInput.value;
            if (vendorInput.parentNode) {
                vendorInput.parentNode.removeChild(vendorInput);
            }
            var result = await fetch(`/update_vendors_budget_category/${id}/${vendor.innerText}`, {method:'POST'});
            var data = await result.json();
            for(let i = 0; i < reassignButtons.length; i++){
                reassignButtons[i].disabled = false;
            }
        }
    };

    document.addEventListener('keydown', handleKeydown);

    const vendor = document.getElementById(`bc-line-${id}`);
    var placeholderText = vendor.innerText
    vendor.innerText = ''
    var inputElem = document.createElement("input");
    inputElem.className = "form-control";
    inputElem.value = placeholderText;
    inputElem.id = `bc-input-${id}`
    vendor.appendChild(inputElem);
    inputElem.focus()
}

document.addEventListener("DOMContentLoaded", () => {
    for(let i = 0; i < delButtons.length; i++){
        delButtons[i].addEventListener('click', e => {
            deleteVendor(parseInt(e.target.id));
        })
    }
    for(let i = 0; i < reassignButtons.length; i++){
        reassignButtons[i].addEventListener('click', e => {
            startEditMode(parseInt(e.target.id));
        })
    }
  });