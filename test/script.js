// test fixture: minimal custom js used by the custom css+js html path
document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("navbar");
    const headers = document.querySelectorAll("h1, h2, h3");
    headers.forEach(header => {
        const id = header.textContent.toLowerCase().replace(/\s+/g, '-');
        header.id = id;
        const anchor = document.createElement("a");
        anchor.href = `#${id}`;
        anchor.textContent = header.textContent;
        navbar.appendChild(anchor);
    });
});
