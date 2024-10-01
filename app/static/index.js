const delButtons = document.getElementsByClassName('del-button');


async function deleteCategory(id){
    console.log(id)
    var result = await fetch(`/delete_budget_category/${id}`, {method:'POST'});
    var data = await result.json();
    document.getElementById(`${id}-row`).remove();
}


document.addEventListener("DOMContentLoaded", (event) => {
    for(let i = 0; i < delButtons.length; i++){
        delButtons[i].addEventListener('click', e => {
            deleteCategory(parseInt(e.target.id))
        })
    }
  });