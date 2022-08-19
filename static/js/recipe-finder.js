function validateForm() {
    if (document.forms["recipeForm"]["ingredients"].value != "") {
    
    var ingredient = document.forms["recipeForm"]["ingredients"].value;
    var entry = document.createElement("li");
    entry.name = ingredient

    document.getElementById("ingredients").value = "";

    var buttonEntry = document.createElement("button");
    buttonEntry.innerHTML = '<i class="fa-solid fa-xmark"></i> ' + ingredient;
    buttonEntry.id = ingredient;
    buttonEntry.className = "btn btn-outline-dark btn-sm";
    buttonEntry.setAttribute("onclick", "deleteIngredient(this)")

    entry.appendChild(buttonEntry);
    document.getElementById("ingredients-list").appendChild(entry)
}
}

function sendUserInfo() {
    var user_info = document.querySelectorAll('ul li button');
    var ingredients_string = ""
    for (let i = 0; i <= user_info.length - 1; i++) {
        ingredients_string += user_info[i].id + ","
    }
    const request = new XMLHttpRequest()
    request.open('POST', `/process-user-info/${JSON.stringify(ingredients_string)}`)
    request.send();
    sleep(100)
}

function deleteIngredient(item) {
    element = document.getElementById(item.id).parentElement;
    element.remove()
}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }