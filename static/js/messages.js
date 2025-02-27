//-JS CODE FOR 'NOTIFS' BY: RYRUBIO-//
//==================================================================================================================================//
//========= SINGLE MSG =============================================================================================================//
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
            let modal = new bootstrap.Modal(document.getElementById("foxDirectoryModal"));
            modal.show();

            let tableBody = document.getElementById("directoryTable");
            tableBody.innerHTML = '<tr><td colspan="3">Loading...</td></tr>'; // Show loading message

            fetch("/display_data")
                .then(response => response.json())
                .then(data => {
                    tableBody.innerHTML = "";
                    data.forEach(row => {
                        let tr = document.createElement("tr");
                        tr.classList.add("clickable-row");
                        tr.dataset.name = row.name;
                        tr.dataset.mobile = row.mobile_no;
                        tr.dataset.email = row.email;
                        tr.innerHTML = `
                            <td>${row.name}</td>
                            <td>${row.mobile_no}</td>
                            <td>${row.email}</td>
                        `;
                        tableBody.appendChild(tr);
                    });

                    addRowClickEvent();
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                    tableBody.innerHTML = '<tr><td colspan="3">Failed to load data</td></tr>';
                });
        });
    });

    function addRowClickEvent() {
        document.querySelectorAll(".clickable-row").forEach(row => {
            row.addEventListener("click", function () {
                let name = this.dataset.name;
                let mobile = this.dataset.mobile;
                let email = this.dataset.email;

                document.getElementById("recipient").value = name;
                document.getElementById("phone").value = mobile;
                document.getElementById("email").value = email;
            });
        });
    }
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

    searchBar.addEventListener("keyup", function () {
        let searchValue = searchBar.value.toLowerCase();
        let tableRows = document.querySelectorAll("#directoryTable tr"); // Get updated rows dynamically

        tableRows.forEach(row => {
            let name = row.dataset.name ? row.dataset.name.toLowerCase() : "";
            let mobile = row.dataset.mobile ? row.dataset.mobile.toLowerCase() : "";
            let email = row.dataset.email ? row.dataset.email.toLowerCase() : "";

            if (name.includes(searchValue) || mobile.includes(searchValue) || email.includes(searchValue)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});
//==================================================================================================================================//
//
//
//
//========= MULTI MSG ==============================================================================================================//
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
//open directory for Multi messagge //
document.addEventListener("DOMContentLoaded", function () {
    // Fetch data before opening the modal
    document.querySelectorAll(".multi_directory-btn").forEach(button => {
        button.addEventListener("click", function () {
            fetch("/display_data")
                .then(response => response.json())
                .then(data => {
                    let tableBody = document.getElementById("mdirectoryTable");
                    tableBody.innerHTML = ""; // Clear old data

                    data.forEach(row => {
                        let newRow = document.createElement("tr");
                        newRow.classList.add("clickable-row");
                        newRow.setAttribute("data-name", row.name);
                        newRow.setAttribute("data-mobile", row.mobile_no);
                        newRow.setAttribute("data-email", row.email);

                        newRow.innerHTML = `
                            <td><input type="checkbox" class="row-checkbox"></td>
                            <td>${row.name}</td>
                            <td>${row.mobile_no}</td>
                            <td>${row.email}</td>
                        `;

                        tableBody.appendChild(newRow);
                    });

                    // Reattach click event for new rows
                    addRowClickEvent();

                    // Open modal after data is loaded
                    new bootstrap.Modal(document.getElementById("multi_foxDirectoryModal")).show();
                })
                .catch(error => console.error("Error fetching data:", error));
        });
    });

    // Function to add event listener to clickable rows
    function addRowClickEvent() {
        document.querySelectorAll(".clickable-row").forEach(row => {
            row.addEventListener("click", function () {
                let name = this.dataset.name;
                let mobile = this.dataset.mobile;
                let email = this.dataset.email;

                document.getElementById("mrecipient").value = name;
                document.getElementById("mphone").value = mobile;
                document.getElementById("memail").value = email;
            });
        });
    }
});
