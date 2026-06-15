function uploadFile() {

    let file =
        document.getElementById("excelFile").files[0];

    if (!file) {

        alert("Please Select Excel File");

        return;
    }

    let formData = new FormData();

    formData.append("file", file);

    fetch("/upload", {

        method: "POST",
        body: formData

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        location.reload();

    })

    .catch(error => {

        console.log(error);

    });

}

// DataTable
$(document).ready(function () {
    $('#shareholderTable').DataTable();
});


