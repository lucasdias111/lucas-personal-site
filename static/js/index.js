const divIDs = ["portfolio", "about", "contact"]
var currentlyOpen = null

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
        currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}

function toggleMenu(menuQuery) {
    if (currentlyOpen != null) {
        if (currentlyOpen == menuQuery) {
            $("#" + currentlyOpen).slideUp("slow");
            currentlyOpen = null
        }
        else if (menuQuery == "home") {
            $("#" + currentlyOpen).slideUp("slow");
            currentlyOpen = null
        }
        else {
            $("#" + currentlyOpen).slideUp("slow", function() {
                $("#" + menuQuery).slideDown("slow");
            });
            currentlyOpen = menuQuery
        }
    }
    else if (menuQuery == "home") {
        null
    }
    else {
        $("#" + menuQuery).slideDown("slow");
        currentlyOpen = menuQuery
    }
}

$("#home-menu").click(function () {
    toggleMenu("home")
})

$("#portfolio-menu").click(function () {
    toggleMenu("portfolio")
});

$("#contact-menu").click(function () {
    toggleMenu("contact")
});

$("#about-menu").click(function () {
    toggleMenu("about")
});

$(".menu-close").click(function (){
    toggleMenu("home")
})

$(".navbar-toggler").click(function (){
    $(".title").fadeToggle();
    $(".profile-image").fadeToggle();
})