# Disk Scheduling Algorithms Simulator & Performance Analysis

**Assigned Student:** Akshat Joshi  
**Course Module:** Unit VI: Storage Management  
**Project Title:** Disk Scheduling Algorithms: FCFS, SSTF and SCAN Performance Analysis  

---

## Project Overview
This project is an interactive, high-fidelity graphical simulator and comparative performance analysis tool for Disk Scheduling Algorithms covered in the standard Operating Systems syllabus (Silberschatz et al.). 

It implements and evaluates the primary required algorithms:
- **FCFS** (First-Come, First-Served)
- **SSTF** (Shortest Seek Time First)
- **SCAN** (Elevator Algorithm)

As well as extended industry algorithms:
- **C-SCAN** (Circular SCAN)
- **LOOK**
- **C-LOOK** (Circular LOOK)

---

## Deliverables Accomplished
1. **Interactive Graphical User Interface (GUI)**:
   - Modern dark glassmorphic design system with vibrant telemetry cues.
   - Interactive physical hard drive assembly with a rotating magnetic platter, concentric cylinder track rings, and an actuator arm that seeks in real time.
   - Dynamic linear cylinder track ruler (0 to Max) with request markers and active head indicator.
   - Step-by-step playback controller with Play/Pause, Step Forward/Backward, Reset, and Speed multiplier (0.5x to 3.0x).
2. **Flexible Request Sequences**:
   - Standard Silberschatz benchmark preset (`98, 183, 37, 122, 14, 124, 65, 67` at head `53`).
   - Workload presets: localized clustering, ping-pong alternating extremes, sequential sweep.
   - Randomized queue generator and custom input parser with boundary validation.
3. **Step-by-Step Head-Movement Calculations**:
   - Detailed calculation table with $|C_i - C_{i-1}|$ seek formula breakdowns, seek distance, cumulative total head movement (THM), and operational rationale.
4. **Comparative Results Matrix**:
   - Side-by-side performance grid comparing THM, Average Seek Length, estimated seek time, efficiency vs baseline FCFS, starvation risk, and time complexity.
5. **Multi-Dimensional Graphs**:
   - Classic Silberschatz OS Textbook Trajectory Plot (Cylinder on X-axis vs Step Order on Y-axis) with single-algorithm view and multi-algorithm overlay mode.
   - Comparative Bar Charts for Total Head Movement and Average Seek Length.
6. **Academic Report Generator**:
   - Formatted academic report export ready for PDF printing with student details, parameters, tables, and theoretical citations.

---

## Mathematical Framework & Formulas

### 1. Total Head Movement (THM)
$$\text{THM} = \sum_{i=1}^{N} |C_i - C_{i-1}|$$
where $C_0$ is the initial head position, and $C_i$ is the cylinder serviced at step $i$.

### 2. Average Seek Length (ASL)
$$\text{ASL} = \frac{\text{THM}}{N}$$
where $N$ is the total number of serviced requests.

### 3. Estimated Seek Time ($T_{\text{seek}}$)
$$T_{\text{seek}} = \text{THM} \times t_{\text{track}}$$
where $t_{\text{track}}$ is the track-to-track seek latency in milliseconds.

---

## How to Run the Project Locally

### Option 1: Double-click or open directly
Simply double-click or open `index.html` in any modern web browser (Google Chrome, Microsoft Edge, Firefox, Safari).

### Option 2: Run via Python built-in HTTP server
```bash
python -m http.server 8000
```
Then navigate to: `http://localhost:8000`

### Option 3: Run via Node.js
```bash
npx serve .
```

---

## Authentic Academic References
1. **Silberschatz, A., Galvin, P. B., & Gagne, G. (2018).** *Operating System Concepts* (10th Edition). Chapter 11: Mass-Storage Structure. John Wiley & Sons.
2. **Tanenbaum, A. S., & Bos, H. (2015).** *Modern Operating Systems* (4th Edition). Chapter 5: Input/Output. Pearson.
3. **Stallings, W. (2018).** *Operating Systems: Internals and Design Principles* (9th Edition). Chapter 11: I/O Management and Disk Scheduling. Pearson.
