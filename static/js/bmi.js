/**
 * PulseFit Interactive BMI Calculator
 * Supports Metric (cm, kg) and Imperial (ft, in, lbs)
 * Provides real-time BMI score, progress bar visualization, and hydration/calorie recommendations.
 */

document.addEventListener('DOMContentLoaded', () => {
    const bmiForm = document.getElementById('bmiForm');
    if (!bmiForm) return;

    let currentUnit = 'metric'; // 'metric' or 'imperial'

    // Unit toggle buttons
    const btnMetric = document.getElementById('btnMetric');
    const btnImperial = document.getElementById('btnImperial');
    const metricInputs = document.getElementById('metricInputs');
    const imperialInputs = document.getElementById('imperialInputs');

    if (btnMetric && btnImperial) {
        btnMetric.addEventListener('click', () => {
            currentUnit = 'metric';
            btnMetric.classList.add('active');
            btnImperial.classList.remove('active');
            if (metricInputs) metricInputs.style.display = 'block';
            if (imperialInputs) imperialInputs.style.display = 'none';
            calculateBMI();
        });

        btnImperial.addEventListener('click', () => {
            currentUnit = 'imperial';
            btnImperial.classList.add('active');
            btnMetric.classList.remove('active');
            if (metricInputs) metricInputs.style.display = 'none';
            if (imperialInputs) imperialInputs.style.display = 'block';
            calculateBMI();
        });
    }

    // Input change listeners
    const inputs = bmiForm.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', calculateBMI);
    });

    bmiForm.addEventListener('submit', (e) => {
        e.preventDefault();
        calculateBMI();
    });

    function calculateBMI() {
        let weightKg = 0;
        let heightM = 0;
        let bmi = 0;

        if (currentUnit === 'metric') {
            const heightCm = parseFloat(document.getElementById('heightCm')?.value || 0);
            const weight = parseFloat(document.getElementById('weightKg')?.value || 0);

            if (heightCm > 50 && weight > 20) {
                heightM = heightCm / 100;
                weightKg = weight;
                bmi = weight / (heightM * heightM);
            }
        } else {
            const feet = parseFloat(document.getElementById('heightFt')?.value || 0);
            const inches = parseFloat(document.getElementById('heightIn')?.value || 0);
            const lbs = parseFloat(document.getElementById('weightLbs')?.value || 0);

            const totalInches = (feet * 12) + inches;
            if (totalInches > 20 && lbs > 40) {
                bmi = (lbs / (totalInches * totalInches)) * 703;
                weightKg = lbs * 0.453592;
                heightM = totalInches * 0.0254;
            }
        }

        updateUI(bmi, weightKg);
    }

    function updateUI(bmi, weightKg) {
        const scoreEl = document.getElementById('bmiScore');
        const badgeEl = document.getElementById('bmiBadge');
        const barFill = document.getElementById('bmiBarFill');
        const adviceEl = document.getElementById('bmiAdvice');
        const waterEl = document.getElementById('recWater');
        const calEl = document.getElementById('recCalories');

        if (!scoreEl || !badgeEl || !barFill) return;

        if (bmi <= 0 || isNaN(bmi) || !isFinite(bmi)) {
            scoreEl.textContent = '--.-';
            badgeEl.textContent = 'Enter Your Stats';
            badgeEl.className = 'badge badge-gray';
            barFill.style.width = '0%';
            if (adviceEl) adviceEl.textContent = 'Input your height and weight above to reveal your fitness metrics.';
            if (waterEl) waterEl.textContent = '-- L';
            if (calEl) calEl.textContent = '-- kcal';
            return;
        }

        const formattedBMI = bmi.toFixed(1);
        scoreEl.textContent = formattedBMI;

        // Determine category & bar fill percentage (scale: 15 to 35)
        let category = '';
        let badgeClass = '';
        let adviceText = '';
        let percentage = Math.min(Math.max(((bmi - 15) / (35 - 15)) * 100, 5), 100);

        if (bmi < 18.5) {
            category = 'Underweight';
            badgeClass = 'badge badge-cyan';
            adviceText = 'Focus on a nutrient-dense caloric surplus with quality protein and strength training to build muscle mass safely.';
        } else if (bmi < 24.9) {
            category = 'Normal Weight';
            badgeClass = 'badge badge-lime';
            adviceText = 'Your weight is in the optimal healthy range. Continue with progressive resistance workouts and balanced nutrition.';
        } else if (bmi < 29.9) {
            category = 'Overweight';
            badgeClass = 'badge badge-coral';
            adviceText = 'Incorporate a moderate calorie deficit of 300-500 kcal combined with regular resistance workouts and HIIT.';
        } else {
            category = 'Obese Range';
            badgeClass = 'badge badge-coral';
            adviceText = 'Prioritize sustainable whole-food nutrition, low-impact cardio (walking/swimming), and consult a fitness coach.';
        }

        badgeEl.textContent = category;
        badgeEl.className = badgeClass;
        barFill.style.width = `${percentage}%`;

        if (adviceEl) adviceEl.textContent = adviceText;

        // Recommendations
        if (waterEl && weightKg > 0) {
            const dailyWater = (weightKg * 0.035).toFixed(1);
            waterEl.textContent = `${dailyWater} L / day`;
        }

        if (calEl && weightKg > 0) {
            // Rough baseline maintenance calories
            const estCal = Math.round(weightKg * 30);
            calEl.textContent = `~${estCal} kcal`;
        }
    }

    // Trigger initial calculation if defaults exist
    calculateBMI();
});
