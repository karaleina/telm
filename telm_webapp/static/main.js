function closeDialog(){
    var whitebg = document.getElementById("white-background");
    var dlg = document.getElementById("dlgbox");
    whitebg.style.display = "none";
    dlg.style.display = "none";
}

function showDialog(){
    var whitebg = document.getElementById("white-background");
    var dlg = document.getElementById("dlgbox");
    whitebg.style.display = "block";
    dlg.style.display = "block";

    var winWidth = window.innerWidth;
    var winHeight = window.innerHeight;

    dlg.style.left = (winWidth/2) - 480/2 + "px";
    dlg.style.top = "150px";
}

function ClearDialogFields() {

     document.getElementById("dlgName").value = "";
     document.getElementById("dlgSurname").value = "";
     document.getElementById("dlgFileHeader").value = "";
     document.getElementById("dlgFileDat").value = "";
}

function notifyUploadSuccess() {

    closeDialog();
    alert('Pomiar został dodany');
}

function validateForm() {

    if (document.getElementById("dlgName").value == "") {
        alert("Wpisz imię");
        return false;
    }
    if (document.getElementById("dlgSurname").value == "") {
        alert("Wpisz nazwiskko");
        return false;
    }
    if (document.getElementById("dlgFileHeader").value == "") {
        alert("Dołącz plik nagłówkowy");
        return false;
    }
    if (document.getElementById("dlgFileDat").value == "") {
        alert("Dołacz plik z danymi");
        return false;
    }

}