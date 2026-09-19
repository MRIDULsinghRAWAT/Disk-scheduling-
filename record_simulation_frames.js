import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';

const FRAMES_DIR = path.resolve('./video_frames');
if (!fs.existsSync(FRAMES_DIR)) {
  fs.mkdirSync(FRAMES_DIR, { recursive: true });
} else {
  // Clean old frames
  fs.readdirSync(FRAMES_DIR).forEach(f => fs.unlinkSync(path.join(FRAMES_DIR, f)));
}

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const executablePath = fs.existsSync(chromePath) ? chromePath : edgePath;

let frameIndex = 0;

async function recordFrames(page, durationMs, intervalMs = 60) {
  const endTime = Date.now() + durationMs;
  while (Date.now() < endTime) {
    const frameName = `frame_${String(frameIndex).padStart(5, '0')}.jpg`;
    await page.screenshot({
      path: path.join(FRAMES_DIR, frameName),
      type: 'jpeg',
      quality: 85
    });
    frameIndex++;
    await new Promise(r => setTimeout(r, intervalMs));
  }
}

async function run() {
  console.log('Launching browser for simulation video capture...');
  const browser = await puppeteer.launch({
    executablePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    defaultViewport: {
      width: 1280,
      height: 720,
      deviceScaleFactor: 1
    }
  });

  const page = await browser.newPage();
  await page.goto('http://localhost:8000', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 1200));

  console.log('Scene 1: Showing Initial Dashboard & Configuration...');
  await recordFrames(page, 1500, 60);

  // Set speed to 2.0x for crisp, smooth demo
  await page.select('#speedSelect', '2.0');
  await new Promise(r => setTimeout(r, 200));

  console.log('Scene 2: Playing FCFS Simulation (Head traversing 53 -> 98 -> ... -> 67)...');
  await page.click('#playPauseBtn');
  // At 2x speed, 8 steps take ~3.5 seconds
  await recordFrames(page, 4500, 60);

  console.log('Scene 3: Switching to SSTF Algorithm and Playing...');
  await page.click('button.alg-tab[data-alg="SSTF"]');
  await new Promise(r => setTimeout(r, 400));
  await page.click('#playPauseBtn');
  await recordFrames(page, 4500, 60);

  console.log('Scene 4: Switching to SCAN (Elevator) Algorithm and Playing...');
  await page.click('button.alg-tab[data-alg="SCAN"]');
  await new Promise(r => setTimeout(r, 400));
  await page.click('#playPauseBtn');
  await recordFrames(page, 4500, 60);

  console.log('Scene 5: Scrolling to Trajectory Graphs & Comparison Charts...');
  await page.evaluate(() => {
    window.scrollTo({ top: 750, behavior: 'smooth' });
  });
  await recordFrames(page, 2500, 60);

  console.log('Scene 6: Toggling Trajectory Overlay on Trajectory Chart...');
  await page.click('#trajectoryOverlayToggle');
  await recordFrames(page, 2000, 60);

  console.log('Scene 7: Scrolling to Step-by-Step Calculation Table & Comparative Matrix...');
  await page.evaluate(() => {
    window.scrollTo({ top: 1400, behavior: 'smooth' });
  });
  await recordFrames(page, 3000, 60);

  console.log('Scene 8: Scrolling back to top overview...');
  await page.evaluate(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  await recordFrames(page, 2000, 60);

  console.log(`Total frames captured: ${frameIndex}`);
  await browser.close();
}

run().catch(err => {
  console.error('Error during recording:', err);
  process.exit(1);
});
