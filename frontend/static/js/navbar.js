menuButton = document.querySelector('.menu-button');
navBar = document.querySelector(".links-container");


menuButton.onclick = function() {
    navBar.classList.toggle("active");
}


navBar.addEventListener('click', function(event) {
    if (event.target === navBar) {
        navBar.classList.remove("active");
    }
});

document.addEventListener('click', function(event) {
    if (!menuButton.contains(event.target) && !navBar.contains(event.target)) {
        navBar.classList.remove("active");
    }
});


document.querySelectorAll('.links-container a').forEach(link => {
    link.addEventListener('click', function() {
        navBar.classList.remove("active");
    });
});
