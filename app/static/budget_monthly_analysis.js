const monthSelector = document.getElementById('month-selector');
const tableBody = document.getElementById('table-body');



async function displayMonthLineItems(dateString){
    const [month, year] = dateString.split(' ');
    var result = await fetch(`/get_budget_details_for_month/${month}/${year}`, {method:'POST'});
    var data = await result.json();
    tableBody.innerHTML = ''
    data.forEach(budget_category => {
        const row = `
            <tr id="${budget_category.id}-row">
                <th scope="row">${budget_category.id}</th>
                <th scope="row">${budget_category.name}</th>
                <th scope="row">${budget_category.month_cost}</th>
            </tr>
        `;

        // Insert the row into the table body
        tableBody.insertAdjacentHTML('beforeend', row);

    });
    addListenersToReassignButtons();
}

document.addEventListener("DOMContentLoaded", (event) => {
    displayMonthLineItems(monthSelector.value);
    monthSelector.addEventListener('change', (e) => {
        displayMonthLineItems(e.target.value);
    })
  });