const hamBurger = document.querySelector(".toggle-btn");
const mainHeading = document.getElementById("main-heading");
const mainContent = document.getElementById("main-content");

hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});
