
function myFunction() {
    var element = document.body;
    var main_table = document.getElementById("main_table");
    if (element.dataset.bsTheme == "light"){
        element.dataset.bsTheme = "dark";
        main_table.classList.remove('table-light');
        main_table.classList.add('table-dark');
    }
    else{
        element.dataset.bsTheme = "light";
        main_table.classList.remove('table-dark');
        main_table.classList.add('table-light');
    }
}

var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})






