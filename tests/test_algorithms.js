import { runFCFS, runSSTF, runSCAN, runCSCAN, runLOOK, runCLOOK } from '../js/algorithms.js';

/**
 * Verification test for Textbook Benchmark:
 * Silberschatz et al. (10th ed.), Chapter 11
 * Requests: [98, 183, 37, 122, 14, 124, 65, 67]
 * Initial Head: 53, Direction: Right (towards 199)
 */

const requests = [98, 183, 37, 122, 14, 124, 65, 67];
const initialHead = 53;
const maxCylinder = 199;

const fcfs = runFCFS(requests, initialHead, maxCylinder);
const sstf = runSSTF(requests, initialHead, maxCylinder);
const scan = runSCAN(requests, initialHead, maxCylinder, 'right');
const cscan = runCSCAN(requests, initialHead, maxCylinder, 'right');
const look = runLOOK(requests, initialHead, maxCylinder, 'right');
const clook = runCLOOK(requests, initialHead, maxCylinder, 'right');

console.log('--- Disk Scheduling Benchmark Test ---');
console.log('FCFS THM:', fcfs.totalHeadMovement, '(Expected: 640)', fcfs.totalHeadMovement === 640 ? '✓ PASS' : '✗ FAIL');
console.log('SSTF THM:', sstf.totalHeadMovement, '(Expected: 236)', sstf.totalHeadMovement === 236 ? '✓ PASS' : '✗ FAIL');
console.log('SCAN THM:', scan.totalHeadMovement, '(Expected: 331)', scan.totalHeadMovement === 331 ? '✓ PASS' : '✗ FAIL');
console.log('C-SCAN THM:', cscan.totalHeadMovement, '(Expected: 382)', cscan.totalHeadMovement === 382 ? '✓ PASS' : '✗ FAIL');
console.log('LOOK THM:', look.totalHeadMovement, '(Expected: 299)', look.totalHeadMovement === 299 ? '✓ PASS' : '✗ FAIL');
console.log('C-LOOK THM:', clook.totalHeadMovement, '(Expected: 322)', clook.totalHeadMovement === 322 ? '✓ PASS' : '✗ FAIL');
