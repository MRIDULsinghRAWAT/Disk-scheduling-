/**
 * Disk Physical & Linear Track Visualizer
 * Renders an animated mechanical disk platter + pivot actuator arm,
 * along with a horizontal cylinder ruler with request markers and head glow.
 */

export class DiskVisualizer {
  constructor(canvasId, rulerContainerId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.rulerContainer = document.getElementById(rulerContainerId);
    this.currentTrack = 0;
    this.targetTrack = 0;
    this.maxCylinder = 199;
    this.requests = [];
    this.visitedTracks = [];
    this.rotationAngle = 0;
    this.isSpinning = true;
    this.animationFrameId = null;

    if (this.canvas) {
      this.initCanvasSize();
      window.addEventListener('resize', () => this.initCanvasSize());
      this.startPlatterSpin();
    }
  }

  initCanvasSize() {
    if (!this.canvas) return;
    const rect = this.canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    if (this.ctx) {
      this.ctx.scale(dpr, dpr);
    }
    this.width = rect.width;
    this.height = rect.height;
    this.draw();
  }

  startPlatterSpin() {
    const loop = () => {
      if (this.isSpinning) {
        this.rotationAngle = (this.rotationAngle + 0.02) % (Math.PI * 2);
        // Smoothly interpolate currentTrack towards targetTrack for animated arm seek
        if (Math.abs(this.currentTrack - this.targetTrack) > 0.1) {
          this.currentTrack += (this.targetTrack - this.currentTrack) * 0.15;
        } else {
          this.currentTrack = this.targetTrack;
        }
        this.draw();
      }
      this.animationFrameId = requestAnimationFrame(loop);
    };
    this.animationFrameId = requestAnimationFrame(loop);
  }

  setParameters(maxCylinder, requests, initialHead) {
    this.maxCylinder = maxCylinder;
    this.requests = [...requests];
    this.currentTrack = initialHead;
    this.targetTrack = initialHead;
    this.visitedTracks = [initialHead];
    this.renderRuler();
    this.draw();
  }

  seekTo(track, isServiced = true) {
    this.targetTrack = track;
    if (isServiced && !this.visitedTracks.includes(track)) {
      this.visitedTracks.push(track);
    }
    this.updateRulerHead(track);
  }

  reset(initialHead) {
    this.currentTrack = initialHead;
    this.targetTrack = initialHead;
    this.visitedTracks = [initialHead];
    this.renderRuler();
    this.draw();
  }

  draw() {
    if (!this.ctx || !this.width || !this.height) return;
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    ctx.clearRect(0, 0, w, h);

    // Hard Drive Chasis Background
    const chasisRadius = Math.min(w, h) * 0.44;
    const centerX = w * 0.42;
    const centerY = h * 0.5;

    // Outer drive enclosure gradient
    const encGrad = ctx.createRadialGradient(centerX, centerY, chasisRadius * 0.2, centerX, centerY, chasisRadius * 1.08);
    encGrad.addColorStop(0, '#111827');
    encGrad.addColorStop(0.85, '#0b0f19');
    encGrad.addColorStop(1, '#030712');

    ctx.save();
    ctx.beginPath();
    ctx.arc(centerX, centerY, chasisRadius * 1.05, 0, Math.PI * 2);
    ctx.fillStyle = encGrad;
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#1e293b';
    ctx.stroke();

    // Metallic disk platter
    const platterRadius = chasisRadius * 0.92;
    const platterGrad = ctx.createRadialGradient(centerX, centerY, platterRadius * 0.1, centerX, centerY, platterRadius);
    platterGrad.addColorStop(0, '#1e293b');
    platterGrad.addColorStop(0.3, '#334155');
    platterGrad.addColorStop(0.6, '#1e293b');
    platterGrad.addColorStop(0.9, '#475569');
    platterGrad.addColorStop(1, '#0f172a');

    ctx.beginPath();
    ctx.arc(centerX, centerY, platterRadius, 0, Math.PI * 2);
    ctx.fillStyle = platterGrad;
    ctx.fill();
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#64748b';
    ctx.stroke();

    // Concentric track lines (magnetic surface tracks)
    const minTrackRadius = platterRadius * 0.32;
    const maxTrackRadius = platterRadius * 0.94;
    const numTrackRings = 7;

    for (let i = 0; i <= numTrackRings; i++) {
      const r = minTrackRadius + ((maxTrackRadius - minTrackRadius) / numTrackRings) * i;
      ctx.beginPath();
      ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.07)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // Rotating platter reflection sheen
    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.rotate(this.rotationAngle);

    const sheenGrad = ctx.createLinearGradient(-platterRadius, -platterRadius, platterRadius, platterRadius);
    sheenGrad.addColorStop(0, 'rgba(255, 255, 255, 0.08)');
    sheenGrad.addColorStop(0.48, 'rgba(255, 255, 255, 0)');
    sheenGrad.addColorStop(0.52, 'rgba(56, 189, 248, 0.12)');
    sheenGrad.addColorStop(1, 'rgba(255, 255, 255, 0.04)');

    ctx.beginPath();
    ctx.arc(0, 0, platterRadius * 0.98, 0, Math.PI * 2);
    ctx.fillStyle = sheenGrad;
    ctx.fill();
    ctx.restore();

    // Active Cylinder Highlight Ring on Platter
    const trackRatio = this.maxCylinder > 0 ? (this.currentTrack / this.maxCylinder) : 0;
    // 0 is innermost or outermost? Standard HDD track 0 is outermost, but inverted or linear representation works:
    const activeRadius = minTrackRadius + (maxTrackRadius - minTrackRadius) * (1 - trackRatio);

    ctx.beginPath();
    ctx.arc(centerX, centerY, activeRadius, 0, Math.PI * 2);
    ctx.strokeStyle = '#00f2fe';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#00f2fe';
    ctx.shadowBlur = 10;
    ctx.stroke();
    ctx.shadowBlur = 0; // reset shadow

    // Spindle Hub
    const hubRadius = platterRadius * 0.22;
    const hubGrad = ctx.createRadialGradient(centerX, centerY, hubRadius * 0.1, centerX, centerY, hubRadius);
    hubGrad.addColorStop(0, '#e2e8f0');
    hubGrad.addColorStop(0.7, '#64748b');
    hubGrad.addColorStop(1, '#0f172a');

    ctx.beginPath();
    ctx.arc(centerX, centerY, hubRadius, 0, Math.PI * 2);
    ctx.fillStyle = hubGrad;
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#94a3b8';
    ctx.stroke();

    // Spindle screws
    for (let i = 0; i < 4; i++) {
      const angle = (Math.PI / 2) * i + this.rotationAngle;
      const sx = centerX + Math.cos(angle) * (hubRadius * 0.55);
      const sy = centerY + Math.sin(angle) * (hubRadius * 0.55);
      ctx.beginPath();
      ctx.arc(sx, sy, 2.5, 0, Math.PI * 2);
      ctx.fillStyle = '#334155';
      ctx.fill();
    }

    // Actuator Arm & Pivot Assembly
    const pivotX = w * 0.86;
    const pivotY = h * 0.22;
    const pivotRadius = 22;

    // Pivot Base
    ctx.beginPath();
    ctx.arc(pivotX, pivotY, pivotRadius, 0, Math.PI * 2);
    ctx.fillStyle = '#1e293b';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#38bdf8';
    ctx.stroke();

    // Calculate arm tip position on the active track ring
    // Pick an intersection point near the right side of the platter
    const armAngleOffset = 0.28; // radians
    const tipX = centerX + Math.cos(armAngleOffset) * activeRadius;
    const tipY = centerY - Math.sin(armAngleOffset) * activeRadius;

    // Arm line & metallic shape
    ctx.beginPath();
    ctx.moveTo(pivotX, pivotY);
    ctx.lineTo(tipX, tipY);
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.stroke();

    // Actuator Arm Head slider / read-write tip
    ctx.beginPath();
    ctx.arc(tipX, tipY, 6, 0, Math.PI * 2);
    ctx.fillStyle = '#00f2fe';
    ctx.shadowColor = '#00f2fe';
    ctx.shadowBlur = 12;
    ctx.fill();
    ctx.shadowBlur = 0;

    // Pivot center screw
    ctx.beginPath();
    ctx.arc(pivotX, pivotY, 6, 0, Math.PI * 2);
    ctx.fillStyle = '#e2e8f0';
    ctx.fill();

    // Status / Track text on canvas
    ctx.font = '600 13px "Outfit", sans-serif';
    ctx.fillStyle = '#94a3b8';
    ctx.fillText('ACTIVE HEAD CYLINDER', 16, 26);

    ctx.font = '700 24px "JetBrains Mono", monospace';
    ctx.fillStyle = '#00f2fe';
    ctx.fillText(`${Math.round(this.currentTrack)}`, 16, 56);

    ctx.font = '400 12px "Outfit", sans-serif';
    ctx.fillStyle = '#64748b';
    ctx.fillText(`Range: 0 – ${this.maxCylinder}`, 16, 76);

    ctx.restore();
  }

  renderRuler() {
    if (!this.rulerContainer) return;
    this.rulerContainer.innerHTML = '';

    const rulerTrack = document.createElement('div');
    rulerTrack.className = 'track-ruler-bar';

    // Min & Max label
    const minLabel = document.createElement('span');
    minLabel.className = 'ruler-label-min';
    minLabel.textContent = '0';
    this.rulerContainer.appendChild(minLabel);

    const maxLabel = document.createElement('span');
    maxLabel.className = 'ruler-label-max';
    maxLabel.textContent = `${this.maxCylinder}`;
    this.rulerContainer.appendChild(maxLabel);

    // Request pins
    this.requests.forEach((req, idx) => {
      const pct = (req / this.maxCylinder) * 100;
      const pin = document.createElement('div');
      pin.className = 'request-pin';
      pin.id = `req-pin-${req}`;
      pin.style.left = `${pct}%`;
      pin.title = `Request #${idx + 1}: Track ${req}`;
      pin.innerHTML = `<span>${req}</span>`;
      rulerTrack.appendChild(pin);
    });

    // Active Head Marker
    const headMarker = document.createElement('div');
    headMarker.className = 'ruler-head-marker';
    headMarker.id = 'rulerHeadMarker';
    const initPct = (this.currentTrack / this.maxCylinder) * 100;
    headMarker.style.left = `${initPct}%`;
    headMarker.innerHTML = `<div class="head-arrow"></div><div class="head-badge">${Math.round(this.currentTrack)}</div>`;
    rulerTrack.appendChild(headMarker);

    this.rulerContainer.appendChild(rulerTrack);
  }

  updateRulerHead(track) {
    const marker = document.getElementById('rulerHeadMarker');
    if (marker && this.maxCylinder > 0) {
      const pct = (track / this.maxCylinder) * 100;
      marker.style.left = `${pct}%`;
      const badge = marker.querySelector('.head-badge');
      if (badge) badge.textContent = `${track}`;
    }

    // Highlight serviced pins
    const pin = document.getElementById(`req-pin-${track}`);
    if (pin) {
      pin.classList.add('serviced');
    }
  }

  destroy() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
  }
}
