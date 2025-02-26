// document.addEventListener("DOMContentLoaded", function () {
//     // Initialize Bootstrap Modals
//     const firstModalEl = document.getElementById("itexmoModal");
//     const firstModal = new bootstrap.Modal(firstModalEl);

//     // Find all edit buttons
//     document.querySelectorAll(".edit-button").forEach(button => {
//         button.addEventListener("click", function () {
//             const modalId = `edititextMoModal${this.getAttribute("data-itexmo-id")}`;
//             const editModalEl = document.getElementById(modalId);
//             const editModal = new bootstrap.Modal(editModalEl);

//             // Show the second modal without closing the first
//             editModalEl.addEventListener("shown.bs.modal", function () {
//                 firstModalEl.classList.add("custom-backdrop"); // Keep first modal visible
//             });

//             editModalEl.addEventListener("hidden.bs.modal", function () {
//                 firstModalEl.classList.remove("custom-backdrop");
//             });

//             editModal.show();
//         });
//     });
// });
