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
//Spinner and result display single send message//
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('send_single_msg');
    const spinner = document.getElementById('singleloadingSpinner');
    const submitBtn = document.getElementById('submitBtnSingle');
    const formFieldsWrapper = document.querySelector('.form-fields-wrapper');

    if (form) {
        form.addEventListener('submit', function () {
            spinner.classList.remove('d-none');
            submitBtn.disabled = true;

            if (formFieldsWrapper) {
                formFieldsWrapper.style.display = 'none';
            }

            sessionStorage.setItem('showResultModal', 'true');
        });
    }

    const shouldShowModal = sessionStorage.getItem('showResultModal') === 'true';

    if (typeof singletotalSent !== 'undefined' && singletotalSent !== null &&
        typeof singletotalUnsent !== 'undefined' && singletotalUnsent !== null &&
        shouldShowModal) {

        const icon = document.getElementById('singleresultIcon');
        const messageText = document.getElementById('singleresultMessage');

        icon.textContent = singletotalUnsent === 0 ? '✅' : '❌';
        messageText.textContent = `Sent: ${singletotalSent}, Unsent: ${singletotalUnsent}`;

        const resultModal = new bootstrap.Modal(document.getElementById('singleresultModal'));
        resultModal.show();

        sessionStorage.removeItem('showResultModal');
    }
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
//Spinner and result display multi send message//
document.addEventListener('DOMContentLoaded', function () {
    const form2 = document.getElementById('send_multi_msg');
    const spinner2 = document.getElementById('multiloadingSpinner');
    const submitBtn2 = document.getElementById('submitBtnMulti');
    const formFieldsWrapper2 = document.querySelector('.form-fields-wrapper2');
    const formFieldsWrapper3 = document.querySelector('.form-fields-wrapper3');

    if (form2) {
        form2.addEventListener('submit', function () {
            spinner2.classList.remove('d-none');
            submitBtn2.disabled = true;

            if (formFieldsWrapper2) {
                formFieldsWrapper2.style.display = 'none';
            }
            if (formFieldsWrapper3) {
                formFieldsWrapper3.style.display = 'none';
            }

            sessionStorage.setItem('showResultModal', 'true');
        });
    }

    const shouldShowModal2 = sessionStorage.getItem('showResultModal') === 'true';

    if (typeof multitotalSent !== 'undefined' && multitotalSent !== null &&
        typeof multitotalUnsent !== 'undefined' && multitotalUnsent !== null &&
        shouldShowModal2) {

        const icon2 = document.getElementById('multiresultIcon');
        const messageText2 = document.getElementById('multiresultMessage');

        icon2.textContent = multitotalUnsent === 0 ? '✅' : '❌';
        messageText2.textContent = `Sent: ${multitotalSent}, Unsent: ${multitotalUnsent}`;

        const resultModal2 = new bootstrap.Modal(document.getElementById('multiresultModal'));
        resultModal2.show();

        sessionStorage.removeItem('showResultModal');
    }
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
//Spinner and result display upload send message//
document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const totalSent = params.get('total_sent');
    const totalUnsent = params.get('total_unsent');
    const totalContents = params.get('total_contents');

    const uploadLoadingModalEl = document.getElementById('uploadLoadingModal');
    const uploadLoadingText = document.getElementById('uploadLoadingText');
    const uploadResultModalEl = document.getElementById('uploadresultModal');
    const uploadResultMessage = document.getElementById('uploadresultMessage');

    // Debug: Log current params
    console.log("Redirect Params:", {
        totalSent,
        totalUnsent,
        totalContents
    });

    // Clear sessionStorage on form submit so modals can appear again on next send
    const form = document.getElementById('send_upload_msg');
    if (form) {
        form.addEventListener('submit', () => {
            sessionStorage.removeItem('uploadShown');
        });
    }

    // Only show loading modal if upload session hasn't already been shown
    if (uploadLoadingModalEl && !sessionStorage.getItem('uploadShown') && totalContents !== null) {
        const uploadLoadingModal = new bootstrap.Modal(uploadLoadingModalEl, {
            backdrop: 'static',
            keyboard: false
        });
        uploadLoadingModal.show();

        // Set loading text after a short delay
        setTimeout(() => {
            if (uploadLoadingText) {
                uploadLoadingText.textContent = `Processing (${totalContents} messages)...`;
            }
        }, 3000);

        // Prevent showing again during this session
        sessionStorage.setItem('uploadShown', 'true');

        // Show result modal after simulated delay
        setTimeout(() => {
            uploadLoadingModal.hide();

            if (uploadResultModalEl && uploadResultMessage) {
                uploadResultMessage.textContent = `Sent: ${totalSent}, Unsent: ${totalUnsent}`;
                const resultModal = new bootstrap.Modal(uploadResultModalEl);
                resultModal.show();
            }
        }, 5000); // Total 5 seconds to simulate processing
    } else if (uploadResultModalEl && !sessionStorage.getItem('uploadShown') && (totalSent || totalUnsent)) {
        // Show only result modal (in case loading modal is skipped)
        uploadResultMessage.textContent = `Sent: ${totalSent}, Unsent: ${totalUnsent}`;
        const resultModal = new bootstrap.Modal(uploadResultModalEl);
        resultModal.show();
        sessionStorage.setItem('uploadShown', 'true');
    }
});

//==================================================================================================================================//




