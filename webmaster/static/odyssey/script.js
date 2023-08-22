//collapses/uncollapses navbar on scroll
var prevScrollpos = window.pageYOffset;
function navbarScroll() {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("navbar").style.top = "0";
        document.getElementById("chat-toggle").style.right = "50px";
    } else {
        document.getElementById("chat-toggle").style.right = "-100px";
        document.getElementById("navbar").style.top = "-100px";
    }
    prevScrollpos = currentScrollPos;
}

//changes transparency and color of navbar on scroll
function scrollFunction() {
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        document.getElementById("navbar").style.backdropFilter = "blur(1rem)";
        document.getElementById("navbar").style.background = "hsl(0 0% 100% / 0.1)";
    } else {
        document.getElementById("navbar").style.backdropFilter = "none";
        document.getElementById("navbar").style.background = "none";

    }
}

function toggleChat() {
    var chat = document.getElementById("chat-container");
    if (chat.style.display == "block") {
        chat.style.display = "none";
        chat.classList.toggle("animate-expand");
    }
    else {
        chat.style.display = "block";
        chat.classList.toggle("animate-expand");
    }
}

//makes elements fade in on scroll
function fadeIn() {
    var pageTop = $(document).scrollTop();
    var pageBottom = pageTop + $(window).height();
    var tags = $(".fadeIn");

    for (var i = 0; i < tags.length; i++) {
        var tag = tags[i];
        if ($(tag).position().top < pageBottom) {
            $(tag).addClass("visible");
        } else {
            $(tag).removeClass("visible");
        }
    }
}