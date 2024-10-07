const reassignButtons = document.getElementsByClassName('reassign-button');

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
    for(let i = 0; i < reassignButtons.length; i++){
        reassignButtons[i].addEventListener('click', e => {
            startEditMode(parseInt(e.target.id))
        })
    }
  });