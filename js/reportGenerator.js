/**
 * Academic Report Generator
 * Formats and exports a comprehensive OS project report for student Akshat Joshi.
 */

export class ReportGenerator {
  static generateReport({ config, allResults, seekTimeMs = 5 }) {
    const dateStr = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    const algorithmsToInclude = ['FCFS', 'SSTF', 'SCAN', 'CSCAN', 'LOOK', 'CLOOK'];
    const results = algorithmsToInclude.map(k => allResults[k]).filter(Boolean);

    // Find best performer
    let bestAlg = results[0];
    results.forEach(r => {
      if (r.totalHeadMovement < bestAlg.totalHeadMovement) {
        bestAlg = r;
      }
    });

    // Generate comparison rows
    const comparisonRows = results.map(r => {
      const isBest = r.algorithm === bestAlg.algorithm;
      const totalTimeMs = (r.totalHeadMovement * seekTimeMs).toFixed(1);
      return `
        <tr class="${isBest ? 'best-row' : ''}">
          <td><strong>${r.name} (${r.algorithm})</strong> ${isBest ? '★ (Best)' : ''}</td>
          <td style="font-weight: 700; color: #0284c7;">${r.totalHeadMovement}</td>
          <td>${r.averageSeekLength.toFixed(2)}</td>
          <td>${totalTimeMs} ms</td>
          <td><small style="word-break: break-all;">${r.seekSequence.join(' → ')}</small></td>
          <td>${r.starvationRisk}</td>
          <td><code>${r.timeComplexity}</code></td>
        </tr>
      `;
    }).join('');

    // Detailed calculation tables for FCFS, SSTF, SCAN
    const primaryAlgs = ['FCFS', 'SSTF', 'SCAN'];
    const detailedTables = primaryAlgs.map(algKey => {
      const r = allResults[algKey];
      if (!r) return '';

      const stepRows = r.steps.map(s => `
        <tr>
          <td>${s.stepIndex}</td>
          <td>${s.from}</td>
          <td>${s.to}</td>
          <td>|${s.to} - ${s.from}|</td>
          <td>${s.distance}</td>
          <td><strong>${s.cumulative}</strong></td>
          <td><small>${s.note}</small></td>
        </tr>
      `).join('');

      return `
        <div class="algorithm-breakdown">
          <h3>${r.name} (${r.algorithm}) - Mathematical Step Breakdown</h3>
          <p>Initial Head: <strong>${r.initialHead}</strong> | Total Head Movement (THM): <strong>${r.totalHeadMovement}</strong> cylinders | Avg Seek: <strong>${r.averageSeekLength.toFixed(2)}</strong> tracks/req</p>
          <table class="report-table">
            <thead>
              <tr>
                <th>Step #</th>
                <th>From Track</th>
                <th>To Track</th>
                <th>Formula</th>
                <th>Seek Distance (|Δ|)</th>
                <th>Cumulative Movement</th>
                <th>Operational Note</th>
              </tr>
            </thead>
            <tbody>
              ${stepRows}
            </tbody>
          </table>
        </div>
      `;
    }).join('');

    // HTML Template for Print
    const reportHtml = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>Academic Project Report - Disk Scheduling Performance Analysis</title>
        <style>
          @page {
            size: A4;
            margin: 18mm;
          }
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #1e293b;
            line-height: 1.5;
            background: #ffffff;
            margin: 0;
            padding: 20px;
          }
          .header-box {
            border-bottom: 2px solid #0284c7;
            padding-bottom: 12px;
            margin-bottom: 20px;
          }
          .header-box h1 {
            margin: 0 0 6px 0;
            font-size: 22px;
            color: #0f172a;
          }
          .header-box h2 {
            margin: 0 0 10px 0;
            font-size: 15px;
            color: #475569;
            font-weight: 500;
          }
          .meta-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px;
            font-size: 13px;
          }
          .meta-item strong {
            color: #0f172a;
          }
          h3 {
            color: #0284c7;
            border-left: 4px solid #0284c7;
            padding-left: 8px;
            margin-top: 24px;
            margin-bottom: 10px;
            font-size: 16px;
          }
          p {
            font-size: 13px;
            margin-bottom: 10px;
          }
          .report-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-bottom: 20px;
          }
          .report-table th, .report-table td {
            border: 1px solid #cbd5e1;
            padding: 7px 10px;
            text-align: left;
          }
          .report-table th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 600;
          }
          .report-table tr:nth-child(even) {
            background-color: #f8fafc;
          }
          .best-row {
            background-color: #e0f2fe !important;
            font-weight: 600;
          }
          .analysis-section {
            background: #f8fafc;
            border-left: 4px solid #10b981;
            padding: 12px 16px;
            border-radius: 0 6px 6px 0;
            margin-top: 15px;
            font-size: 13px;
          }
          .references {
            margin-top: 30px;
            border-top: 1px solid #cbd5e1;
            padding-top: 12px;
            font-size: 12px;
            color: #475569;
          }
          @media print {
            body { padding: 0; }
            .no-print { display: none; }
            .algorithm-breakdown { page-break-inside: avoid; }
          }
        </style>
      </head>
      <body>
        <div class="no-print" style="margin-bottom: 16px; display: flex; gap: 10px;">
          <button onclick="window.print()" style="background: #0284c7; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer;">
            Print / Save as PDF
          </button>
          <button onclick="window.close()" style="background: #64748b; color: white; border: none; padding: 10px 16px; border-radius: 6px; cursor: pointer;">
            Close Window
          </button>
        </div>

        <div class="header-box">
          <h1>Disk Scheduling Algorithms: FCFS, SSTF and SCAN Performance Analysis</h1>
          <h2>Operating Systems Lab Project Report • Unit VI: Storage Management</h2>
          <div class="meta-grid">
            <div class="meta-item"><strong>Student Name:</strong> Akshat Joshi</div>
            <div class="meta-item"><strong>Date:</strong> ${dateStr}</div>
            <div class="meta-item"><strong>Total Cylinders:</strong> 0 to ${config.maxCylinder} (${config.maxCylinder + 1} tracks)</div>
            <div class="meta-item"><strong>Initial Head Position:</strong> Track ${config.initialHead}</div>
            <div class="meta-item"><strong>Arm Seek Direction:</strong> ${config.direction.toUpperCase()} (towards ${config.direction === 'right' ? config.maxCylinder : 0})</div>
            <div class="meta-item"><strong>Request Queue (${config.requests.length} requests):</strong> [${config.requests.join(', ')}]</div>
          </div>
        </div>

        <h3>1. Executive Performance Comparison</h3>
        <p>Comparative summary of head movement efficiency, fairness, and execution performance across evaluated disk scheduling algorithms:</p>
        <table class="report-table">
          <thead>
            <tr>
              <th>Algorithm</th>
              <th>Total Head Movement (THM)</th>
              <th>Avg Seek (Tracks/Req)</th>
              <th>Est. Seek Time (@${seekTimeMs}ms)</th>
              <th>Service Sequence</th>
              <th>Starvation Risk</th>
              <th>Time Complexity</th>
            </tr>
          </thead>
          <tbody>
            ${comparisonRows}
          </tbody>
        </table>

        <div class="analysis-section">
          <strong>Key Findings & Performance Analysis:</strong>
          <ul>
            <li><strong>FCFS</strong> resulted in a total head movement of <strong>${allResults.FCFS.totalHeadMovement}</strong> tracks. Because it blindly processes requests in order of arrival, it suffers from wild arm swings across the platter (arm oscillation). However, it is completely free from starvation and provides strict FIFO fairness.</li>
            <li><strong>SSTF</strong> achieved a total head movement of <strong>${allResults.SSTF.totalHeadMovement}</strong> tracks (a <strong>${(((allResults.FCFS.totalHeadMovement - allResults.SSTF.totalHeadMovement) / allResults.FCFS.totalHeadMovement) * 100).toFixed(1)}%</strong> reduction compared to FCFS). SSTF greedily picks the nearest request, drastically minimizing seek times. However, requests at distant disk boundaries risk perpetual starvation under heavy workload.</li>
            <li><strong>SCAN</strong> (Elevator Algorithm) achieved a total head movement of <strong>${allResults.SCAN.totalHeadMovement}</strong> tracks. By sweeping continuously in one direction until reaching boundary ${config.direction === 'right' ? config.maxCylinder : 0} before reversing, it balances high throughput with starvation prevention.</li>
            <li><strong>Most Optimal Algorithm:</strong> In this test sequence, <strong>${bestAlg.name}</strong> delivered the lowest total head movement (<strong>${bestAlg.totalHeadMovement}</strong> tracks).</li>
          </ul>
        </div>

        <h3>2. Detailed Mathematical Calculation Logs</h3>
        ${detailedTables}

        <h3>3. Theoretical Framework & Formulas</h3>
        <p><strong>Disk Access Time Equation:</strong></p>
        <p style="background: #f1f5f9; padding: 8px 12px; border-radius: 4px; font-family: monospace;">
          T<sub>access</sub> = T<sub>seek</sub> + T<sub>rotational</sub> + T<sub>transfer</sub>
        </p>
        <ul>
          <li><strong>Seek Distance Formula:</strong> &Delta;C<sub>i</sub> = |C<sub>i</sub> - C<sub>i-1</sub>| where C<sub>i</sub> is the target cylinder and C<sub>i-1</sub> is the prior head position.</li>
          <li><strong>Total Head Movement (THM):</strong> THM = &sum;<sub>i=1</sub><sup>N</sup> |C<sub>i</sub> - C<sub>i-1</sub>|</li>
          <li><strong>Average Seek Length (ASL):</strong> ASL = THM / N, where N is the total number of I/O requests.</li>
        </ul>

        <div class="references">
          <strong>Authentic Academic References:</strong>
          <ol>
            <li>Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). <em>Operating System Concepts</em> (10th Edition). Chapter 11: Mass-Storage Structure. John Wiley & Sons.</li>
            <li>Tanenbaum, A. S., & Bos, H. (2015). <em>Modern Operating Systems</em> (4th Edition). Chapter 5: Input/Output and Disk Arm Scheduling Algorithms. Pearson.</li>
            <li>Stallings, W. (2018). <em>Operating Systems: Internals and Design Principles</em> (9th Edition). Chapter 11: I/O Management and Disk Scheduling. Pearson.</li>
          </ol>
        </div>
      </body>
      </html>
    `;

    const printWin = window.open('', '_blank');
    if (printWin) {
      printWin.document.write(reportHtml);
      printWin.document.close();
    } else {
      alert('Please allow popups to open the academic report window.');
    }
  }
}
