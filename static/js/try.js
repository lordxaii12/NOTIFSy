
























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

        let endpoint = type === "external" ? "/display_external_data" : "/display_data";

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

        let list = document.getElementById("mlist").value.split("\n"); // Get existing entries

        data.forEach(row => {
            let entry = `${row.name}:${row.mobile_no}:${row.email}`;
            let checked = list.includes(entry) ? "checked" : ""; // Check if already in mlist

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

            // Clear all checkboxes
            document.querySelectorAll(".row-checkbox").forEach(checkbox => {
                checkbox.checked = false;
            });

            // Clear input fields
            document.getElementById("mrecipient").value = "";
            document.getElementById("mphone").value = "";
            document.getElementById("memail").value = "";
        }
    });
});


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
        let tableBody = document.getElementById("mdirectoryTable");
        tableBody.innerHTML = "";

        data.forEach(row => {
            let tr = document.createElement("tr");
            tr.classList.add("mclickable-row");
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
    }

    function addRowClickEvent() {
        document.querySelectorAll(".mclickable-row").forEach(row => {
            row.addEventListener("click", function () {
                document.getElementById("mrecipient").value = this.dataset.name;
                document.getElementById("mphone").value = this.dataset.mobile;
                document.getElementById("memail").value = this.dataset.email;
            });
        });
    }

    // Function to handle "OK" button click using .msend class
    document.querySelector(".msend").addEventListener("click", function () {
        let mrecipient = document.getElementById("mrecipient").value;
        let mmobile = document.getElementById("mphone").value;
        let memail = document.getElementById("memail").value;
        let list = document.getElementById("mlist");

        if (recipient && mobile && email) {
            let entry = `${mrecipient}:${mmobile}:${memail}`;
            list.value = list.value ? list.value + "\n" + entry : entry;
        }

        // Clear input fields
        document.getElementById("mrecipient").value = "";
        document.getElementById("mphone").value = "";
        document.getElementById("memail").value = "";
    });
});

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
        let tableBody = document.getElementById("mdirectoryTable");
        tableBody.innerHTML = "";

        data.forEach(row => {
            let tr = document.createElement("tr");
            tr.classList.add("mclickable-row");
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
    }

    function addRowClickEvent() {
        document.querySelectorAll(".mclickable-row").forEach(row => {
            row.addEventListener("click", function () {
                document.getElementById("mrecipient").value = this.dataset.name;
                document.getElementById("mphone").value = this.dataset.mobile;
                document.getElementById("memail").value = this.dataset.email;
            });
        });
    }
});

















