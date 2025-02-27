//-CODE BY: RYRUBIO-//
//==================================================================================================================================//
//toggle required attribute on email or phone number//
function toggleRequiredFields() {
    let sendingOption = document.getElementById("sending_option").value;
    let phoneInput = document.getElementById("phone");
    let emailInput = document.getElementById("email");

    // Reset required attributes
    phoneInput.removeAttribute("required");
    emailInput.removeAttribute("required");

    // Add required based on selection
    if (sendingOption === "sms") {
        phoneInput.setAttribute("required", "required");
    } else if (sendingOption === "email") {
        emailInput.setAttribute("required", "required");
    }
}
//==================================================================================================================================//
//open directory for single messagge //
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".directory-btn").forEach(button => {
        button.addEventListener("click", function () {
            new bootstrap.Modal(document.getElementById("foxDirectoryModal")).show();
        });
    });
});
//==================================================================================================================================//
//get data from directory single message//
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".clickable-row").forEach(row => {
        row.addEventListener("click", function() {
            let name = this.dataset.name;
            let mobile = this.dataset.mobile;
            let email = this.dataset.email;

            document.getElementById("recipient").value = name;
            document.getElementById("phone").value = mobile;
            document.getElementById("email").value = email;
        });
    });
});
//==================================================================================================================================//
//search directory for single message//
document.addEventListener("DOMContentLoaded", function () {
    const searchBar = document.getElementById("searchBar");
    const tableRows = document.querySelectorAll("#directoryTable tr");

    searchBar.addEventListener("keyup", function () {
        let searchValue = searchBar.value.toLowerCase();

        tableRows.forEach(row => {
            let name = row.getAttribute("data-name").toLowerCase();
            let mobile = row.getAttribute("data-mobile").toLowerCase();
            let email = row.getAttribute("data-email").toLowerCase();

            if (name.includes(searchValue) || mobile.includes(searchValue) || email.includes(searchValue)) {
                row.style.display = ""; 
            } else {
                row.style.display = "none";
            }
        });
    });
});
//==================================================================================================================================//
//Add recipients to recipient list//
function addRecipient() {
    let recipient = document.getElementById("mrecipient").value.trim();
    let mobile = document.getElementById("mphone").value.trim();
    let email = document.getElementById("memail").value.trim();
    let list = document.getElementById("mlist");

    if (recipient === "" || mobile === "" || email === "") {
        alert("Please fill in all fields before adding.");
        return;
    }

    let entry = `${recipient}:${mobile}:${email}`;
    list.value = list.value ? list.value + "\n" + entry : entry;

    document.getElementById("mrecipient").value = "";
    document.getElementById("mphone").value = "";
    document.getElementById("memail").value = "";
}
//==================================================================================================================================//



