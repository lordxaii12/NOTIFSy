//-JS CODE FOR 'NOTIFS' BY: RYRUBIO-//
//==================================================================================================================================//
//========= REGISTER USER =============================================================================================================//
//open user directory for registration//
document.addEventListener("DOMContentLoaded", function () {
    let cache = {};

    // Initial fetch
    fetchAndDisplayData();

    // Show modal and fetch data on button click
    document.querySelectorAll(".user_directory-btn").forEach(button => {
        button.addEventListener("click", function () {
            let modal = new bootstrap.Modal(document.getElementById("userDirectoryModal"));
            modal.show();
            fetchAndDisplayData(); // No type needed
        });
    });

    function fetchAndDisplayData() {
        let tableBody = document.getElementById("userdirectoryTable");

        if (cache["data"]) {
            console.log("Using cached data");
            displayData(cache["data"]);
            return;
        }

        tableBody.innerHTML = '<tr><td colspan="3">Loading...</td></tr>';

        fetch("/display_users_data") // Just one endpoint now
            .then(response => response.json())
            .then(data => {
                cache["data"] = data;
                displayData(data);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                tableBody.innerHTML = '<tr><td colspan="3">Failed to load data</td></tr>';
            });
    }

    function displayData(data) {
        let tableBody = document.getElementById("userdirectoryTable");
        tableBody.innerHTML = "";

        data.forEach(row => {
            let tr = document.createElement("tr");
            tr.classList.add("clickable-row");
            tr.dataset.name = row.name;
            tr.dataset.username = row.username;
            tr.dataset.division = row.division;
            tr.dataset.section = row.section;
            tr.dataset.email = row.email;
            tr.innerHTML = `
                <td>${row.name}</td>
            `;
            tableBody.appendChild(tr);
        });

        addRowClickEvent();
    }

    function addRowClickEvent() {
        document.querySelectorAll(".clickable-row").forEach(row => {
            row.addEventListener("click", function () {
                // Hide directory modal
                bootstrap.Modal.getInstance(document.getElementById("userDirectoryModal")).hide();

                // Wait for a short delay to ensure transition is smooth
                setTimeout(() => {
                    // Show the example modal
                    const formModal = new bootstrap.Modal(document.getElementById("addUserModal"));
                    formModal.show();

                    // Populate form fields
                    document.getElementById("ufull_name").value = this.dataset.name;
                    document.getElementById("uusername").value = this.dataset.username;
                    document.getElementById("udivision").value = this.dataset.division;
                    document.getElementById("usection").value = this.dataset.section;
                    document.getElementById("uemail").value = this.dataset.email;
                }, 500);
            });
        });
    }
});
//==================================================================================================================================//
//search directory for user//
document.addEventListener("DOMContentLoaded", function () {
    const searchBar = document.getElementById("user_searchBar");

    searchBar.addEventListener("keyup", function () {
        let searchValue = searchBar.value.toLowerCase();
        let tableRows = document.querySelectorAll("#userdirectoryTable tr"); 

        tableRows.forEach(row => {
            let name = row.dataset.name ? row.dataset.name.toLowerCase() : "";

            if (name.includes(searchValue)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});
//==================================================================================================================================//
