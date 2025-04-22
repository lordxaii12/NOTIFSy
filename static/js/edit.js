//-JS CODE FOR 'NOTIFS' BY: RYRUBIO-//
//==================================================================================================================================//
//Edit Email API Credentials Table//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit_email-btn").forEach(button => {
        button.addEventListener("click", function () {
            let emid = this.getAttribute("data-emid");
            let ename = this.getAttribute("data-name");
            let email = this.getAttribute("data-email");
            let sender = this.getAttribute("data-sender");
            let password = this.getAttribute("data-password");

            document.getElementById("ecreds_id").value = emid;
            document.getElementById("ecreds_name").value = ename;
            document.getElementById("ecreds_email").value = email;
            document.getElementById("ecreds_sender").value = sender;
            document.getElementById("ecreds_password").value = password;

            document.getElementById("email_editForm").action = `/edit_email_route/${emid}`;
            new bootstrap.Modal(document.getElementById("email_edit")).show();
        });
    });
});
//==================================================================================================================================//
//Edit HRIS API Credentials Table Table//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit_hris-btn").forEach(button => {
        button.addEventListener("click", function () {

            let hrid = this.getAttribute("data-hrid");
            let hrname = this.getAttribute("data-hrname");
            let host = this.getAttribute("data-host");
            let root = this.getAttribute("data-root");
            let user = this.getAttribute("data-user");
            let password = this.getAttribute("data-password");
            let db = this.getAttribute("data-db");
            let table = this.getAttribute("data-table");
           
            document.getElementById("hrpears_id").value = hrid;
            document.getElementById("hrpears_name").value = hrname;
            document.getElementById("hrpears_host").value = host;
            document.getElementById("hrpears_root").value = root;
            document.getElementById("hrpears_user").value = user;
            document.getElementById("hrpears_password").value = password;
            document.getElementById("hrpears_dbname").value = db;
            document.getElementById("hrpears_table").value = table;
            
            document.getElementById("hris_editForm").action = `/edit_hrpears_route/${hrid}`;
            
            new bootstrap.Modal(document.getElementById("hris_edit")).show();
        });
    });
});
//==================================================================================================================================//
//Edit ITEXMO API Credentials Table//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit_itexmo-btn").forEach(button => {
        button.addEventListener("click", function () {
            let txtid = this.getAttribute("data-txtid");
            let txtname = this.getAttribute("data-txtname");
            let txturl = this.getAttribute("data-txturl");
            let txtemail = this.getAttribute("data-txtemail");
            let txtpassword = this.getAttribute("data-txtpassword");
            let txtapicode = this.getAttribute("data-txtapicode");
            let txtcontenttype = this.getAttribute("data-txtcontenttype");
           
            document.getElementById("itexmo_id").value = txtid;
            document.getElementById("itexmo_name").value = txtname;
            document.getElementById("itexmo_url").value = txturl;
            document.getElementById("itexmo_email").value = txtemail;
            document.getElementById("itexmo_password").value = txtpassword;
            document.getElementById("itexmo_apicode").value = txtapicode;
            document.getElementById("itexmo_contenttype").value = txtcontenttype;
            
            document.getElementById("itextmo_editForm").action = `/edit_itexmo_route/${txtid}`;
            
            new bootstrap.Modal(document.getElementById("itextmo_edit")).show();
        });
    });
});
//==================================================================================================================================//
//Edit LOGIN API Credentials Table//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit_login-btn").forEach(button => {
        button.addEventListener("click", function () {

            let logid = this.getAttribute("data-logid");
            let logname = this.getAttribute("data-logname");
            let logurl = this.getAttribute("data-logurl");
            let logtoken = this.getAttribute("data-logtoken");
            let logcontenttype = this.getAttribute("data-logcontenttype");

            document.getElementById("login_api_id").value = logid;
            document.getElementById("login_api_name").value = logname;
            document.getElementById("login_api_url").value = logurl;
            document.getElementById("login_api_token").value = logtoken;
            document.getElementById("login_api_content_type").value = logcontenttype;
           
            document.getElementById("login_editForm").action = `/edit_loginapi_route/${logid}`;
            new bootstrap.Modal(document.getElementById("login_edit")).show();
        });
    });
});
//==================================================================================================================================//
//Edit User Data Table//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit_user-btn").forEach(button => {
        button.addEventListener("click", function () {
            let uid = this.getAttribute("data-uid");
            let fname = this.getAttribute("data-fname");
            let rid = this.getAttribute("data-rid");

            document.getElementById("user_id").value = uid;
            document.getElementById("full_name").value = fname;
            document.getElementById("role_id").value = rid;
            
            document.getElementById("user_editForm").action = `/edit_user_route/${uid}`;
            
            new bootstrap.Modal(document.getElementById("user_edit")).show();
        });
    });
});
//==================================================================================================================================//
//Edit User Role Table//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit_role-btn").forEach(button => {
        button.addEventListener("click", function () {
            let rid = this.getAttribute("data-rid");
            let rname = this.getAttribute("data-rname");
            let rdesc = this.getAttribute("data-rdesc");

            document.getElementById("role_id").value = rid;
            document.getElementById("role_name").value = rname;
            document.getElementById("role_description").value = rdesc;

            document.getElementById("role_editForm").action = `/edit_role_route/${rid}`;

            new bootstrap.Modal(document.getElementById("role_edit")).show();
        });
    });
});
//==================================================================================================================================//
//Edit User Divisions Table//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit_division-btn").forEach(button => {
        button.addEventListener("click", function () {
            let did = this.getAttribute("data-did");
            let dname = this.getAttribute("data-dname");
            let ddesc = this.getAttribute("data-ddesc");

            document.getElementById("division_id").value = did;
            document.getElementById("division_name").value = dname;
            document.getElementById("division_description").value = ddesc;

            document.getElementById("division_editForm").action = `/edit_division_route/${did}`;

            new bootstrap.Modal(document.getElementById("division_edit")).show();
        });
    });
});

//==================================================================================================================================//
//Edit Message Templates Table//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit_msg_temp-btn").forEach(button => {
        button.addEventListener("click", function () {
            let mtid = this.getAttribute("data-mtid");
            let mtname = this.getAttribute("data-mtname");
            let mtdesc = this.getAttribute("data-mtdesc");

            document.getElementById("msg_temp_id").value = mtid;
            document.getElementById("msg_temp_name").value = mtname;
            document.getElementById("msg_temp_description").value = mtdesc;

            document.getElementById("msgTemp_editForm").action = `/edit_msg_temp_route/${mtid}`;

            new bootstrap.Modal(document.getElementById("msg_temp_edit")).show();
        });
    });
});
//==================================================================================================================================//