//-JS CODE FOR 'NOTIFS' BY: RYRUBIO-//
//==================================================================================================================================//
//========= SINGLE MSG =============================================================================================================//
//toggle required attribute on email or phone number for single message//
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
    let cache = {};

    let directoryTypeElement = document.getElementById("directory-type");

    let initialType = directoryTypeElement.value;
    fetchAndDisplayData(initialType);

    document.querySelectorAll(".directory-btn").forEach(button => {
        button.addEventListener("click", function () {
            let modal = new bootstrap.Modal(document.getElementById("foxDirectoryModal"));
            modal.show();

            let directoryType = directoryTypeElement.value;
            fetchAndDisplayData(directoryType);

            directoryTypeElement.removeEventListener("change", onDirectoryTypeChange);
            directoryTypeElement.addEventListener("change", onDirectoryTypeChange);
        });
    });

    function onDirectoryTypeChange() {
        let selectedType = this.value;

        document.getElementById("searchBar").value = "";

        fetchAndDisplayData(selectedType);
    }

    function fetchAndDisplayData(type) {
        let tableBody = document.getElementById("directoryTable");

        if (cache[type]) {
            console.log(`Using cached data for ${type}`);
            displayData(cache[type]);
            return;
        }

        tableBody.innerHTML = '<tr><td colspan="3">Loading...</td></tr>';

        let endpoint = type === "external" ? "/display_external_data" : "/display_data";

        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                cache[type] = data;
                displayData(data);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                tableBody.innerHTML = '<tr><td colspan="3">Failed to load data</td></tr>';
            });
    }

    function displayData(data) {
        let tableBody = document.getElementById("directoryTable");
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
    }

    function addRowClickEvent() {
        document.querySelectorAll(".clickable-row").forEach(row => {
            row.addEventListener("click", function () {
                document.getElementById("recipient").value = this.dataset.name;
                document.getElementById("phone").value = this.dataset.mobile;
                document.getElementById("email").value = this.dataset.email;
            });
        });
    }
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
//toggle required attribute on email or phone number for Multi messagge//
function mtoggleRequiredFields() {
    let msendingOption = document.getElementById("msending_option").value;
    let mphoneInput = document.getElementById("mphone");
    let memailInput = document.getElementById("memail");

    // Reset required attributes
    mphoneInput.removeAttribute("required");
    memailInput.removeAttribute("required");

    // Add required based on selection
    if (msendingOption === "sms") {
        mphoneInput.setAttribute("required", "required");
    } else if (msendingOption === "email") {
        memailInput.setAttribute("required", "required");
    }
}
//==================================================================================================================================//
//open directory for Multi messagge //
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".multi_directory-btn").forEach(button => {
        button.addEventListener("click", function () {
            let modal = new bootstrap.Modal(document.getElementById("multi_foxDirectoryModal"));
            modal.show();

            let tableBody = document.getElementById("mdirectoryTable");
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
                            <td><input type="checkbox" class="row-checkbox"></td>
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

                document.getElementById("mrecipient").value = name;
                document.getElementById("mphone").value = mobile;
                document.getElementById("memail").value = email;
            });
        });
    }
});
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
//search directory for Multi message//
document.addEventListener("DOMContentLoaded", function () {
    const searchBar = document.getElementById("msearchBar");

    searchBar.addEventListener("keyup", function () {
        let searchValue = searchBar.value.toLowerCase();
        let tableRows = document.querySelectorAll("#mdirectoryTable tr");

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








