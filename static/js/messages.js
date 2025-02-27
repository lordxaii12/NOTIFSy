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
//open directory //
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".directory-btn").forEach(button => {
        button.addEventListener("click", function () {
            new bootstrap.Modal(document.getElementById("foxDirectoryModal")).show();
        });
    });
});
//==================================================================================================================================//
//open directory //
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