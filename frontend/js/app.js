document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initNavigation();
    initModals();
    initBreathingExercise();
    loadView('dashboard');
});

// State Store
const state = {
    currentView: 'dashboard',
    profile: null,
    recommendation: null,
    activities: [],
    medications: [],
    appointments: [],
    chatHistory: [
        {
            sender: 'ai',
            text: 'Greetings, Commander Vance. VitalMind Antigravity AI Assistant operational. How can I assist your zero-g health, workout, or sleep protocol today?',
            disclaimer: 'VitalMind AI provides educational information only, not a medical diagnosis or prescription.'
        }
    ]
};

/* --- Background Particle System --- */
function initParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = Array.from({ length: 45 }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2 + 1,
        color: Math.random() > 0.5 ? 'rgba(0, 242, 254, ' : 'rgba(127, 0, 255, ',
        alpha: Math.random() * 0.5 + 0.2,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4
    }));

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0) p.x = width;
            if (p.x > width) p.x = 0;
            if (p.y < 0) p.y = height;
            if (p.y > height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color + p.alpha + ')';
            ctx.fill();
        });
        requestAnimationFrame(animate);
    }
    animate();
}

/* --- Navigation Router --- */
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetView = btn.getAttribute('data-view');
            navItems.forEach(i => i.classList.remove('active'));
            btn.classList.add('active');
            loadView(targetView);
        });
    });
}

function loadView(viewName) {
    state.currentView = viewName;
    const container = document.getElementById('viewContainer');
    const pageTitle = document.getElementById('pageTitle');

    switch (viewName) {
        case 'dashboard':
            pageTitle.textContent = 'Orbital Telemetry Dashboard';
            renderDashboard(container);
            break;
        case 'fitness':
            pageTitle.textContent = 'Antigravity Resistance & Osteo Protocol';
            renderFitness(container);
            break;
        case 'wellness':
            pageTitle.textContent = 'Zero-G Wellness & Sleep Pod Tracker';
            renderWellness(container);
            break;
        case 'mental':
            pageTitle.textContent = 'Mental Health & Zero-G CBT Module';
            renderMentalHealth(container);
            break;
        case 'medications':
            pageTitle.textContent = 'Space Medication Adherence';
            renderMedications(container);
            break;
        case 'appointments':
            pageTitle.textContent = 'Station CMO Consultations';
            renderAppointments(container);
            break;
        case 'ai-assistant':
            pageTitle.textContent = 'VitalMind Antigravity AI Assistant';
            renderAIChat(container);
            break;
        case 'profile':
            pageTitle.textContent = 'Crew Member Health Profile';
            renderProfile(container);
            break;
        default:
            renderDashboard(container);
    }
}

/* --- Global Modals --- */
function initModals() {
    const emergencyBtn = document.getElementById('emergencyBtn');
    const emergencyModal = document.getElementById('emergencyModal');
    const closeEmergency = document.getElementById('closeEmergencyModal');

    emergencyBtn.addEventListener('click', () => emergencyModal.classList.remove('hidden'));
    closeEmergency.addEventListener('click', () => emergencyModal.classList.add('hidden'));

    const closeBreathing = document.getElementById('closeBreathingModal');
    if (closeBreathing) {
        closeBreathing.addEventListener('click', () => {
            document.getElementById('breathingModal').classList.add('hidden');
        });
    }
}

/* --- Guided Breathing Logic --- */
let breathingInterval = null;
function initBreathingExercise() {
    const startBtn = document.getElementById('startBreathingBtn');
    const stopBtn = document.getElementById('stopBreathingBtn');
    const circle = document.getElementById('breathingCircle');
    const instruction = document.getElementById('breathingInstruction');

    if (!startBtn) return;

    startBtn.addEventListener('click', () => {
        let phase = 0;
        circle.className = 'breathing-circle inhale';
        instruction.textContent = 'Inhale';

        if (breathingInterval) clearInterval(breathingInterval);
        breathingInterval = setInterval(() => {
            phase = (phase + 1) % 4;
            if (phase === 0) {
                circle.className = 'breathing-circle inhale';
                instruction.textContent = 'Inhale (4s)';
            } else if (phase === 1) {
                circle.className = 'breathing-circle inhale';
                instruction.textContent = 'Hold (4s)';
            } else if (phase === 2) {
                circle.className = 'breathing-circle exhale';
                instruction.textContent = 'Exhale (4s)';
            } else {
                circle.className = 'breathing-circle exhale';
                instruction.textContent = 'Rest (4s)';
            }
        }, 4000);
    });

    stopBtn.addEventListener('click', () => {
        if (breathingInterval) clearInterval(breathingInterval);
        circle.className = 'breathing-circle';
        instruction.textContent = 'Inhale';
    });
}

function openBreathingModal() {
    document.getElementById('breathingModal').classList.remove('hidden');
}

/* --- 1. Dashboard View --- */
async function renderDashboard(container) {
    container.innerHTML = `<div class="text-center p-5"><i class="fa-solid fa-spinner fa-spin fa-2x"></i><p>Loading Orbital Telemetry...</p></div>`;

    try {
        const [rec, activities, meds, appts] = await Promise.all([
            API.getRecommendation(),
            API.getActivities(),
            API.getMedications(),
            API.getAppointments()
        ]);
        state.recommendation = rec;
        state.activities = activities;
        state.medications = meds;
        state.appointments = appts;

        const hr = activities.find(a => a.activity_type === 'hr')?.value || 72;
        const spo2 = activities.find(a => a.activity_type === 'spo2')?.value || 98;
        const sleep = activities.find(a => a.activity_type === 'sleep')?.value || 7.4;
        const work = activities.find(a => a.activity_type === 'work_kj')?.value || 950;

        container.innerHTML = `
            <!-- Telemetry Metrics Grid -->
            <div class="grid-4">
                <div class="glass-card telemetry-card">
                    <div class="telemetry-icon cyan"><i class="fa-solid fa-heart-pulse"></i></div>
                    <div class="telemetry-data">
                        <h3>${hr} <span class="unit">bpm</span></h3>
                        <p>Heart Rate Telemetry</p>
                    </div>
                </div>
                <div class="glass-card telemetry-card">
                    <div class="telemetry-icon blue"><i class="fa-solid fa-lungs"></i></div>
                    <div class="telemetry-data">
                        <h3>${spo2}% <span class="unit">SpO2</span></h3>
                        <p>Blood Oxygen Saturation</p>
                    </div>
                </div>
                <div class="glass-card telemetry-card">
                    <div class="telemetry-icon violet"><i class="fa-solid fa-bed"></i></div>
                    <div class="telemetry-data">
                        <h3>${sleep} <span class="unit">hrs</span></h3>
                        <p>Sleep Pod Efficiency</p>
                    </div>
                </div>
                <div class="glass-card telemetry-card">
                    <div class="telemetry-icon emerald"><i class="fa-solid fa-bolt"></i></div>
                    <div class="telemetry-data">
                        <h3>${work} <span class="unit">kJ</span></h3>
                        <p>ARED Work Equivalent</p>
                    </div>
                </div>
            </div>

            <!-- AI Recommendation Banner -->
            <div class="glass-card recommendation-banner">
                <div class="banner-header">
                    <span class="banner-tag">AI ANTIGRAVITY RECOMMENDATION</span>
                    <button class="btn btn-secondary" onclick="loadView('fitness')">View Full Protocol</button>
                </div>
                <h2 class="banner-title">${rec.title}</h2>
                <p class="banner-desc">${rec.summary}</p>
                <div class="protocol-list">
                    ${rec.exercise_protocol.map(p => `<div class="protocol-chip"><i class="fa-solid fa-check"></i> ${p}</div>`).join('')}
                </div>
            </div>

            <!-- Two Column Layout: Quick Log & Schedule -->
            <div class="grid-2">
                <div class="glass-card">
                    <h3><i class="fa-solid fa-plus-circle"></i> Quick Telemetry & Mood Logger</h3>
                    <p style="color:var(--text-muted); margin-bottom:16px; font-size:14px;">Log daily zero-g metrics to keep the recommendation engine updated.</p>
                    <form id="quickLogForm">
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px;">
                            <div>
                                <label style="font-size:12px; color:var(--text-muted);">Heart Rate (bpm)</label>
                                <input type="number" id="logHr" value="75" class="chat-input" style="width:100%;">
                            </div>
                            <div>
                                <label style="font-size:12px; color:var(--text-muted);">Sleep Pod Hours</label>
                                <input type="number" step="0.1" id="logSleep" value="7.5" class="chat-input" style="width:100%;">
                            </div>
                        </div>
                        <div style="margin-bottom:14px;">
                            <label style="font-size:12px; color:var(--text-muted);">Current Mood Score (1-10)</label>
                            <input type="range" id="logMood" min="1" max="10" value="8" style="width:100%; accent-color:var(--primary-cyan);">
                        </div>
                        <button type="submit" class="btn btn-primary btn-block"><i class="fa-solid fa-cloud-arrow-up"></i> Submit Telemetry</button>
                    </form>
                </div>

                <div class="glass-card">
                    <h3><i class="fa-solid fa-calendar-check"></i> Station Schedule</h3>
                    <div style="margin-top:16px; display:flex; flex-direction:column; gap:12px;">
                        <div style="background:rgba(255,255,255,0.04); padding:12px; border-radius:10px; border-left:3px solid var(--primary-cyan);">
                            <span style="font-size:11px; color:var(--primary-cyan); font-weight:600;">ACTIVE MEDICATION</span>
                            <div style="font-weight:600; font-size:14px; margin-top:2px;">Calcium + Vitamin D3</div>
                            <span style="font-size:12px; color:var(--text-muted);">08:00 UTC - Osteopenia Prevention</span>
                        </div>
                        <div style="background:rgba(255,255,255,0.04); padding:12px; border-radius:10px; border-left:3px solid var(--primary-violet);">
                            <span style="font-size:11px; color:var(--primary-violet); font-weight:600;">UPCOMING CMO APPOINTMENT</span>
                            <div style="font-weight:600; font-size:14px; margin-top:2px;">Dr. Aris Thorne (CMO)</div>
                            <span style="font-size:12px; color:var(--text-muted);">Sept 8, 14:30 UTC - Bone Densitometry</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('quickLogForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const hr = parseFloat(document.getElementById('logHr').value);
            const sleep = parseFloat(document.getElementById('logSleep').value);
            await API.addActivity({ activity_type: 'hr', value: hr, unit: 'bpm', source: 'Manual Dashboard' });
            await API.addActivity({ activity_type: 'sleep', value: sleep, unit: 'hours', source: 'Manual Dashboard' });
            alert('Telemetry successfully updated!');
            renderDashboard(container);
        });

    } catch (e) {
        container.innerHTML = `<div class="glass-card text-center"><p>Error loading dashboard metrics: ${e.message}</p></div>`;
    }
}

/* --- 2. Antigravity Fitness View --- */
async function renderFitness(container) {
    const rec = state.recommendation || await API.getRecommendation();
    container.innerHTML = `
        <div class="glass-card recommendation-banner">
            <h2>${rec.title}</h2>
            <p>${rec.summary}</p>
        </div>

        <div class="grid-2">
            <div class="glass-card">
                <h3><i class="fa-solid fa-list-check"></i> Today's Zero-G Exercise Protocol</h3>
                <div style="margin-top:16px; display:flex; flex-direction:column; gap:12px;">
                    ${rec.exercise_protocol.map((item, idx) => `
                        <div style="background:rgba(255,255,255,0.04); padding:14px; border-radius:12px; display:flex; align-items:center; justify-content:space-between; border:1px solid var(--border-color);">
                            <div style="display:flex; align-items:center; gap:12px;">
                                <div style="width:28px; height:28px; background:var(--primary-cyan); color:#090c15; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:12px;">${idx + 1}</div>
                                <span style="font-size:14px; font-weight:500;">${item}</span>
                            </div>
                            <input type="checkbox" style="width:20px; height:20px; accent-color:var(--primary-cyan);">
                        </div>
                    `).join('')}
                </div>
            </div>

            <div class="glass-card text-center">
                <h3><i class="fa-solid fa-stopwatch"></i> ARED Workout Session Timer</h3>
                <div style="font-size:42px; font-family:var(--font-heading); font-weight:700; color:var(--primary-cyan); margin:20px 0;" id="workoutTimer">45:00</div>
                <div style="display:flex; gap:10px; justify-content:center;">
                    <button class="btn btn-primary" onclick="alert('Workout timer started! Focus on eccentric ARED load.')"><i class="fa-solid fa-play"></i> Start Session</button>
                    <button class="btn btn-secondary" onclick="alert('Work logged to telemetry!')"><i class="fa-solid fa-check"></i> Complete Workout</button>
                </div>
                <div style="margin-top:24px; padding-top:16px; border-top:1px solid var(--border-color); text-align:left;">
                    <h4 style="font-size:13px; color:var(--primary-blue);">OSTEOPENIA PREVENTION ADVICE</h4>
                    <p style="font-size:12px; color:var(--text-muted); margin-top:4px;">Microgravity reduces mechanical load on axial skeleton. ARED vacuum pistons provide up to 600 lbs of resistance force to preserve bone mineral density.</p>
                </div>
            </div>
        </div>
    `;
}

/* --- 3. Wellness & Sleep View --- */
function renderWellness(container) {
    container.innerHTML = `
        <div class="grid-2">
            <div class="glass-card">
                <h3><i class="fa-solid fa-moon"></i> Sleep Pod Circadian Light Simulator</h3>
                <p style="color:var(--text-muted); font-size:14px; margin-bottom:16px;">In microgravity, 16 orbital sunrises daily require strict light wavelength control in sleep quarters.</p>
                <div style="display:flex; gap:12px; margin-bottom:20px;">
                    <button class="btn btn-secondary" style="background:#ff1744; color:#fff;" onclick="alert('Circadian Pod Light set to Deep Red Spectrum (Melatonin Secretion On)')"><i class="fa-solid fa-lightbulb"></i> Red Spectrum (Pre-Sleep)</button>
                    <button class="btn btn-secondary" style="background:#00f2fe; color:#090c15;" onclick="alert('Circadian Pod Light set to Bright Cyan Spectrum (Wake Alertness On)')"><i class="fa-solid fa-sun"></i> Cyan Spectrum (Wake)</button>
                </div>

                <h3><i class="fa-solid fa-bottle-water"></i> Microgravity Hydration Tracker</h3>
                <div style="margin-top:12px; background:rgba(255,255,255,0.04); padding:16px; border-radius:12px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span>Daily Hydration Goal (2.5L)</span>
                        <span style="color:var(--primary-cyan); font-weight:700;">1.8L / 2.5L</span>
                    </div>
                    <div style="height:10px; background:rgba(255,255,255,0.1); border-radius:5px; overflow:hidden;">
                        <div style="width:72%; height:100%; background:linear-gradient(90deg, var(--primary-cyan), var(--primary-blue));"></div>
                    </div>
                    <button class="btn btn-secondary btn-block" style="margin-top:12px;" onclick="alert('Added 250mL mineralized water pouch to telemetry!')">+ Add 250mL Pouch</button>
                </div>
            </div>

            <div class="glass-card">
                <h3><i class="fa-solid fa-spa"></i> Zero-G Spinal Decompression</h3>
                <p style="color:var(--text-muted); font-size:13px; margin-bottom:16px;">Without gravity, intervertebral discs expand by up to 7cm, causing mild back ache.</p>
                <div style="display:flex; flex-direction:column; gap:10px;">
                    <div class="protocol-chip"><i class="fa-solid fa-check"></i> Knee-to-chest tether stretch (10 mins)</div>
                    <div class="protocol-chip"><i class="fa-solid fa-check"></i> Thoracic axial extension in crew module</div>
                    <div class="protocol-chip"><i class="fa-solid fa-check"></i> Sleeping bag tension strap adjustments</div>
                </div>
            </div>
        </div>
    `;
}

/* --- 4. Mental Health & CBT View --- */
function renderMentalHealth(container) {
    container.innerHTML = `
        <div class="grid-2">
            <div class="glass-card">
                <h3><i class="fa-solid fa-clipboard-question"></i> Orbital PHQ-2 / GAD-2 Wellness Screener</h3>
                <p style="color:var(--text-muted); font-size:13px; margin-bottom:16px;">This 4-question check-in screens orbital stress and emotional balance. (Wellness tool, not diagnostic).</p>

                <form id="riskScreenForm">
                    <div style="margin-bottom:14px;">
                        <label style="font-size:13px; font-weight:600;">1. Feeling down, depressed, or hopeless in orbit?</label>
                        <select id="q1" class="chat-input" style="width:100%; margin-top:4px;">
                            <option value="0">0 - Not at all</option>
                            <option value="1">1 - Several days</option>
                            <option value="2">2 - More than half the days</option>
                            <option value="3">3 - Nearly every day</option>
                        </select>
                    </div>

                    <div style="margin-bottom:14px;">
                        <label style="font-size:13px; font-weight:600;">2. Little interest or pleasure in daily station tasks?</label>
                        <select id="q2" class="chat-input" style="width:100%; margin-top:4px;">
                            <option value="0">0 - Not at all</option>
                            <option value="1">1 - Several days</option>
                            <option value="2">2 - More than half the days</option>
                            <option value="3">3 - Nearly every day</option>
                        </select>
                    </div>

                    <div style="margin-bottom:14px;">
                        <label style="font-size:13px; font-weight:600;">3. Feeling nervous, anxious, or on edge?</label>
                        <select id="q3" class="chat-input" style="width:100%; margin-top:4px;">
                            <option value="0">0 - Not at all</option>
                            <option value="1">1 - Several days</option>
                            <option value="2">2 - More than half the days</option>
                            <option value="3">3 - Nearly every day</option>
                        </select>
                    </div>

                    <div style="margin-bottom:14px;">
                        <label style="font-size:13px; font-weight:600;">4. Trouble relaxing or managing station stressors?</label>
                        <select id="q4" class="chat-input" style="width:100%; margin-top:4px;">
                            <option value="0">0 - Not at all</option>
                            <option value="1">1 - Several days</option>
                            <option value="2">2 - More than half the days</option>
                            <option value="3">3 - Nearly every day</option>
                        </select>
                    </div>

                    <button type="submit" class="btn btn-primary btn-block"><i class="fa-solid fa-magnifying-glass-chart"></i> Submit Screener</button>
                </form>
            </div>

            <div class="glass-card">
                <h3><i class="fa-solid fa-wind"></i> Guided Zero-G Breathing</h3>
                <p style="color:var(--text-muted); font-size:13px; margin-bottom:16px;">Lower heart rate and reduce stress scores with box breathing in microgravity.</p>
                <button class="btn btn-primary btn-block" onclick="openBreathingModal()"><i class="fa-solid fa-play"></i> Open Guided Breathing Tool</button>

                <div id="riskResultBox" class="hidden" style="margin-top:20px; padding:16px; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid var(--border-glowing);">
                    <!-- Screen results pop up here -->
                </div>
            </div>
        </div>
    `;

    document.getElementById('riskScreenForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const res = await API.screenRisk({
            q1_down: parseInt(document.getElementById('q1').value),
            q2_pleasure: parseInt(document.getElementById('q2').value),
            q3_anxious: parseInt(document.getElementById('q3').value),
            q4_relax: parseInt(document.getElementById('q4').value)
        });

        const box = document.getElementById('riskResultBox');
        box.classList.remove('hidden');
        box.innerHTML = `
            <span style="font-size:11px; font-weight:700; color:var(--primary-cyan);">${res.risk_tier.toUpperCase()} (${res.total_score}/12)</span>
            <h4 style="font-size:16px; margin:4px 0;">${res.title}</h4>
            <p style="font-size:13px; color:var(--text-muted); line-height:1.4;">${res.message}</p>
            <div style="margin-top:10px;">
                <strong>Recommended Actions:</strong>
                <ul style="padding-left:18px; font-size:12px; color:var(--text-muted); margin-top:4px;">
                    ${res.recommended_actions.map(a => `<li>${a}</li>`).join('')}
                </ul>
            </div>
        `;
    });
}

/* --- 5. Space Medications View --- */
async function renderMedications(container) {
    const meds = await API.getMedications();
    container.innerHTML = `
        <div class="glass-card" style="margin-bottom:24px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3><i class="fa-solid fa-pills"></i> Active Medication Schedule</h3>
                <button class="btn btn-primary" onclick="promptAddMed()"><i class="fa-solid fa-plus"></i> Add Medication</button>
            </div>
        </div>

        <div class="grid-2">
            ${meds.map(m => `
                <div class="glass-card" style="border-left:4px solid ${m.is_taken_today ? 'var(--accent-emerald)' : 'var(--accent-warning)'};">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <div>
                            <h4 style="font-size:18px;">${m.name}</h4>
                            <span style="font-size:13px; color:var(--primary-cyan);">${m.dosage} - ${m.frequency}</span>
                            <p style="font-size:12px; color:var(--text-muted); margin-top:6px;">Scheduled: ${m.schedule_time}</p>
                            <p style="font-size:12px; color:var(--text-muted);">${m.notes || ''}</p>
                        </div>
                        <button class="btn ${m.is_taken_today ? 'btn-secondary' : 'btn-primary'}" onclick="toggleMed(${m.id})">
                            ${m.is_taken_today ? '<i class="fa-solid fa-circle-check"></i> Taken Today' : 'Mark as Taken'}
                        </button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

window.toggleMed = async function(id) {
    await API.toggleMedication(id);
    renderMedications(document.getElementById('viewContainer'));
};

window.promptAddMed = async function() {
    const name = prompt('Medication Name (e.g. Scopolamine Patch):');
    if (!name) return;
    const dosage = prompt('Dosage (e.g. 25mg):', '25mg');
    await API.addMedication({ name, dosage, frequency: 'Daily', schedule_time: '12:00 UTC', notes: 'Added by crew member' });
    renderMedications(document.getElementById('viewContainer'));
};

/* --- 6. CMO Appointments View --- */
async function renderAppointments(container) {
    const appts = await API.getAppointments();
    container.innerHTML = `
        <div class="glass-card" style="margin-bottom:24px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3><i class="fa-solid fa-user-doctor"></i> Station CMO Consultations</h3>
                <button class="btn btn-primary" onclick="promptAddAppt()"><i class="fa-solid fa-calendar-plus"></i> Schedule Consultation</button>
            </div>
        </div>

        <div class="grid-2">
            ${appts.map(a => `
                <div class="glass-card" style="border-left:4px solid var(--primary-violet);">
                    <h4 style="font-size:18px;">${a.doctor_name}</h4>
                    <span style="font-size:13px; color:var(--primary-blue);">${a.specialty}</span>
                    <p style="font-size:13px; margin-top:8px;"><strong>Date/Time:</strong> ${a.appointment_date} at ${a.appointment_time}</p>
                    <p style="font-size:12px; color:var(--text-muted); margin-top:4px;">${a.notes || ''}</p>
                    <div style="margin-top:12px;">
                        <span class="protocol-chip" style="background:rgba(0,230,118,0.15); color:var(--accent-emerald); border:none;">Status: ${a.status}</span>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

window.promptAddAppt = async function() {
    const date = prompt('Appointment Date (YYYY-MM-DD):', '2026-09-12');
    if (!date) return;
    await API.addAppointment({
        doctor_name: 'Dr. Aris Thorne',
        specialty: 'Chief Medical Officer (CMO)',
        appointment_date: date,
        appointment_time: '15:00 UTC',
        notes: 'Routine crew check-in'
    });
    renderAppointments(document.getElementById('viewContainer'));
};

/* --- 7. AI Assistant Chat View --- */
function renderAIChat(container) {
    container.innerHTML = `
        <div class="chat-container">
            <div class="chat-header">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div class="logo-icon" style="width:36px; height:36px; font-size:16px;"><i class="fa-solid fa-robot"></i></div>
                    <div>
                        <h4 style="font-size:16px;">VitalMind Antigravity AI</h4>
                        <span style="font-size:11px; color:var(--accent-emerald);">Safety & Policy Layer Active</span>
                    </div>
                </div>
                <span class="protocol-chip" style="font-size:11px; border-color:var(--border-glowing);">Microgravity Persona Enabled</span>
            </div>

            <div class="chat-messages" id="chatMessages">
                ${state.chatHistory.map(msg => `
                    <div class="chat-bubble ${msg.sender} ${msg.safety_flag === 'MEDICAL_EMERGENCY' ? 'emergency' : ''}">
                        <div>${msg.text.replace(/\n/g, '<br>')}</div>
                        ${msg.disclaimer ? `<div class="chat-disclaimer">${msg.disclaimer}</div>` : ''}
                    </div>
                `).join('')}
            </div>

            <div class="quick-replies">
                <button class="chip-btn" onclick="sendQuickReply('How did I sleep this week?')">How did I sleep this week?</button>
                <button class="chip-btn" onclick="sendQuickReply('Suggest today\'s zero-g workout')">Suggest today's zero-g workout</button>
                <button class="chip-btn" onclick="sendQuickReply('I\'m feeling stressed in orbit')">I'm feeling stressed in orbit</button>
                <button class="chip-btn" onclick="sendQuickReply('How do I adapt ARED resistance?')">How do I adapt ARED resistance?</button>
            </div>

            <form id="chatForm" class="chat-input-area">
                <input type="text" id="chatInput" class="chat-input" placeholder="Ask VitalMind AI about zero-g workouts, sleep, or stress..." autocomplete="off">
                <button type="submit" class="btn btn-primary"><i class="fa-solid fa-paper-plane"></i> Send</button>
            </form>
        </div>
    `;

    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;

    document.getElementById('chatForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = document.getElementById('chatInput');
        const q = input.value.trim();
        if (!q) return;

        input.value = '';
        state.chatHistory.push({ sender: 'user', text: q });
        renderAIChat(container);

        try {
            const res = await API.sendAIChat(q);
            state.chatHistory.push({
                sender: 'ai',
                text: res.response,
                safety_flag: res.safety_flag,
                disclaimer: res.safety_flag === 'SAFE' ? 'VitalMind AI provides educational information only, not a medical diagnosis.' : ''
            });
        } catch (err) {
            state.chatHistory.push({
                sender: 'ai',
                text: 'Connection error communicating with VitalMind AI service. Please check telemetry link.'
            });
        }
        renderAIChat(container);
    });
}

window.sendQuickReply = function(text) {
    const input = document.getElementById('chatInput');
    if (input) {
        input.value = text;
        document.getElementById('chatForm').dispatchEvent(new Event('submit'));
    }
};

/* --- 8. Profile View --- */
async function renderProfile(container) {
    const profile = await API.getProfile();
    container.innerHTML = `
        <div class="grid-2">
            <div class="glass-card">
                <h3><i class="fa-solid fa-user-gear"></i> Orbital Health Profile</h3>
                <p style="color:var(--text-muted); font-size:13px; margin-bottom:18px;">Single source of truth for physiological monitoring and AI personalization.</p>
                <form id="profileForm">
                    <div style="margin-bottom:12px;">
                        <label style="font-size:12px; color:var(--text-muted);">Station Role & Rank</label>
                        <input type="text" id="pRole" value="${profile.station_role}" class="chat-input" style="width:100%;">
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">
                        <div>
                            <label style="font-size:12px; color:var(--text-muted);">Age</label>
                            <input type="number" id="pAge" value="${profile.age}" class="chat-input" style="width:100%;">
                        </div>
                        <div>
                            <label style="font-size:12px; color:var(--text-muted);">Blood Group</label>
                            <input type="text" id="pBlood" value="${profile.blood_group}" class="chat-input" style="width:100%;">
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">
                        <div>
                            <label style="font-size:12px; color:var(--text-muted);">Height (cm)</label>
                            <input type="number" id="pHeight" value="${profile.height_cm}" class="chat-input" style="width:100%;">
                        </div>
                        <div>
                            <label style="font-size:12px; color:var(--text-muted);">Earth Weight (kg)</label>
                            <input type="number" step="0.1" id="pWeight" value="${profile.weight_kg}" class="chat-input" style="width:100%;">
                        </div>
                    </div>
                    <div style="margin-bottom:12px;">
                        <label style="font-size:12px; color:var(--text-muted);">Known Allergies</label>
                        <input type="text" id="pAllergies" value="${profile.allergies}" class="chat-input" style="width:100%;">
                    </div>
                    <div style="margin-bottom:16px;">
                        <label style="font-size:12px; color:var(--text-muted);">Zero-G Medical History</label>
                        <textarea id="pHistory" class="chat-input" style="width:100%; height:80px;">${profile.medical_history}</textarea>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block"><i class="fa-solid fa-floppy-disk"></i> Update Profile</button>
                </form>
            </div>

            <div class="glass-card">
                <h3><i class="fa-solid fa-shield-halved"></i> Privacy & Responsible AI Policy</h3>
                <div style="margin-top:14px; font-size:13px; color:var(--text-muted); display:flex; flex-direction:column; gap:12px; line-height:1.5;">
                    <div class="protocol-chip"><i class="fa-solid fa-lock"></i> AES-256 On-Device Telemetry Encryption</div>
                    <div class="protocol-chip"><i class="fa-solid fa-user-shield"></i> Non-Diagnostic AI Assistant Limits</div>
                    <div class="protocol-chip"><i class="fa-solid fa-kit-medical"></i> Station CMO Automatic Escalation Protocol</div>
                    <p>All physiological data collected is processed according to zero-g bio-safety guidelines and HIPAA/GDPR space privacy standards.</p>
                </div>
            </div>
        </div>
    `;

    document.getElementById('profileForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await API.updateProfile({
            station_role: document.getElementById('pRole').value,
            age: parseInt(document.getElementById('pAge').value),
            blood_group: document.getElementById('pBlood').value,
            height_cm: parseFloat(document.getElementById('pHeight').value),
            weight_kg: parseFloat(document.getElementById('pWeight').value),
            allergies: document.getElementById('pAllergies').value,
            medical_history: document.getElementById('pHistory').value
        });
        alert('Profile saved!');
    });
}
