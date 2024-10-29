const addLineButton = document.getElementById("add-line-button");
const lineContainer = document.getElementById('table-body');
var counter = 1;

function addLine(){
    const columns = ['Amount', 'Vendor', 'Confirmation Code', 'Note'];
    var tr = document.createElement('tr');
    columns.forEach(column => {
        var td = document.createElement('td');
        var ip = document.createElement('input');
        ip.type = 'text'
        ip.classList = 'form-control'
        ip.name = `${column}-${counter}`
        ip.placeholder = column
        td.appendChild(ip)
        tr.appendChild(td)
    })
    counter++
    lineContainer.appendChild(tr)
    
}


document.addEventListener('DOMContentLoaded', () => {
    addLine()
    addLineButton.addEventListener('click', addLine)
})