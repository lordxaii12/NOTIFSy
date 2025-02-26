
//Delete Logs//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-log-btn").forEach(button => {
        button.addEventListener("click", function () {
            let logId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_logs_route/${logId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});

//Delete Itexmo Credential//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".itexmo-log-btn").forEach(button => {
        button.addEventListener("click", function () {
            let itexmoId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_itexmo/${itexmoId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});

//Delete Email Credential//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".email-log-btn").forEach(button => {
        button.addEventListener("click", function () {
            let emailId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_email_route/${emailId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});

//Delete HRIS Credential//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".hris-log-btn").forEach(button => {
        button.addEventListener("click", function () {
            let hrisId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_hrpears_route/${hrisId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});

//Delete Login Credential//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".login-log-btn").forEach(button => {
        button.addEventListener("click", function () {
            let loginId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_loginapi_route/${loginId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});

//Delete User Credential//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".user-log-btn").forEach(button => {
        button.addEventListener("click", function () {
            let userId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_user_route/${userId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});

//Delete User type Credential//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".role-log-btn").forEach(button => {
        button.addEventListener("click", function () {
            let roleId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_role_route/${roleId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});

//Delete User division Credential//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".division-log-btn").forEach(button => {
        button.addEventListener("click", function () {
            let divisionId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_division_route/${divisionId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});


//Delete Message-logs//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".msg-btn").forEach(button => {
        button.addEventListener("click", function () {
            let msglogId = this.getAttribute("data-log-id");

            if (confirm("Are you sure?")) {
                let form = document.createElement("form");
                form.method = "POST";
                form.action = `/delete_msglogs_route/${msglogId}`;

                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});