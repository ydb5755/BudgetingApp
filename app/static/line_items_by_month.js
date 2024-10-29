const monthSelector = document.getElementById('month-selector');
const tableBody = document.getElementById('table-body');
const childTableBody = document.getElementById('child-table-body');
var reassignButtons = document.getElementsByClassName('reassign-button');


async function startEditMode(id){
    for(let i = 0; i < reassignButtons.length; i++){
        reassignButtons[i].disabled = true;
    }

    const handleKeydown = async (e) => {
        if (e.key === 'Enter') {
            document.removeEventListener('keydown', handleKeydown);
            const vendor = document.getElementById(`vendor-line-${id}`);
            const vendorInput = document.getElementById(`vendor-input-${id}`);
            vendor.innerText = vendorInput.value;
            if (vendorInput.parentNode) {
                vendorInput.parentNode.removeChild(vendorInput);
            }
            var result = await fetch(`/update_vendor/${id}/${vendor.innerText}`, {method:'POST'});
            var data = await result.json();
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

async function displayMonthLineItems(dateString){
    const [month, year] = dateString.split(' ');
    var result = await fetch(`/get_month_line_items/${month}/${year}`, {method:'POST'});
    var data = await result.json();
    tableBody.innerHTML = ''
    childTableBody.innerHTML = ''
    data.forEach(li => {
        if (!li.parent_line_item_id){
            const row = `
                <tr id="${li.id}-row">
                    <th scope="row">${li.id}</th>
                    <th scope="row">${li.amount}</th>
                    <th scope="row">${li.currency_type}</th>
                    <th scope="row" id="vendor-line-${li.id}">${li.vendor}</th>
                    <th scope="row">${li.date}</th>
                    <th scope="row">${li.confirmation_code}</th>
                    <th scope="row">${li.note || ''}</th>
                    <th scope="row"><button id="${li.id}" class="btn btn-primary reassign-button">Click to reassign vendor</button></th>
                    <th scope="row"><a class="btn btn-primary" href="/split_line/${li.id}">Click to split line</a></th>
                </tr>
            `;
    
            // Insert the row into the table body
            tableBody.insertAdjacentHTML('beforeend', row);
        } else {
            const row = `
                <tr id="${li.id}-row">
                    <th scope="row">${li.id}</th>
                    <th scope="row">${li.parent_line_item_id}</th>
                    <th scope="row">${li.amount}</th>
                    <th scope="row">${li.currency_type}</th>
                    <th scope="row" id="vendor-line-${li.id}">${li.vendor}</th>
                    <th scope="row">${li.date}</th>
                    <th scope="row">${li.confirmation_code}</th>
                    <th scope="row">${li.note || ''}</th>
                    <th scope="row"><button id="${li.id}" class="btn btn-primary reassign-button">Click to reassign vendor</button></th>
                </tr>
            `;
    
            // Insert the row into the table body
            childTableBody.insertAdjacentHTML('beforeend', row);
        }

    });
    addListenersToReassignButtons();
}

function addListenersToReassignButtons() {
    reassignButtons = document.getElementsByClassName('reassign-button');
    for(let i = 0; i < reassignButtons.length; i++){
        reassignButtons[i].addEventListener('click', e => {
            startEditMode(parseInt(e.target.id));
        })
    }
}

document.addEventListener("DOMContentLoaded", (event) => {
    displayMonthLineItems(monthSelector.value);
    monthSelector.addEventListener('change', (e) => {
        displayMonthLineItems(e.target.value);
    })
  });