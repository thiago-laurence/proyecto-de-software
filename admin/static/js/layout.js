window.addEventListener("scroll", function() {
    const header = document.querySelector(".sticky-header");
    const scrollY = window.scrollY;

    if (scrollY > 100) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }
});