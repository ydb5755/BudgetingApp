const monthSelector = document.getElementById('month-selector');
const tableBody = document.getElementById('table-body');


document.addEventListener("DOMContentLoaded", (event) => {
    displayMonthLineItems(monthSelector.value);
    monthSelector.addEventListener('change', (e) => {
        displayMonthLineItems(e.target.value);
    })
  });