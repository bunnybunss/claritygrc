// ===== MULTI-STEP FORM =====
function nextStep(current) {
    const currentStep = document.getElementById(`step${current}`);
    const nextStep = document.getElementById(`step${current + 1}`);

    if (!currentStep || !nextStep) return;

    // Basic validation — check required fields in current step
    const required = currentStep.querySelectorAll('[required]');
    for (let field of required) {
        if (!field.value) {
            field.style.borderColor = '#C0392B';
            field.focus();
            return;
        }
        field.style.borderColor = '';
    }

    currentStep.classList.remove('active');
    nextStep.classList.add('active');
    updateProgress(current + 1);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function prevStep(current) {
    const currentStep = document.getElementById(`step${current}`);
    const prevStep = document.getElementById(`step${current - 1}`);

    if (!currentStep || !prevStep) return;

    currentStep.classList.remove('active');
    prevStep.classList.add('active');
    updateProgress(current - 1);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateProgress(step) {
    const bar = document.getElementById('progressBar');
    if (bar) {
        bar.style.width = `${(step / 4) * 100}%`;
    }
}

// ===== GAUGE =====
function drawGauge(score, color) {
    const canvas = document.getElementById('gaugeCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const cx = 150;
    const cy = 150;
    const radius = 120;

    const colorMap = {
        'green': '#27AE60',
        'yellow': '#B8860B',
        'orange': '#E67E22',
        'red': '#C0392B'
    };

    const gaugeColor = colorMap[color] || '#2E75B6';

    // Clear
    ctx.clearRect(0, 0, 300, 170);

    // Background arc
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, 2 * Math.PI);
    ctx.lineWidth = 20;
    ctx.strokeStyle = '#E0E0E0';
    ctx.stroke();

    // Score arc
    const angle = Math.PI + (score / 100) * Math.PI;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, angle);
    ctx.lineWidth = 20;
    ctx.strokeStyle = gaugeColor;
    ctx.lineCap = 'round';
    ctx.stroke();

    // Labels
    ctx.fillStyle = '#888';
    ctx.font = '13px Segoe UI';
    ctx.textAlign = 'center';
    ctx.fillText('0', cx - radius - 10, cy + 15);
    ctx.fillText('100', cx + radius + 15, cy + 15);
}

// ===== AI EXPLAINER =====
async function getExplanation() {
    const btn = document.getElementById('explainBtn');
    const box = document.getElementById('explanationBox');
    const text = document.getElementById('explanationText');

    if (!btn || !box || !text) return;

    btn.textContent = 'Generating...';
    btn.disabled = true;

    try {
        const response = await fetch('/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(resultData)
        });

        const data = await response.json();

        text.textContent = data.explanation;
        box.style.display = 'block';
        btn.textContent = 'Regenerate';
        btn.disabled = false;

        // Save explanation for PDF
        resultData.explanation = data.explanation;

    } catch (error) {
        text.textContent = 'Something went wrong. Please try again.';
        box.style.display = 'block';
        btn.textContent = 'Try Again';
        btn.disabled = false;
    }
}

// ===== PDF DOWNLOAD =====
async function downloadReport() {
    const btn = event.target;
    btn.textContent = 'Generating PDF...';
    btn.disabled = true;

    try {
        const response = await fetch('/download-report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(resultData)
        });

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ClarityGRC_Report.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        btn.textContent = 'Download PDF Report';
        btn.disabled = false;

    } catch (error) {
        btn.textContent = 'Something went wrong. Try again.';
        btn.disabled = false;
    }
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
    // Draw gauge if on results page
    if (typeof riskScore !== 'undefined' && typeof riskColor !== 'undefined') {
        drawGauge(riskScore, riskColor);
    }
});
// ===== SOA DOWNLOAD =====
async function downloadSoA() {
    const btn = event.target;
    btn.textContent = 'Generating SoA...';
    btn.disabled = true;

    try {
        const response = await fetch('/download-soa', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(resultData)
        });

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ClarityGRC_Statement_of_Applicability.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        btn.textContent = 'Download Statement of Applicability';
        btn.disabled = false;

    } catch (error) {
        btn.textContent = 'Something went wrong. Try again.';
        btn.disabled = false;
    }
}
