function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {

        document.getElementById("navbar").style.background = "#14213D";
    } else {

        document.getElementById("navbar").style.background = "none";
    }
}

