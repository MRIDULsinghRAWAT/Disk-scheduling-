/**
 * Disk Scheduling Playback Simulator Engine
 * Manages step-by-step playback, pause, rewind, forward, and speed controls.
 */

export class SimulatorEngine {
  constructor({ onStepChange, onFinish }) {
    this.onStepChange = onStepChange || (() => {});
    this.onFinish = onFinish || (() => {});

    this.activeResult = null;
    this.currentStepIndex = 0; // 0 represents initial head state before any steps executed
    this.isPlaying = false;
    this.speed = 1.0;
    this.timer = null;
  }

  loadResult(result) {
    this.pause();
    this.activeResult = result;
    this.currentStepIndex = 0;
    this.notify();
  }

  play() {
    if (!this.activeResult || this.isPlaying) return;
    if (this.currentStepIndex >= this.activeResult.steps.length) {
      this.currentStepIndex = 0; // loop back to start if finished
    }
    this.isPlaying = true;
    this.scheduleNextTick();
    this.notify();
  }

  pause() {
    this.isPlaying = false;
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    this.notify();
  }

  togglePlayPause() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  stepForward() {
    this.pause();
    if (!this.activeResult) return;
    if (this.currentStepIndex < this.activeResult.steps.length) {
      this.currentStepIndex++;
      this.notify();
    }
  }

  stepBackward() {
    this.pause();
    if (!this.activeResult) return;
    if (this.currentStepIndex > 0) {
      this.currentStepIndex--;
      this.notify();
    }
  }

  jumpToStep(stepIdx) {
    this.pause();
    if (!this.activeResult) return;
    this.currentStepIndex = Math.max(0, Math.min(stepIdx, this.activeResult.steps.length));
    this.notify();
  }

  reset() {
    this.pause();
    this.currentStepIndex = 0;
    this.notify();
  }

  setSpeed(speedMultiplier) {
    this.speed = Math.max(0.2, Number(speedMultiplier));
  }

  scheduleNextTick() {
    if (!this.isPlaying) return;

    const baseDelay = 1000; // 1 second at 1x
    const delay = Math.max(150, baseDelay / this.speed);

    this.timer = setTimeout(() => {
      if (!this.isPlaying || !this.activeResult) return;

      if (this.currentStepIndex < this.activeResult.steps.length) {
        this.currentStepIndex++;
        this.notify();

        if (this.currentStepIndex >= this.activeResult.steps.length) {
          this.pause();
          this.onFinish();
        } else {
          this.scheduleNextTick();
        }
      } else {
        this.pause();
        this.onFinish();
      }
    }, delay);
  }

  notify() {
    if (!this.activeResult) return;

    let stepData = null;
    let track = this.activeResult.initialHead;

    if (this.currentStepIndex > 0) {
      stepData = this.activeResult.steps[this.currentStepIndex - 1];
      track = stepData.to;
    }

    this.onStepChange({
      stepIndex: this.currentStepIndex,
      totalSteps: this.activeResult.steps.length,
      currentTrack: track,
      stepData: stepData,
      cumulativeTHM: stepData ? stepData.cumulative : 0,
      isPlaying: this.isPlaying,
      isInitial: this.currentStepIndex === 0,
      isFinished: this.currentStepIndex === this.activeResult.steps.length
    });
  }
}
