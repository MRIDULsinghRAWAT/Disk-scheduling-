import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';

const SCREENSHOT_DIR = path.resolve('./screenshots');
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

// Locate Chrome or Edge
const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const executablePath = fs.existsSync(chromePath) ? chromePath : edgePath;

console.log(`Using browser executable: ${executablePath}`);

async function run() {
  const browser = await puppeteer.launch({
    executablePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    defaultViewport: {
      width: 1440,
      height: 900,
      deviceScaleFactor: 2 // High DPI for crystal clear screenshots
    }
  });

  const page = await browser.newPage();
  await page.goto('http://localhost:8000', { waitUntil: 'networkidle0' });

  // Wait 1.5s for fonts, animations and Chart.js to fully render
  await new Promise(r => setTimeout(r, 1500));

  console.log('1. Capturing Full Dashboard...');
  await page.screenshot({
    path: path.join(SCREENSHOT_DIR, '01_full_dashboard.png'),
    fullPage: true
  });

  console.log('2. Capturing Configuration & Parameters Panel...');
  const configSection = await page.$('section[aria-label="Disk Configuration"]');
  if (configSection) {
    await configSection.screenshot({
      path: path.join(SCREENSHOT_DIR, '02_configuration_panel.png')
    });
  }

  console.log('3. Capturing Live Disk Platter & Seek Simulator...');
  const platterSection = await page.$('section[aria-label="Physical Hard Disk Simulation"]');
  if (platterSection) {
    await platterSection.screenshot({
      path: path.join(SCREENSHOT_DIR, '03_hardware_visualizer.png')
    });
  }

  console.log('4. Stepping through simulation to show active seek state...');
  // Click Next Step button 4 times to show active seek
  for (let i = 0; i < 4; i++) {
    await page.click('#nextStepBtn');
    await new Promise(r => setTimeout(r, 400));
  }
  if (platterSection) {
    await platterSection.screenshot({
      path: path.join(SCREENSHOT_DIR, '04_active_seeking_state.png')
    });
  }

  // Reset simulation for clean graph screenshots
  await page.click('#resetStepBtn');
  await new Promise(r => setTimeout(r, 300));

  console.log('5. Capturing FCFS Trajectory Graph...');
  const chartsSection = await page.$('section[aria-label="Visual Graphs"]');
  const trajectoryCard = await page.$('.charts-grid .chart-card:first-child');
  if (trajectoryCard) {
    await trajectoryCard.screenshot({
      path: path.join(SCREENSHOT_DIR, '05_trajectory_fcfs.png')
    });
  }

  console.log('6. Switching to SSTF and capturing Trajectory...');
  await page.click('button.alg-tab[data-alg="SSTF"]');
  await new Promise(r => setTimeout(r, 600));
  if (trajectoryCard) {
    await trajectoryCard.screenshot({
      path: path.join(SCREENSHOT_DIR, '06_trajectory_sstf.png')
    });
  }

  console.log('7. Switching to SCAN and capturing Trajectory...');
  await page.click('button.alg-tab[data-alg="SCAN"]');
  await new Promise(r => setTimeout(r, 600));
  if (trajectoryCard) {
    await trajectoryCard.screenshot({
      path: path.join(SCREENSHOT_DIR, '07_trajectory_scan.png')
    });
  }

  console.log('8. Enabling Trajectory Overlay (All Algorithms)...');
  await page.click('#trajectoryOverlayToggle');
  await new Promise(r => setTimeout(r, 800));
  if (trajectoryCard) {
    await trajectoryCard.screenshot({
      path: path.join(SCREENSHOT_DIR, '08_trajectory_overlay_all.png')
    });
  }

  console.log('9. Capturing Comparative Metrics Bar Charts...');
  const barCard = await page.$('.charts-grid .chart-card:last-child');
  if (barCard) {
    await barCard.screenshot({
      path: path.join(SCREENSHOT_DIR, '09_comparison_barcharts.png')
    });
  }

  console.log('10. Capturing Mathematical Step Calculation Table...');
  const calcSection = await page.$('section[aria-label="Step-by-Step Calculations"]');
  if (calcSection) {
    await calcSection.screenshot({
      path: path.join(SCREENSHOT_DIR, '10_step_calculation_table.png')
    });
  }

  console.log('11. Capturing Comparative Results Matrix...');
  const matrixSection = await page.$('section[aria-label="Comparative Matrix"]');
  if (matrixSection) {
    await matrixSection.screenshot({
      path: path.join(SCREENSHOT_DIR, '11_comparative_matrix.png')
    });
  }

  console.log('All screenshots captured successfully!');
  await browser.close();
}

run().catch(err => {
  console.error('Error capturing screenshots:', err);
  process.exit(1);
});
