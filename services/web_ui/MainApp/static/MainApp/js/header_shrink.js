document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector(".header");
    const headerLine = document.querySelector(".header-line");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 10) {
            header.classList.add("shrink")
            headerLine.classList.add("shrink-line");
        } else {
            header.classList.remove("shrink")
            headerLine.classList.remove("shrink-line")
        }
    });
});
