/**
 * Chart Manager
 * Manages the OS Textbook Trajectory Chart (Cylinder vs Step Order)
 * and Comparative Performance Bar Charts using Chart.js.
 */

export class ChartManager {
  constructor(trajectoryCanvasId, comparisonCanvasId) {
    this.trajectoryCanvas = document.getElementById(trajectoryCanvasId);
    this.comparisonCanvas = document.getElementById(comparisonCanvasId);
    this.trajectoryChart = null;
    this.comparisonChart = null;

    this.algorithmColors = {
      FCFS: { border: '#38bdf8', bg: 'rgba(56, 189, 248, 0.2)' },
      SSTF: { border: '#10b981', bg: 'rgba(16, 185, 129, 0.2)' },
      SCAN: { border: '#f59e0b', bg: 'rgba(245, 158, 11, 0.2)' },
      CSCAN: { border: '#a855f7', bg: 'rgba(168, 85, 247, 0.2)' },
      LOOK: { border: '#ec4899', bg: 'rgba(236, 72, 153, 0.2)' },
      CLOOK: { border: '#06b6d4', bg: 'rgba(6, 182, 212, 0.2)' }
    };
  }

  /**
   * Render or update the classic OS Textbook Trajectory Graph
   * @param {Object} result - Algorithm result or array of results if overlaying
   * @param {number} maxCylinder - Maximum track number
   * @param {number} currentActiveStep - (optional) index of step to highlight during playback
   */
  renderTrajectory(results, maxCylinder, currentActiveStep = null) {
    if (!this.trajectoryCanvas || typeof Chart === 'undefined') return;

    const isArray = Array.isArray(results);
    const resultList = isArray ? results : [results];

    // Build datasets
    const datasets = resultList.map(res => {
      const color = this.algorithmColors[res.algorithm] || { border: '#38bdf8', bg: 'rgba(56, 189, 248, 0.2)' };
      const dataPoints = res.seekSequence.map((track, stepIdx) => ({
        x: track,
        y: stepIdx
      }));

      // Point styling: make the current step larger / pulsating if provided
      const pointRadius = dataPoints.map((_, idx) => {
        if (!isArray && currentActiveStep !== null && idx === currentActiveStep) return 9;
        return idx === 0 ? 6 : 5;
      });

      const pointBackgroundColor = dataPoints.map((_, idx) => {
        if (!isArray && currentActiveStep !== null && idx === currentActiveStep) return '#ffffff';
        if (idx === 0) return '#fbbf24'; // Initial head is gold/amber
        return color.border;
      });

      return {
        label: `${res.name} (THM: ${res.totalHeadMovement})`,
        data: dataPoints,
        borderColor: color.border,
        backgroundColor: color.bg,
        borderWidth: 2.5,
        tension: 0, // Straight lines between cylinders as in Silberschatz textbook
        fill: false,
        pointRadius: pointRadius,
        pointHoverRadius: 8,
        pointBackgroundColor: pointBackgroundColor,
        pointBorderColor: '#0f172a',
        pointBorderWidth: 1.5
      };
    });

    // Find max step count for Y axis
    const maxSteps = Math.max(...resultList.map(r => r.seekSequence.length));

    if (this.trajectoryChart) {
      this.trajectoryChart.data.datasets = datasets;
      this.trajectoryChart.options.scales.x.max = maxCylinder;
      this.trajectoryChart.options.scales.y.max = maxSteps + 1;
      this.trajectoryChart.update();
      return;
    }

    const ctx = this.trajectoryCanvas.getContext('2d');
    this.trajectoryChart = new Chart(ctx, {
      type: 'line',
      data: { datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 400
        },
        interaction: {
          mode: 'nearest',
          intersect: false
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              color: '#e2e8f0',
              font: { family: "'Outfit', sans-serif", size: 13, weight: '500' },
              boxWidth: 14,
              padding: 14
            }
          },
          tooltip: {
            backgroundColor: '#1e293b',
            titleColor: '#00f2fe',
            bodyColor: '#e2e8f0',
            borderColor: '#334155',
            borderWidth: 1,
            padding: 10,
            callbacks: {
              title: items => `Step ${items[0].raw.y}: Cylinder ${items[0].raw.x}`,
              label: item => `${item.dataset.label.split('(')[0].trim()}: Track ${item.raw.x}`
            }
          }
        },
        scales: {
          x: {
            type: 'linear',
            position: 'top', // Place cylinder axis at top like textbook
            min: 0,
            max: maxCylinder,
            title: {
              display: true,
              text: 'Cylinder Number (Track)',
              color: '#94a3b8',
              font: { family: "'Outfit', sans-serif", size: 13, weight: '600' }
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.06)'
            },
            ticks: {
              color: '#cbd5e1',
              stepSize: Math.ceil(maxCylinder / 10),
              font: { family: "'JetBrains Mono', monospace", size: 11 }
            }
          },
          y: {
            type: 'linear',
            reverse: false, // Step 0 at top, increasing downwards
            min: 0,
            max: maxSteps + 1,
            title: {
              display: true,
              text: 'Service Order / Step Index',
              color: '#94a3b8',
              font: { family: "'Outfit', sans-serif", size: 13, weight: '600' }
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.06)'
            },
            ticks: {
              color: '#cbd5e1',
              stepSize: 1,
              font: { family: "'JetBrains Mono', monospace", size: 11 }
            }
          }
        }
      }
    });
  }

  /**
   * Render Comparative Bar Charts (Total Head Movement & Average Seek Length)
   * @param {Object} allResults - Dictionary of algorithm results: { FCFS, SSTF, SCAN, ... }
   */
  renderComparison(allResults) {
    if (!this.comparisonCanvas || typeof Chart === 'undefined') return;

    const labels = Object.keys(allResults).map(k => allResults[k].algorithm);
    const thmData = Object.keys(allResults).map(k => allResults[k].totalHeadMovement);
    const aslData = Object.keys(allResults).map(k => Number(allResults[k].averageSeekLength.toFixed(2)));

    const bgColors = labels.map(alg => (this.algorithmColors[alg]?.bg || 'rgba(56, 189, 248, 0.3)'));
    const borderColors = labels.map(alg => (this.algorithmColors[alg]?.border || '#38bdf8'));

    // Highlight minimum THM (Best Efficiency)
    const minTHM = Math.min(...thmData);

    const datasets = [
      {
        label: 'Total Head Movement (Cylinders)',
        data: thmData,
        backgroundColor: bgColors,
        borderColor: borderColors,
        borderWidth: 2,
        borderRadius: 6,
        yAxisID: 'y'
      },
      {
        label: 'Average Seek Length (Tracks/Req)',
        data: aslData,
        backgroundColor: 'rgba(244, 63, 94, 0.25)',
        borderColor: '#f43f5e',
        borderWidth: 2,
        borderRadius: 6,
        type: 'bar',
        yAxisID: 'y1'
      }
    ];

    if (this.comparisonChart) {
      this.comparisonChart.data.labels = labels;
      this.comparisonChart.data.datasets = datasets;
      this.comparisonChart.update();
      return;
    }

    const ctx = this.comparisonCanvas.getContext('2d');
    this.comparisonChart = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 600 },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              color: '#e2e8f0',
              font: { family: "'Outfit', sans-serif", size: 12 }
            }
          },
          tooltip: {
            backgroundColor: '#1e293b',
            titleColor: '#00f2fe',
            bodyColor: '#e2e8f0',
            borderColor: '#334155',
            borderWidth: 1,
            padding: 10,
            callbacks: {
              afterBody: items => {
                const alg = items[0].label;
                const res = allResults[alg];
                if (res && res.totalHeadMovement === minTHM) {
                  return `★ Best Performer in this run!`;
                }
                return '';
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: '#cbd5e1',
              font: { family: "'Outfit', sans-serif", size: 12, weight: '600' }
            }
          },
          y: {
            type: 'linear',
            position: 'left',
            title: {
              display: true,
              text: 'Total Head Movement (Cylinders)',
              color: '#94a3b8',
              font: { family: "'Outfit', sans-serif", size: 12 }
            },
            grid: { color: 'rgba(255, 255, 255, 0.06)' },
            ticks: { color: '#94a3b8' }
          },
          y1: {
            type: 'linear',
            position: 'right',
            title: {
              display: true,
              text: 'Avg Seek Length',
              color: '#f43f5e',
              font: { family: "'Outfit', sans-serif", size: 12 }
            },
            grid: { drawOnChartArea: false },
            ticks: { color: '#f43f5e' }
          }
        }
      }
    });
  }

  highlightStep(result, maxCylinder, stepIdx) {
    this.renderTrajectory(result, maxCylinder, stepIdx);
  }

  destroy() {
    if (this.trajectoryChart) this.trajectoryChart.destroy();
    if (this.comparisonChart) this.comparisonChart.destroy();
  }
}
