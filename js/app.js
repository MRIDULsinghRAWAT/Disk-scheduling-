import { runAllAlgorithms } from './algorithms.js';
import { DiskVisualizer } from './diskVisualizer.js';
import { ChartManager } from './chartManager.js';
import { SimulatorEngine } from './simulator.js';
import { ReportGenerator } from './reportGenerator.js';

// Application State
const state = {
  maxCylinder: 199,
  initialHead: 53,
  direction: 'right', // 'right' or 'left'
  seekTimeMs: 5, // ms per track seek
  requests: [98, 183, 37, 122, 14, 124, 65, 67],
  activeAlgorithmKey: 'FCFS', // 'FCFS', 'SSTF', 'SCAN', 'CSCAN', 'LOOK', 'CLOOK', or 'ALL'
  allResults: null,
  showExtended: true
};

// Preset sequences
const PRESETS = {
  textbook: {
    name: 'Silberschatz Textbook Benchmark',
    requests: [98, 183, 37, 122, 14, 124, 65, 67],
    initialHead: 53,
    maxCylinder: 199,
    direction: 'right'
  },
  clustering: {
    name: 'Localized Clustering',
    requests: [45, 52, 58, 48, 160, 165, 172, 168],
    initialHead: 50,
    maxCylinder: 199,
    direction: 'right'
  },
  pingpong: {
    name: 'Ping-Pong Alternating Extremes',
    requests: [12, 188, 18, 182, 25, 175, 30, 170],
    initialHead: 100,
    maxCylinder: 199,
    direction: 'right'
  },
  sequential: {
    name: 'Sequential Ascending Sweep',
    requests: [20, 45, 70, 95, 120, 145, 170, 190],
    initialHead: 10,
    maxCylinder: 199,
    direction: 'right'
  }
};

let diskVisualizer = null;
let chartManager = null;
let simulator = null;

document.addEventListener('DOMContentLoaded', () => {
  initVisualizers();
  initEventListeners();
  loadPreset('textbook');
});

function initVisualizers() {
  diskVisualizer = new DiskVisualizer('diskCanvas', 'trackRulerContainer');
  chartManager = new ChartManager('trajectoryChartCanvas', 'comparisonChartCanvas');

  simulator = new SimulatorEngine({
    onStepChange: handleStepChange,
    onFinish: () => {
      updatePlayButtonUI(false);
    }
  });
}

function initEventListeners() {
  // Config form inputs
  const requestsInput = document.getElementById('requestsInput');
  const initialHeadInput = document.getElementById('initialHeadInput');
  const maxCylinderInput = document.getElementById('maxCylinderInput');
  const directionSelect = document.getElementById('directionSelect');
  const seekTimeInput = document.getElementById('seekTimeInput');
  const runBtn = document.getElementById('runBtn');

  // Input change events
  runBtn.addEventListener('click', applyConfigAndRun);

  // Allow pressing Enter in requests input to trigger run
  requestsInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') applyConfigAndRun();
  });

  // Preset Buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const presetKey = btn.getAttribute('data-preset');
      if (PRESETS[presetKey]) {
        loadPreset(presetKey);
      }
    });
  });

  // Random Generator Button
  const randomBtn = document.getElementById('randomGenBtn');
  if (randomBtn) {
    randomBtn.addEventListener('click', generateRandomRequests);
  }

  // Algorithm Tab switching
  document.querySelectorAll('.alg-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const algKey = tab.getAttribute('data-alg');
      setActiveAlgorithm(algKey);
    });
  });

  // Extended Algorithms Toggle
  const toggleExtended = document.getElementById('toggleExtendedAlgorithms');
  if (toggleExtended) {
    toggleExtended.addEventListener('change', e => {
      state.showExtended = e.target.checked;
      document.querySelectorAll('.extended-alg').forEach(el => {
        el.style.display = state.showExtended ? '' : 'none';
      });
      // If active algorithm is an extended one and now hidden, revert to FCFS
      if (!state.showExtended && ['CSCAN', 'LOOK', 'CLOOK'].includes(state.activeAlgorithmKey)) {
        setActiveAlgorithm('FCFS');
      } else {
        recomputeAndRender();
      }
    });
  }

  // Simulator controls
  const playPauseBtn = document.getElementById('playPauseBtn');
  const prevStepBtn = document.getElementById('prevStepBtn');
  const nextStepBtn = document.getElementById('nextStepBtn');
  const resetStepBtn = document.getElementById('resetStepBtn');
  const speedSelect = document.getElementById('speedSelect');

  if (playPauseBtn) playPauseBtn.addEventListener('click', () => simulator.togglePlayPause());
  if (prevStepBtn) prevStepBtn.addEventListener('click', () => simulator.stepBackward());
  if (nextStepBtn) nextStepBtn.addEventListener('click', () => simulator.stepForward());
  if (resetStepBtn) resetStepBtn.addEventListener('click', () => simulator.reset());
  if (speedSelect) {
    speedSelect.addEventListener('change', e => {
      simulator.setSpeed(parseFloat(e.target.value));
    });
  }

  // Trajectory view mode toggle (Single vs Overlay All)
  const trajectoryOverlayToggle = document.getElementById('trajectoryOverlayToggle');
  if (trajectoryOverlayToggle) {
    trajectoryOverlayToggle.addEventListener('change', () => {
      renderCharts();
    });
  }

  // Export Report Button
  const exportBtn = document.getElementById('exportReportBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      ReportGenerator.generateReport({
        config: state,
        allResults: state.allResults,
        seekTimeMs: state.seekTimeMs
      });
    });
  }
}

function loadPreset(key) {
  const preset = PRESETS[key];
  if (!preset) return;

  document.getElementById('requestsInput').value = preset.requests.join(', ');
  document.getElementById('initialHeadInput').value = preset.initialHead;
  document.getElementById('maxCylinderInput').value = preset.maxCylinder;
  document.getElementById('directionSelect').value = preset.direction;

  // Visual active state on preset button
  document.querySelectorAll('.preset-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-preset') === key);
  });

  applyConfigAndRun();
}

function generateRandomRequests() {
  const count = 8;
  const maxCyl = parseInt(document.getElementById('maxCylinderInput').value) || 199;
  const reqs = [];
  while (reqs.length < count) {
    const r = Math.floor(Math.random() * (maxCyl + 1));
    if (!reqs.includes(r)) reqs.push(r);
  }
  document.getElementById('requestsInput').value = reqs.join(', ');
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
  applyConfigAndRun();
}

function applyConfigAndRun() {
  const reqStr = document.getElementById('requestsInput').value;
  const maxCyl = Math.max(10, parseInt(document.getElementById('maxCylinderInput').value) || 199);
  let initHead = parseInt(document.getElementById('initialHeadInput').value);
  if (isNaN(initHead) || initHead < 0) initHead = 0;
  if (initHead > maxCyl) initHead = maxCyl;

  const dir = document.getElementById('directionSelect').value || 'right';
  const seekTime = parseFloat(document.getElementById('seekTimeInput')?.value) || 5;

  // Parse comma or whitespace separated requests
  const parsedRequests = reqStr
    .split(/[\s,]+/)
    .map(s => parseInt(s.trim()))
    .filter(n => !isNaN(n) && n >= 0 && n <= maxCyl);

  if (parsedRequests.length === 0) {
    alert('Please enter at least one valid cylinder request within 0 to ' + maxCyl);
    return;
  }

  state.requests = parsedRequests;
  state.initialHead = initHead;
  state.maxCylinder = maxCyl;
  state.direction = dir;
  state.seekTimeMs = seekTime;

  // Update input displays if clamped
  document.getElementById('initialHeadInput').value = initHead;
  document.getElementById('maxCylinderInput').value = maxCyl;

  recomputeAndRender();
}

function recomputeAndRender() {
  // Execute all algorithms
  state.allResults = runAllAlgorithms(
    state.requests,
    state.initialHead,
    state.maxCylinder,
    state.direction
  );

  // Update visualizer parameters
  diskVisualizer.setParameters(state.maxCylinder, state.requests, state.initialHead);

  // Update active algorithm UI & load into simulator
  updateActiveAlgorithmView();

  // Render Charts
  renderCharts();

  // Render Comparative Table
  renderComparisonTable();
}

function setActiveAlgorithm(algKey) {
  state.activeAlgorithmKey = algKey;

  document.querySelectorAll('.alg-tab').forEach(tab => {
    tab.classList.toggle('active', tab.getAttribute('data-alg') === algKey);
  });

  updateActiveAlgorithmView();
  renderCharts();
}

function updateActiveAlgorithmView() {
  if (!state.allResults) return;

  const currentResult = state.allResults[state.activeAlgorithmKey] || state.allResults['FCFS'];

  // Load into simulator engine
  simulator.loadResult(currentResult);

  // Update Metrics Cards
  const thmElem = document.getElementById('metricTHM');
  const aslElem = document.getElementById('metricASL');
  const timeElem = document.getElementById('metricTime');
  const effElem = document.getElementById('metricEfficiency');
  const algTitleElem = document.getElementById('activeAlgTitle');
  const algDescElem = document.getElementById('activeAlgDesc');

  if (thmElem) thmElem.textContent = `${currentResult.totalHeadMovement} cylinders`;
  if (aslElem) aslElem.textContent = `${currentResult.averageSeekLength.toFixed(2)} tracks/req`;
  if (timeElem) timeElem.textContent = `${(currentResult.totalHeadMovement * state.seekTimeMs).toFixed(1)} ms`;

  // Compare efficiency against FCFS baseline
  const fcfsTHM = state.allResults.FCFS.totalHeadMovement;
  if (effElem) {
    if (currentResult.algorithm === 'FCFS') {
      effElem.textContent = 'Baseline (0%)';
      effElem.className = 'metric-value neutral';
    } else {
      const diff = fcfsTHM - currentResult.totalHeadMovement;
      const pct = ((diff / fcfsTHM) * 100).toFixed(1);
      if (diff > 0) {
        effElem.textContent = `+${pct}% Better than FCFS`;
        effElem.className = 'metric-value positive';
      } else if (diff === 0) {
        effElem.textContent = 'Identical to FCFS';
        effElem.className = 'metric-value neutral';
      } else {
        effElem.textContent = `${pct}% Slower than FCFS`;
        effElem.className = 'metric-value negative';
      }
    }
  }

  if (algTitleElem) algTitleElem.textContent = currentResult.name;
  if (algDescElem) {
    let desc = '';
    if (currentResult.algorithm === 'FCFS') {
      desc = 'Services I/O requests strictly in order of arrival. Simple and fair (FIFO), but high average seek time due to wild arm movements.';
    } else if (currentResult.algorithm === 'SSTF') {
      desc = 'Always chooses the pending request with the minimum seek distance from current head. Highly efficient, but risks starvation for distant tracks.';
    } else if (currentResult.algorithm === 'SCAN') {
      desc = `Elevator algorithm: Sweeps continuously ${state.direction === 'right' ? 'upwards to cylinder ' + state.maxCylinder : 'downwards to track 0'}, servicing requests along the way, then reverses. Prevents starvation while maintaining high throughput.`;
    } else if (currentResult.algorithm === 'CSCAN') {
      desc = `Circular SCAN: Sweeps in one direction, then immediately jumps back to the starting boundary without servicing requests on the return trip. Provides uniform waiting times.`;
    } else if (currentResult.algorithm === 'LOOK') {
      desc = 'Optimized SCAN: Only travels as far as the final request in each direction before reversing, avoiding unnecessary trips to the disk ends.';
    } else if (currentResult.algorithm === 'CLOOK') {
      desc = 'Optimized Circular SCAN: Only travels to the last request in current direction, then jumps directly to the lowest pending request.';
    }
    algDescElem.textContent = desc;
  }

  // Render Step Table
  renderCalculationTable(currentResult);
}

function renderCharts() {
  if (!state.allResults) return;

  const overlayToggle = document.getElementById('trajectoryOverlayToggle');
  const isOverlay = overlayToggle ? overlayToggle.checked : false;

  if (isOverlay) {
    // Show all 3 required or all available algorithms on trajectory
    const algs = state.showExtended
      ? Object.values(state.allResults)
      : [state.allResults.FCFS, state.allResults.SSTF, state.allResults.SCAN];
    chartManager.renderTrajectory(algs, state.maxCylinder);
  } else {
    // Single active algorithm
    const currentResult = state.allResults[state.activeAlgorithmKey] || state.allResults['FCFS'];
    chartManager.renderTrajectory(currentResult, state.maxCylinder, simulator.currentStepIndex);
  }

  // Comparative bar charts
  const comparativeSubset = {};
  const keys = state.showExtended
    ? ['FCFS', 'SSTF', 'SCAN', 'CSCAN', 'LOOK', 'CLOOK']
    : ['FCFS', 'SSTF', 'SCAN'];

  keys.forEach(k => {
    if (state.allResults[k]) comparativeSubset[k] = state.allResults[k];
  });
  chartManager.renderComparison(comparativeSubset);
}

function renderCalculationTable(result) {
  const tableBody = document.getElementById('calculationTableBody');
  if (!tableBody) return;

  tableBody.innerHTML = '';

  // Initial head row
  const initRow = document.createElement('tr');
  initRow.id = 'step-row-0';
  initRow.className = 'step-row active';
  initRow.innerHTML = `
    <td><strong>0 (Start)</strong></td>
    <td>—</td>
    <td><span class="track-badge">${result.initialHead}</span></td>
    <td>Initial head position</td>
    <td>0</td>
    <td><strong>0</strong></td>
    <td><span class="badge badge-info">Start Position</span></td>
  `;
  tableBody.appendChild(initRow);

  result.steps.forEach(step => {
    const row = document.createElement('tr');
    row.id = `step-row-${step.stepIndex}`;
    row.className = 'step-row';
    row.innerHTML = `
      <td><strong>${step.stepIndex}</strong></td>
      <td><span class="track-badge">${step.from}</span></td>
      <td><span class="track-badge target">${step.to}</span></td>
      <td><code>|${step.to} - ${step.from}|</code></td>
      <td class="seek-cell">${step.distance}</td>
      <td><strong>${step.cumulative}</strong></td>
      <td>
        <span class="badge ${step.isBoundary ? 'badge-warning' : 'badge-success'}">
          ${step.note}
        </span>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

function renderComparisonTable() {
  const tbody = document.getElementById('comparisonTableBody');
  if (!tbody || !state.allResults) return;

  tbody.innerHTML = '';

  const keys = state.showExtended
    ? ['FCFS', 'SSTF', 'SCAN', 'CSCAN', 'LOOK', 'CLOOK']
    : ['FCFS', 'SSTF', 'SCAN'];

  // Find lowest THM among evaluated
  let minTHM = Infinity;
  keys.forEach(k => {
    if (state.allResults[k] && state.allResults[k].totalHeadMovement < minTHM) {
      minTHM = state.allResults[k].totalHeadMovement;
    }
  });

  keys.forEach(k => {
    const r = state.allResults[k];
    if (!r) return;

    const isBest = r.totalHeadMovement === minTHM;
    const estTimeMs = (r.totalHeadMovement * state.seekTimeMs).toFixed(1);
    const fcfsDiff = state.allResults.FCFS.totalHeadMovement - r.totalHeadMovement;
    const diffPct = ((fcfsDiff / state.allResults.FCFS.totalHeadMovement) * 100).toFixed(1);

    let efficiencyBadge = '';
    if (k === 'FCFS') {
      efficiencyBadge = '<span class="badge badge-neutral">Baseline</span>';
    } else if (fcfsDiff > 0) {
      efficiencyBadge = `<span class="badge badge-success">+${diffPct}% Faster</span>`;
    } else {
      efficiencyBadge = `<span class="badge badge-danger">${diffPct}% Slower</span>`;
    }

    const row = document.createElement('tr');
    if (isBest) row.classList.add('best-row');
    row.innerHTML = `
      <td>
        <strong>${r.name}</strong>
        ${isBest ? ' <span class="badge badge-gold">★ Most Efficient</span>' : ''}
      </td>
      <td class="thm-value">${r.totalHeadMovement}</td>
      <td>${r.averageSeekLength.toFixed(2)}</td>
      <td>${estTimeMs} ms</td>
      <td>${efficiencyBadge}</td>
      <td><span class="service-seq">${r.seekSequence.join(' → ')}</span></td>
      <td><span class="badge ${r.starvationRisk.includes('High') ? 'badge-danger' : r.starvationRisk.includes('None') ? 'badge-success' : 'badge-warning'}">${r.starvationRisk}</span></td>
      <td><code>${r.timeComplexity}</code></td>
    `;
    tbody.appendChild(row);
  });
}

function handleStepChange({ stepIndex, totalSteps, currentTrack, stepData, cumulativeTHM, isPlaying }) {
  // Move visualizer head
  if (diskVisualizer) {
    diskVisualizer.seekTo(currentTrack, true);
  }

  // Update step status text
  const stepTracker = document.getElementById('stepProgressText');
  if (stepTracker) {
    stepTracker.textContent = `Step ${stepIndex} of ${totalSteps}`;
  }

  // Highlight active table row
  document.querySelectorAll('.step-row').forEach(r => r.classList.remove('active'));
  const activeRow = document.getElementById(`step-row-${stepIndex}`);
  if (activeRow) {
    activeRow.classList.add('active');
    activeRow.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // Update play button icon/text
  updatePlayButtonUI(isPlaying);

  // Update trajectory chart highlight
  const overlayToggle = document.getElementById('trajectoryOverlayToggle');
  const isOverlay = overlayToggle ? overlayToggle.checked : false;
  if (!isOverlay && state.allResults) {
    const currentResult = state.allResults[state.activeAlgorithmKey] || state.allResults['FCFS'];
    chartManager.highlightStep(currentResult, state.maxCylinder, stepIndex);
  }
}

function updatePlayButtonUI(isPlaying) {
  const btn = document.getElementById('playPauseBtn');
  if (!btn) return;
  if (isPlaying) {
    btn.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
        <rect x="6" y="4" width="4" height="16"/>
        <rect x="14" y="4" width="4" height="16"/>
      </svg>
      <span>Pause</span>
    `;
    btn.classList.add('playing');
  } else {
    btn.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
        <polygon points="5 3 19 12 5 21 5 3"/>
      </svg>
      <span>Play Simulation</span>
    `;
    btn.classList.remove('playing');
  }
}
