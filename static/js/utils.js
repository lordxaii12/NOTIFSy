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