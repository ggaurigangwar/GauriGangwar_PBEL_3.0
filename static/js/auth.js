// ==========================================
// VitaCare Authentication
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    // Elements
    const authOverlay = document.getElementById("authOverlay");
    const authModal = document.querySelector(".auth-modal");

    const openButtons = document.querySelectorAll(".open-auth-btn");
    const closeAuth = document.getElementById("closeAuth");

    const loginBox = document.getElementById("loginBox");
    const signupBox = document.getElementById("signupBox");

    const showSignup = document.getElementById("showSignup");
    const showLogin = document.getElementById("showLogin");

    // ==========================================
    // Open Modal
    // ==========================================

    function openModal() {

        if (!authOverlay) return;

        authOverlay.classList.add("active");
        document.body.style.overflow = "hidden";

    }

    // ==========================================
    // Close Modal
    // ==========================================

    function closeModal() {

        if (!authOverlay) return;

        authOverlay.classList.remove("active");
        document.body.style.overflow = "auto";

    }

    // ==========================================
    // Open Buttons
    // ==========================================

    openButtons.forEach(button => {

        button.addEventListener("click", openModal);

    });

    // ==========================================
    // Close Button
    // ==========================================

    if (closeAuth) {

        closeAuth.addEventListener("click", closeModal);

    }

    // ==========================================
    // Click Outside Modal
    // ==========================================

    if (authOverlay) {

        authOverlay.addEventListener("click", function (e) {

            if (e.target === authOverlay) {

                closeModal();

            }

        });

    }

    // ==========================================
    // ESC Key
    // ==========================================

    document.addEventListener("keydown", function (e) {

        if (e.key === "Escape") {

            closeModal();

        }

    });

    // ==========================================
    // Switch to Signup
    // ==========================================

    if (showSignup) {

        showSignup.addEventListener("click", function () {

            loginBox.classList.remove("active");
            signupBox.classList.add("active");

        });

    }

    // ==========================================
    // Switch to Login
    // ==========================================

    if (showLogin) {

        showLogin.addEventListener("click", function () {

            signupBox.classList.remove("active");
            loginBox.classList.add("active");

        });

    }

    // ==========================================
    // Password Toggle
    // ==========================================

    const toggleButtons = document.querySelectorAll(".toggle-password");

    toggleButtons.forEach((button) => {

        button.addEventListener("click", function () {

            const input = button.previousElementSibling;
            const icon = button.querySelector("i");

            if (input.type === "password") {

                input.type = "text";

                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");

            }

            else {

                input.type = "password";

                icon.classList.remove("bi-eye-slash");
                icon.classList.add("bi-eye");

            }

        });

    });

});