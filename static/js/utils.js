//-JS CODE FOR 'NOTIFS' BY: RYRUBIO-//
//==================================================================================================================================//
//Pop Over Display//
document.addEventListener("DOMContentLoaded", function () {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    
    popoverTriggerList.forEach(function (popoverTriggerEl) {
        var popover = new bootstrap.Popover(popoverTriggerEl, {
            trigger: "hover", // Changes the trigger from 'click' to 'hover'
            placement: "bottom", // Adjust placement if needed
            container: "body" // Ensures proper positioning
        });
    });
});
//==================================================================================================================================//
//Flash Message Auto Hide//
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let flashMessages = document.querySelectorAll(".flash-message");
        flashMessages.forEach(msg => msg.style.display = "none");
    }, 5000); // Hide after 5 seconds
});
//==================================================================================================================================//
//Modal back drop auto removal after closing//
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("hidden.bs.modal", function () {
        document.querySelectorAll(".modal-backdrop").forEach(backdrop => {
            backdrop.remove();
        });
        document.body.classList.remove("modal-open");
    });
});
//==================================================================================================================================//
//Theme options button change from Activate-Active//
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".submit-btn").forEach(button => {
        button.addEventListener("click", function () {
            let themeId = this.getAttribute("data-theme-id");

            document.getElementById("theme_id").value = themeId;
            document.getElementById("themeForm").action = `/select_theme/${themeId}`;
            document.getElementById("themeForm").submit();
        });
    });
}); 
//==================================================================================================================================//

