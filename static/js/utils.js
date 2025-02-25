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

//Flash Message Auto Hide//
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let flashMessages = document.querySelectorAll(".flash-message");
        flashMessages.forEach(msg => msg.style.display = "none");
    }, 5000); // Hide after 5 seconds
});