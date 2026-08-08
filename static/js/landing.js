document.addEventListener("DOMContentLoaded", () => {

    const authOverlay = document.getElementById("authOverlay");

    function openAuthModal(e) {

        if (e) e.preventDefault();

        if (authOverlay) {

            authOverlay.classList.add("active");
            document.body.style.overflow = "hidden";

        }

    }

    // Hero button
    const heroButton = document.getElementById("openAuth");

    if (heroButton) {

        heroButton.addEventListener("click", openAuthModal);

    }

    // Sidebar button
    const sidebarButton = document.getElementById("sidebarOpenAuth");

    if (sidebarButton) {

        sidebarButton.addEventListener("click", openAuthModal);

    }

});