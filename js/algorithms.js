/**
 * Disk Scheduling Algorithms Engine
 * Supports: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK
 *
 * Each algorithm returns an object:
 * {
 *   algorithm: string,
 *   initialHead: number,
 *   totalHeadMovement: number,
 *   averageSeekLength: number,
 *   seekSequence: number[],        // Array of tracks visited in order, starting with initialHead
 *   steps: Array<{
 *     stepIndex: number,
 *     from: number,
 *     to: number,
 *     distance: number,
 *     cumulative: number,
 *     isBoundary?: boolean,
 *     note: string
 *   }>,
 *   starvationRisk: 'None' | 'Low' | 'High',
 *   timeComplexity: string
 * }
 */

// Utility: sanitize requests array
function sanitizeRequests(requests, maxCylinder) {
  return requests
    .map(Number)
    .filter(n => !isNaN(n) && n >= 0 && n <= maxCylinder);
}

/**
 * First-Come, First-Served (FCFS)
 * Services requests in the exact order they arrive.
 */
export function runFCFS(requests, initialHead, maxCylinder) {
  const reqs = sanitizeRequests(requests, maxCylinder);
  const seekSequence = [initialHead];
  const steps = [];
  let currentHead = initialHead;
  let totalMovement = 0;

  reqs.forEach((track, idx) => {
    const distance = Math.abs(track - currentHead);
    totalMovement += distance;
    steps.push({
      stepIndex: idx + 1,
      from: currentHead,
      to: track,
      distance: distance,
      cumulative: totalMovement,
      isBoundary: false,
      note: `Service request in arrival order (#${idx + 1}): track ${track}`
    });
    seekSequence.push(track);
    currentHead = track;
  });

  return {
    algorithm: 'FCFS',
    name: 'First-Come, First-Served',
    initialHead,
    maxCylinder,
    totalHeadMovement: totalMovement,
    averageSeekLength: reqs.length ? (totalMovement / reqs.length) : 0,
    seekSequence,
    steps,
    starvationRisk: 'None',
    fairness: 'Very High (Strict FIFO)',
    timeComplexity: 'O(N)'
  };
}

/**
 * Shortest Seek Time First (SSTF)
 * Selects the request closest to the current head position.
 */
export function runSSTF(requests, initialHead, maxCylinder) {
  let pending = sanitizeRequests(requests, maxCylinder);
  const seekSequence = [initialHead];
  const steps = [];
  let currentHead = initialHead;
  let totalMovement = 0;
  let stepCount = 0;

  while (pending.length > 0) {
    stepCount++;
    // Find request with minimum distance to currentHead
    let minDiff = Infinity;
    let bestIdx = -1;

    for (let i = 0; i < pending.length; i++) {
      const diff = Math.abs(pending[i] - currentHead);
      if (diff < minDiff) {
        minDiff = diff;
        bestIdx = i;
      }
    }

    const nextTrack = pending[bestIdx];
    pending.splice(bestIdx, 1);

    totalMovement += minDiff;
    steps.push({
      stepIndex: stepCount,
      from: currentHead,
      to: nextTrack,
      distance: minDiff,
      cumulative: totalMovement,
      isBoundary: false,
      note: `Shortest seek distance: |${nextTrack} - ${currentHead}| = ${minDiff}`
    });
    seekSequence.push(nextTrack);
    currentHead = nextTrack;
  }

  const reqCount = requests.length;
  return {
    algorithm: 'SSTF',
    name: 'Shortest Seek Time First',
    initialHead,
    maxCylinder,
    totalHeadMovement: totalMovement,
    averageSeekLength: reqCount ? (totalMovement / reqCount) : 0,
    seekSequence,
    steps,
    starvationRisk: 'High (distant tracks can starve)',
    fairness: 'Low',
    timeComplexity: 'O(N²)'
  };
}

/**
 * SCAN (Elevator Algorithm)
 * Moves towards one end servicing requests until the boundary (0 or maxCylinder),
 * then reverses direction.
 */
export function runSCAN(requests, initialHead, maxCylinder, direction = 'right') {
  const reqs = sanitizeRequests(requests, maxCylinder);
  const seekSequence = [initialHead];
  const steps = [];
  let currentHead = initialHead;
  let totalMovement = 0;
  let stepCount = 0;

  const left = reqs.filter(r => r < initialHead).sort((a, b) => b - a); // descending
  const right = reqs.filter(r => r >= initialHead).sort((a, b) => a - b); // ascending

  if (direction === 'right') {
    // Service right towards maxCylinder
    for (const track of right) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `Moving right/up towards cylinder ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }

    // If there are left requests, must hit the end boundary (maxCylinder) before reversing
    if (left.length > 0) {
      if (currentHead !== maxCylinder) {
        stepCount++;
        const dist = Math.abs(maxCylinder - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: maxCylinder,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: true,
          note: `Reaching disk boundary (track ${maxCylinder}) and reversing direction`
        });
        seekSequence.push(maxCylinder);
        currentHead = maxCylinder;
      }

      // Now service left requests (descending)
      for (const track of left) {
        stepCount++;
        const dist = Math.abs(track - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: track,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: false,
          note: `Moving left/down towards cylinder ${track}`
        });
        seekSequence.push(track);
        currentHead = track;
      }
    }
  } else {
    // direction === 'left', move towards 0
    for (const track of left) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `Moving left/down towards cylinder ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }

    // If there are right requests, must hit boundary (0) before reversing
    if (right.length > 0) {
      if (currentHead !== 0) {
        stepCount++;
        const dist = Math.abs(0 - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: 0,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: true,
          note: `Reaching disk boundary (track 0) and reversing direction`
        });
        seekSequence.push(0);
        currentHead = 0;
      }

      // Now service right requests (ascending)
      for (const track of right) {
        stepCount++;
        const dist = Math.abs(track - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: track,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: false,
          note: `Moving right/up towards cylinder ${track}`
        });
        seekSequence.push(track);
        currentHead = track;
      }
    }
  }

  const reqCount = reqs.length;
  return {
    algorithm: 'SCAN',
    name: 'SCAN (Elevator Algorithm)',
    direction,
    initialHead,
    maxCylinder,
    totalHeadMovement: totalMovement,
    averageSeekLength: reqCount ? (totalMovement / reqCount) : 0,
    seekSequence,
    steps,
    starvationRisk: 'Low (uniform sweep)',
    fairness: 'Moderate',
    timeComplexity: 'O(N log N)'
  };
}

/**
 * C-SCAN (Circular SCAN)
 */
export function runCSCAN(requests, initialHead, maxCylinder, direction = 'right') {
  const reqs = sanitizeRequests(requests, maxCylinder);
  const seekSequence = [initialHead];
  const steps = [];
  let currentHead = initialHead;
  let totalMovement = 0;
  let stepCount = 0;

  const left = reqs.filter(r => r < initialHead).sort((a, b) => a - b);
  const right = reqs.filter(r => r >= initialHead).sort((a, b) => a - b);

  if (direction === 'right') {
    for (const track of right) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `Servicing request at cylinder ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }

    if (left.length > 0) {
      if (currentHead !== maxCylinder) {
        stepCount++;
        const dist = Math.abs(maxCylinder - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: maxCylinder,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: true,
          note: `Reaching maximum disk boundary (${maxCylinder})`
        });
        seekSequence.push(maxCylinder);
        currentHead = maxCylinder;
      }

      // Circular jump to 0
      stepCount++;
      const distJump = Math.abs(0 - currentHead);
      totalMovement += distJump;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: 0,
        distance: distJump,
        cumulative: totalMovement,
        isBoundary: true,
        note: `Circular return jump to track 0 (no service during return)`
      });
      seekSequence.push(0);
      currentHead = 0;

      for (const track of left) {
        stepCount++;
        const dist = Math.abs(track - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: track,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: false,
          note: `Servicing remaining request at cylinder ${track}`
        });
        seekSequence.push(track);
        currentHead = track;
      }
    }
  } else {
    // direction left
    const leftDesc = reqs.filter(r => r <= initialHead).sort((a, b) => b - a);
    const rightDesc = reqs.filter(r => r > initialHead).sort((a, b) => b - a);

    for (const track of leftDesc) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `Servicing request downwards at cylinder ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }

    if (rightDesc.length > 0) {
      if (currentHead !== 0) {
        stepCount++;
        const dist = Math.abs(0 - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: 0,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: true,
          note: `Reaching minimum disk boundary (0)`
        });
        seekSequence.push(0);
        currentHead = 0;
      }

      stepCount++;
      const distJump = Math.abs(maxCylinder - currentHead);
      totalMovement += distJump;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: maxCylinder,
        distance: distJump,
        cumulative: totalMovement,
        isBoundary: true,
        note: `Circular jump to cylinder ${maxCylinder} (no service during return)`
      });
      seekSequence.push(maxCylinder);
      currentHead = maxCylinder;

      for (const track of rightDesc) {
        stepCount++;
        const dist = Math.abs(track - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: track,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: false,
          note: `Servicing remaining request downwards at cylinder ${track}`
        });
        seekSequence.push(track);
        currentHead = track;
      }
    }
  }

  const reqCount = reqs.length;
  return {
    algorithm: 'CSCAN',
    name: 'Circular SCAN (C-SCAN)',
    direction,
    initialHead,
    maxCylinder,
    totalHeadMovement: totalMovement,
    averageSeekLength: reqCount ? (totalMovement / reqCount) : 0,
    seekSequence,
    steps,
    starvationRisk: 'Very Low (uniform wait time)',
    fairness: 'High',
    timeComplexity: 'O(N log N)'
  };
}

/**
 * LOOK Algorithm
 */
export function runLOOK(requests, initialHead, maxCylinder, direction = 'right') {
  const reqs = sanitizeRequests(requests, maxCylinder);
  const seekSequence = [initialHead];
  const steps = [];
  let currentHead = initialHead;
  let totalMovement = 0;
  let stepCount = 0;

  const left = reqs.filter(r => r < initialHead).sort((a, b) => b - a);
  const right = reqs.filter(r => r >= initialHead).sort((a, b) => a - b);

  if (direction === 'right') {
    for (const track of right) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `LOOK: Servicing track ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }
    for (const track of left) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `LOOK: Reversing to service track ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }
  } else {
    for (const track of left) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `LOOK: Servicing track ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }
    for (const track of right) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `LOOK: Reversing to service track ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }
  }

  const reqCount = reqs.length;
  return {
    algorithm: 'LOOK',
    name: 'LOOK Algorithm',
    direction,
    initialHead,
    maxCylinder,
    totalHeadMovement: totalMovement,
    averageSeekLength: reqCount ? (totalMovement / reqCount) : 0,
    seekSequence,
    steps,
    starvationRisk: 'Low',
    fairness: 'Moderate',
    timeComplexity: 'O(N log N)'
  };
}

/**
 * C-LOOK (Circular LOOK)
 */
export function runCLOOK(requests, initialHead, maxCylinder, direction = 'right') {
  const reqs = sanitizeRequests(requests, maxCylinder);
  const seekSequence = [initialHead];
  const steps = [];
  let currentHead = initialHead;
  let totalMovement = 0;
  let stepCount = 0;

  const left = reqs.filter(r => r < initialHead).sort((a, b) => a - b);
  const right = reqs.filter(r => r >= initialHead).sort((a, b) => a - b);

  if (direction === 'right') {
    for (const track of right) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `C-LOOK: Servicing track ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }
    if (left.length > 0) {
      const lowestTrack = left[0];
      stepCount++;
      const jumpDist = Math.abs(lowestTrack - currentHead);
      totalMovement += jumpDist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: lowestTrack,
        distance: jumpDist,
        cumulative: totalMovement,
        isBoundary: true,
        note: `C-LOOK: Direct return jump to lowest request (track ${lowestTrack})`
      });
      seekSequence.push(lowestTrack);
      currentHead = lowestTrack;

      for (let i = 1; i < left.length; i++) {
        const track = left[i];
        stepCount++;
        const dist = Math.abs(track - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: track,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: false,
          note: `C-LOOK: Servicing track ${track}`
        });
        seekSequence.push(track);
        currentHead = track;
      }
    }
  } else {
    const leftDesc = reqs.filter(r => r <= initialHead).sort((a, b) => b - a);
    const rightDesc = reqs.filter(r => r > initialHead).sort((a, b) => b - a);

    for (const track of leftDesc) {
      stepCount++;
      const dist = Math.abs(track - currentHead);
      totalMovement += dist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: track,
        distance: dist,
        cumulative: totalMovement,
        isBoundary: false,
        note: `C-LOOK: Servicing track ${track}`
      });
      seekSequence.push(track);
      currentHead = track;
    }

    if (rightDesc.length > 0) {
      const highestTrack = rightDesc[0];
      stepCount++;
      const jumpDist = Math.abs(highestTrack - currentHead);
      totalMovement += jumpDist;
      steps.push({
        stepIndex: stepCount,
        from: currentHead,
        to: highestTrack,
        distance: jumpDist,
        cumulative: totalMovement,
        isBoundary: true,
        note: `C-LOOK: Direct return jump to highest request (track ${highestTrack})`
      });
      seekSequence.push(highestTrack);
      currentHead = highestTrack;

      for (let i = 1; i < rightDesc.length; i++) {
        const track = rightDesc[i];
        stepCount++;
        const dist = Math.abs(track - currentHead);
        totalMovement += dist;
        steps.push({
          stepIndex: stepCount,
          from: currentHead,
          to: track,
          distance: dist,
          cumulative: totalMovement,
          isBoundary: false,
          note: `C-LOOK: Servicing track ${track}`
        });
        seekSequence.push(track);
        currentHead = track;
      }
    }
  }

  const reqCount = reqs.length;
  return {
    algorithm: 'CLOOK',
    name: 'Circular LOOK (C-LOOK)',
    direction,
    initialHead,
    maxCylinder,
    totalHeadMovement: totalMovement,
    averageSeekLength: reqCount ? (totalMovement / reqCount) : 0,
    seekSequence,
    steps,
    starvationRisk: 'Very Low',
    fairness: 'High',
    timeComplexity: 'O(N log N)'
  };
}

/**
 * Execute all algorithms for comparative analysis
 */
export function runAllAlgorithms(requests, initialHead, maxCylinder, direction = 'right') {
  return {
    FCFS: runFCFS(requests, initialHead, maxCylinder),
    SSTF: runSSTF(requests, initialHead, maxCylinder),
    SCAN: runSCAN(requests, initialHead, maxCylinder, direction),
    CSCAN: runCSCAN(requests, initialHead, maxCylinder, direction),
    LOOK: runLOOK(requests, initialHead, maxCylinder, direction),
    CLOOK: runCLOOK(requests, initialHead, maxCylinder, direction)
  };
}
