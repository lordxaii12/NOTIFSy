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

















