/**
 * MediAI 2.0 — Core Platform Scripts
 * Includes 3D Card Tilt, Theme Engine, Mobile Drawer & Live Calculators
 */

document.addEventListener("DOMContentLoaded", function () {
    initThemeToggle();
    initMobileNav();
    init3DCardTilt();
    initHomeCalculators();
    initSmoothScroll();
});

/* ==========================================================================
   1. THEME ENGINE & TOGGLE
   ========================================================================== */
function initThemeToggle() {
    const toggleBtn = document.getElementById("themeToggleBtn");
    if (!toggleBtn) return;

    toggleBtn.addEventListener("click", function () {
        const currentTheme = document.documentElement.dataset.theme || "dark";
        const newTheme = currentTheme === "dark" ? "light" : "dark";

        document.documentElement.dataset.theme = newTheme;
        try {
            localStorage.setItem("mediai-theme", newTheme);
        } catch (e) {
            console.warn("Storage unavailable");
        }
    });
}

/* ==========================================================================
   2. MOBILE NAVIGATION DRAWER
   ========================================================================== */
function initMobileNav() {
    const menuBtn = document.getElementById("mobileMenuBtn");
    const drawer = document.getElementById("mobileDrawer");
    if (!menuBtn || !drawer) return;

    menuBtn.addEventListener("click", function () {
        const isOpen = drawer.classList.toggle("open");
        menuBtn.classList.toggle("active");
        menuBtn.setAttribute("aria-expanded", isOpen);
    });

    // Close when clicking any link
    const mobileLinks = drawer.querySelectorAll(".mobile-link");
    mobileLinks.forEach(link => {
        link.addEventListener("click", () => {
            drawer.classList.remove("open");
            menuBtn.classList.remove("active");
            menuBtn.setAttribute("aria-expanded", "false");
        });
    });
}

/* ==========================================================================
   3. 3D CARD TILT & SPECULAR GLARE
   ========================================================================== */
function init3DCardTilt() {
    const tiltCards = document.querySelectorAll(".anatomy-card, .calc-card, .floating-hud, .diag-gauge-card");

    tiltCards.forEach(card => {
        card.addEventListener("mousemove", function (e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -7;
            const rotateY = ((x - centerX) / centerX) * 7;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });

        card.addEventListener("mouseleave", function () {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)`;
        });
    });
}

/* ==========================================================================
   4. INTERACTIVE HOMEPAGE CALCULATORS
   ========================================================================== */
function initHomeCalculators() {
    // BMI & BMR Live Calculator
    const heightInput = document.getElementById("calcHeight");
    const weightInput = document.getElementById("calcWeight");
    const ageInput = document.getElementById("calcAge");

    const bmiValDisplay = document.getElementById("calcBmiVal");
    const bmiStatusDisplay = document.getElementById("calcBmiStatus");
    const bmrValDisplay = document.getElementById("calcBmrVal");
    const hydrationValDisplay = document.getElementById("calcHydrationVal");

    function updateCalculations() {
        if (!heightInput || !weightInput || !bmiValDisplay) return;

        const h = parseFloat(heightInput.value) || 170;
        const w = parseFloat(weightInput.value) || 68;
        const a = parseInt(ageInput ? ageInput.value : 30) || 30;

        if (h > 0 && w > 0) {
            const hM = h / 100.0;
            const bmi = (w / (hM * hM)).toFixed(1);
            bmiValDisplay.textContent = bmi;

            let status = "Normal";
            let color = "var(--success)";
            if (bmi < 18.5) {
                status = "Underweight";
                color = "var(--warning)";
            } else if (bmi >= 30) {
                status = "Obese";
                color = "var(--danger)";
            } else if (bmi >= 25) {
                status = "Overweight";
                color = "var(--warning)";
            }

            if (bmiStatusDisplay) {
                bmiStatusDisplay.textContent = status;
                bmiStatusDisplay.style.color = color;
            }

            if (bmrValDisplay) {
                const bmr = Math.round((10 * w) + (6.25 * h) - (5 * a) + 5);
                bmrValDisplay.textContent = bmr + " kcal";
            }

            if (hydrationValDisplay) {
                const hyd = (w * 0.035).toFixed(1);
                hydrationValDisplay.textContent = hyd + " L / day";
            }
        }
    }

    if (heightInput) heightInput.addEventListener("input", updateCalculations);
    if (weightInput) weightInput.addEventListener("input", updateCalculations);
    if (ageInput) ageInput.addEventListener("input", updateCalculations);
}

/* ==========================================================================
   5. SMOOTH SCROLLING
   ========================================================================== */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const href = this.getAttribute("href");
            if (href === "#") return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });
}