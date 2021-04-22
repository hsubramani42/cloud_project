var aname = ""
document.getElementById("inputfieldapprove").setAttribute("type", "hidden");
document.getElementById("inputfieldreject").setAttribute("type", "hidden");

function approve(name) {
    aname = document.getElementsByClassName(name)[1].innerHTML + "-";
    if (confirm("Are you sure you want to approve " + aname + " ?")) {
        document.getElementById("inputfieldapprove").value = document.getElementById("inputfieldapprove").value + aname;
    } else {}
}

function reject(name) {
    rname = document.getElementsByClassName(name)[1].innerHTML + "-";
    if (confirm("Are you sure you want to reject " + rname + " ?")) {
        document.getElementById("inputfieldreject").value = document.getElementById("inputfieldapprove").value + rname;
    } else {}
}
