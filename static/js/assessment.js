/**
 * MediAI 2.0 — 4-Step Clinical Assessment Wizard & Real-Time Symptom Matrix
 */

document.addEventListener("DOMContentLoaded", function () {
    let currentStep = 1;
    const totalSteps = 4;

    // Elements
    const stepPanels = document.querySelectorAll(".wizard-step-panel");
    const stepNodes = document.querySelectorAll(".wizard-step-node");
    const prevBtn = document.getElementById("wizardPrevBtn");
    const nextBtn = document.getElementById("wizardNextBtn");
    const submitBtn = document.getElementById("wizardSubmitBtn");
    const assessmentForm = document.getElementById("clinicalAssessmentForm");

    // Vitals inputs
    const heightInput = document.getElementById("height");
    const weightInput = document.getElementById("weight");
    const tempInput = document.getElementById("temperature");
    const spo2Input = document.getElementById("spo2");

    // Symptom search & filter
    const searchInput = document.getElementById("symptomSearch");
    const categoryBtns = document.querySelectorAll(".cat-filter-btn");
    const symptomChips = document.querySelectorAll(".symptom-chip");
    const selectedCountDisplay = document.getElementById("selectedSymptomCount");
    const clearAllBtn = document.getElementById("clearSymptomsBtn");

    /* ==========================================================================
       1. STEP NAVIGATION
       ========================================================================== */
    function showStep(step) {
        currentStep = step;

        stepPanels.forEach((panel, idx) => {
            if (idx + 1 === step) {
                panel.classList.add("active");
            } else {
                panel.classList.remove("active");
            }
        });

        stepNodes.forEach((node, idx) => {
            const stepNum = idx + 1;
            node.classList.remove("active", "completed");
            if (stepNum === step) {
                node.classList.add("active");
            } else if (stepNum < step) {
                node.classList.add("completed");
            }
        });

        // Button states
        if (prevBtn) {
            prevBtn.style.display = step === 1 ? "none" : "inline-flex";
        }
        if (nextBtn) {
            nextBtn.style.display = step === totalSteps ? "none" : "inline-flex";
        }
        if (submitBtn) {
            submitBtn.style.display = step === totalSteps ? "inline-flex" : "none";
        }

        // Scroll to wizard top
        const wizardCard = document.querySelector(".wizard-progress-bar-wrap");
        if (wizardCard) {
            wizardCard.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }

    function validateStep(step) {
        if (step === 1) {
            const name = document.getElementById("name");
            const age = document.getElementById("age");
            const gender = document.getElementById("gender");
            if (!name.value.trim() || !age.value || !gender.value) {
                alert("Please enter patient name, age, and select a gender before proceeding.");
                return false;
            }
        } else if (step === 3) {
            const checkedSymptoms = document.querySelectorAll('input[name="symptoms"]:checked');
            const otherSymptoms = document.getElementById("other_symptoms");
            if (checkedSymptoms.length === 0 && (!otherSymptoms || !otherSymptoms.value.trim())) {
                alert("Please select at least one symptom or describe your symptoms before proceeding.");
                return false;
            }
        }
        return true;
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", function () {
            if (validateStep(currentStep)) {
                if (currentStep < totalSteps) {
                    showStep(currentStep + 1);
                }
            }
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", function () {
            if (currentStep > 1) {
                showStep(currentStep - 1);
            }
        });
    }

    stepNodes.forEach((node, idx) => {
        node.addEventListener("click", function () {
            const targetStep = idx + 1;
            if (targetStep < currentStep || validateStep(currentStep)) {
                showStep(targetStep);
            }
        });
    });

    /* ==========================================================================
       2. REAL-TIME VITALS CALCULATION
       ========================================================================== */
    function updateVitalsCalculations() {
        const h = parseFloat(heightInput ? heightInput.value : 170) || 170;
        const w = parseFloat(weightInput ? weightInput.value : 65) || 65;
        const temp = parseFloat(tempInput ? tempInput.value : 0);
        const spo2 = parseInt(spo2Input ? spo2Input.value : 0);

        // BMI
        if (h > 0 && w > 0) {
            const bmi = (w / ((h / 100) * (h / 100))).toFixed(1);
            const liveBmiVal = document.getElementById("liveBmiVal");
            const liveBmiBadge = document.getElementById("liveBmiBadge");
            if (liveBmiVal) liveBmiVal.textContent = bmi;
            if (liveBmiBadge) {
                if (bmi < 18.5) {
                    liveBmiBadge.textContent = "Underweight";
                    liveBmiBadge.style.color = "var(--warning)";
                } else if (bmi < 25) {
                    liveBmiBadge.textContent = "Normal";
                    liveBmiBadge.style.color = "var(--success)";
                } else if (bmi < 30) {
                    liveBmiBadge.textContent = "Overweight";
                    liveBmiBadge.style.color = "var(--warning)";
                } else {
                    liveBmiBadge.textContent = "Obese";
                    liveBmiBadge.style.color = "var(--danger)";
                }
            }
        }

        // Temp
        const liveTempVal = document.getElementById("liveTempVal");
        const liveTempBadge = document.getElementById("liveTempBadge");
        if (liveTempVal && liveTempBadge) {
            if (temp > 0) {
                liveTempVal.textContent = temp.toFixed(1) + "°C";
                if (temp < 37.3) {
                    liveTempBadge.textContent = "Normal";
                    liveTempBadge.style.color = "var(--success)";
                } else if (temp < 38.5) {
                    liveTempBadge.textContent = "Mild Fever";
                    liveTempBadge.style.color = "var(--warning)";
                } else {
                    liveTempBadge.textContent = "High Fever";
                    liveTempBadge.style.color = "var(--danger)";
                }
            } else {
                liveTempVal.textContent = "--";
                liveTempBadge.textContent = "Not Provided";
            }
        }

        // SpO2
        const liveSpo2Val = document.getElementById("liveSpo2Val");
        const liveSpo2Badge = document.getElementById("liveSpo2Badge");
        if (liveSpo2Val && liveSpo2Badge) {
            if (spo2 > 0) {
                liveSpo2Val.textContent = spo2 + "%";
                if (spo2 >= 95) {
                    liveSpo2Badge.textContent = "Optimal";
                    liveSpo2Badge.style.color = "var(--success)";
                } else if (spo2 >= 92) {
                    liveSpo2Badge.textContent = "Caution";
                    liveSpo2Badge.style.color = "var(--warning)";
                } else {
                    liveSpo2Badge.textContent = "Hypoxia";
                    liveSpo2Badge.style.color = "var(--danger)";
                }
            } else {
                liveSpo2Val.textContent = "--";
                liveSpo2Badge.textContent = "Not Provided";
            }
        }
    }

    if (heightInput) heightInput.addEventListener("input", updateVitalsCalculations);
    if (weightInput) weightInput.addEventListener("input", updateVitalsCalculations);
    if (tempInput) tempInput.addEventListener("input", updateVitalsCalculations);
    if (spo2Input) spo2Input.addEventListener("input", updateVitalsCalculations);

    /* ==========================================================================
       3. 130+ SYMPTOM SEARCH & CATEGORY FILTERING
       ========================================================================== */
    function updateSelectedCount() {
        const count = document.querySelectorAll('input[name="symptoms"]:checked').length;
        if (selectedCountDisplay) {
            selectedCountDisplay.textContent = count;
        }
    }

    symptomChips.forEach(chip => {
        const checkbox = chip.querySelector('input[type="checkbox"]');
        chip.addEventListener("click", function (e) {
            if (e.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
            }
            if (checkbox.checked) {
                chip.classList.add("selected");
            } else {
                chip.classList.remove("selected");
            }
            updateSelectedCount();
        });
    });

    if (clearAllBtn) {
        clearAllBtn.addEventListener("click", function () {
            symptomChips.forEach(chip => {
                const cb = chip.querySelector('input[type="checkbox"]');
                if (cb) cb.checked = false;
                chip.classList.remove("selected");
            });
            updateSelectedCount();
        });
    }

    function filterSymptoms() {
        const query = (searchInput ? searchInput.value.toLowerCase().trim() : "");
        const activeCat = document.querySelector(".cat-filter-btn.active");
        const category = activeCat ? activeCat.dataset.cat : "all";

        symptomChips.forEach(chip => {
            const name = chip.dataset.name.toLowerCase();
            const cat = chip.dataset.cat;

            const matchesQuery = !query || name.includes(query);
            const matchesCat = category === "all" || cat === category;

            if (matchesQuery && matchesCat) {
                chip.style.display = "flex";
            } else {
                chip.style.display = "none";
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener("input", filterSymptoms);
    }

    categoryBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            categoryBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            filterSymptoms();
        });
    });

    // Check for pre-selected symptoms in URL query (e.g. from 3D Anatomy explorer)
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get("category");
    if (categoryParam) {
        const targetBtn = document.querySelector(`.cat-filter-btn[data-cat="${categoryParam}"]`);
        if (targetBtn) {
            targetBtn.click();
            showStep(3);
        }
    }

    // Initial state
    showStep(1);
    updateVitalsCalculations();
    updateSelectedCount();
});
