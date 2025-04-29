//-JS CODE FOR 'NOTIFS' BY: RYRUBIO-//
//==================================================================================================================================//
//========= SINGLE MSG =============================================================================================================//
//toggle required attribute on email or phone number for single message//
document.addEventListener("DOMContentLoaded", function () {
    let phoneInput = document.getElementById("phone");
    let emailInput = document.getElementById("email");
    let sendingOptionSelect = document.getElementById("sending_option");

    function toggleRequiredFields() {
        let sendingOption = sendingOptionSelect.value;

        phoneInput.removeAttribute("required");
        emailInput.removeAttribute("required");

        if (sendingOption === "sms") {
            phoneInput.setAttribute("required", "required");
        } else if (sendingOption === "email") {
            emailInput.setAttribute("required", "required");
        } else if (sendingOption === "both") {
            phoneInput.setAttribute("required", "required");
            emailInput.setAttribute("required", "required");
        }
    }
    toggleRequiredFields();
    sendingOptionSelect.addEventListener("change", toggleRequiredFields);
});
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

        let endpoint = type === "external" ? "/display_eprocsys_data" : "/display_hrpears_data";

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
        let tableRows = document.querySelectorAll("#directoryTable tr"); 

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
//select message template to message area content single message//
document.getElementById("stemplate").addEventListener("change", function() {
    let s_selectedOption = this.options[this.selectedIndex];
    let s_description = s_selectedOption.getAttribute("data-descS") || "";
    
    document.getElementById("message").value = s_description;
});
//==================================================================================================================================//
//
//
//
//========= MULTI MSG ==============================================================================================================//
//open directory for Multi messagge //
document.addEventListener("DOMContentLoaded", function () {
    let cache = {};
    let directoryTypeElement = document.getElementById("mdirectory-type");
    let initialType = directoryTypeElement.value;
    fetchAndDisplayData(initialType);
    document.querySelectorAll(".multi_directory-btn").forEach(button => {
        button.addEventListener("click", function () {
            let modal = new bootstrap.Modal(document.getElementById("multi_foxDirectoryModal"));
            modal.show();
            let directoryType = directoryTypeElement.value;
            fetchAndDisplayData(directoryType);
            directoryTypeElement.removeEventListener("change", onDirectoryTypeChange);
            directoryTypeElement.addEventListener("change", onDirectoryTypeChange);
        });
    });
    function onDirectoryTypeChange() {
        let selectedType = this.value;
        document.getElementById("msearchBar").value = "";
        fetchAndDisplayData(selectedType);
    }
    function fetchAndDisplayData(type) {
        let tableBody = document.getElementById("mdirectoryTable");
        if (cache[type]) {
            console.log(`Using cached data for ${type}`);
            displayData(cache[type]);
            return;
        }
        tableBody.innerHTML = '<tr><td colspan="4">Loading...</td></tr>';
        let endpoint = type === "external" ? "/display_eprocsys_data" : "/display_hrpears_data";
        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                cache[type] = data;
                displayData(data);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                tableBody.innerHTML = '<tr><td colspan="4">Failed to load data</td></tr>';
            });
    }
    function displayData(data) {
        let tableBody = document.getElementById("mdirectoryTable");
        tableBody.innerHTML = "";
        let list = document.getElementById("mlist").value.split("\n"); 
        data.forEach(row => {
            let entry = `${row.name}:${row.mobile_no}:${row.email}`;
            let checked = list.includes(entry) ? "checked" : ""; 
            let tr = document.createElement("tr");
            tr.classList.add("mclickable-row");
            tr.dataset.name = row.name;
            tr.dataset.mobile = row.mobile_no;
            tr.dataset.email = row.email;
            tr.innerHTML = `
                <td><input type="checkbox" class="row-checkbox" ${checked}></td>
                <td>${row.name}</td>
                <td>${row.mobile_no}</td>
                <td>${row.email}</td>
            `;
            tableBody.appendChild(tr);
        });
        addRowClickEvent();
        addCheckboxChangeEvent();
    }
    function addRowClickEvent() {
        document.querySelectorAll(".mclickable-row").forEach(row => {
            row.addEventListener("click", function (event) {
                if (!event.target.classList.contains("row-checkbox")) { 
                    document.getElementById("mrecipient").value = this.dataset.name;
                    document.getElementById("mphone").value = this.dataset.mobile;
                    document.getElementById("memail").value = this.dataset.email;
                }
            });
        });
    }
    function addCheckboxChangeEvent() {
        document.querySelectorAll(".row-checkbox").forEach(checkbox => {
            checkbox.addEventListener("change", function () {
                let list = document.getElementById("mlist");
                let row = this.closest("tr");
                let entry = `${row.dataset.name}:${row.dataset.mobile}:${row.dataset.email}`;
                let entries = list.value ? list.value.split("\n") : [];

                if (this.checked) {
                    if (!entries.includes(entry)) {
                        entries.push(entry);
                    }
                } else {
                    entries = entries.filter(e => e !== entry);
                }
                list.value = entries.join("\n");
            });
        });
    }
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("msend")) {
            let list = document.getElementById("mlist");
            let selectedEntries = [];
            document.querySelectorAll(".row-checkbox:checked").forEach(checkbox => {
                let row = checkbox.closest("tr");
                let entry = `${row.dataset.name}:${row.dataset.mobile}:${row.dataset.email}`;
                selectedEntries.push(entry);
            });
            if (selectedEntries.length > 0) {
                list.value = selectedEntries.join("\n");
            } else {
                list.value = "";
            }
            document.querySelectorAll(".row-checkbox").forEach(checkbox => {
                checkbox.checked = false;
            });
        }
    });
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
//select message template to message area content multi message//
document.getElementById("mtemplate").addEventListener("change", function() {
    let m_selectedOption = this.options[this.selectedIndex];
    let m_description = m_selectedOption.getAttribute("data-descM") || "";
    
    document.getElementById("mmessage").value = m_description;
});
//==================================================================================================================================//
//
//
//
//========= UPLOAD MSG =============================================================================================================//
//Extract recipient from file upload//
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("searchIcon").addEventListener("click", function () {
        let fileInput = document.getElementById("uploaded");
        let file = fileInput.files[0];

        if (!file) {
            alert("Please upload a file first.");
            return;
        }
        let formData = new FormData();
        formData.append("uploaded", file);

        fetch("/generate_from_upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response from Flask:", data);

            let formattedRecords = data.matched_records.map(record => {
                return `${record.fullname}:${record.mobile}:${record.email}:${record.amount}\n`;
            }).join("");

            let displayRecords = data.matched_records.map(record => {
                return `${record.fullname}:->${record.amount}\n`;
            }).join("");

            document.getElementById("udisplaydata").value = displayRecords || "No data found";
            document.getElementById("ufounddata").value = formattedRecords || "No data found";
            document.getElementById("unodatafound").value = data.unmatched_names.join("\n");
        })
        .catch(error => console.error("Error:", error));
    });
});
//==================================================================================================================================//
//select message template to message area content upload message//
document.getElementById("utemplate").addEventListener("change", function() {
    let u_selectedOption = this.options[this.selectedIndex];
    let u_description = u_selectedOption.getAttribute("data-descU") || "";
    
    document.getElementById("umessage").value = u_description;
});
//==================================================================================================================================//




