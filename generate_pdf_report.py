import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = "Disk_Scheduling_Algorithms_Performance_Analysis_Report.pdf"
SCREENSHOTS_DIR = "screenshots"

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page count
    and professional running headers/footers.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress header and footer on cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header
        header_text = "Disk Scheduling Algorithms: FCFS, SSTF & SCAN Analysis  |  Akshat Joshi"
        self.drawString(45, 805, header_text)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(45, 798, 550, 798)

        # Running Footer
        footer_text = f"Unit VI: Storage Management • Operating Systems Project"
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(45, 30, footer_text)
        self.drawRightString(550, 30, page_str)
        self.line(45, 40, 550, 40)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=52,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0f2438")     # Deep Navy
    SECONDARY = colors.HexColor("#0284c7")   # Electric Blue / Cyan
    ACCENT = colors.HexColor("#0d9488")      # Teal / Cyan
    TEXT_DARK = colors.HexColor("#1e293b")   # Slate Dark
    TEXT_MUTED = colors.HexColor("#64748b")  # Slate Muted
    BG_LIGHT = colors.HexColor("#f8fafc")    # Light slate bg
    BORDER_CLR = colors.HexColor("#e2e8f0")  # Border gray

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=SECONDARY,
        alignment=0
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=21,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=14,
        bulletIndent=4,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#0369a1")
    )

    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
        alignment=1,
        spaceBefore=4,
        spaceAfter=8
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    # Academic Header Banner
    story.append(Paragraph("<font size=10 color='#64748b'><b>OPERATING SYSTEMS LAB • SPECIAL DIRECT READING PROJECT (25 POINTS)</b></font>", body_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=3, color=SECONDARY, spaceAfter=20, spaceBefore=0))

    story.append(Paragraph("Disk Scheduling Algorithms: FCFS, SSTF and SCAN Performance Analysis", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("A Comprehensive Theoretical, Mathematical, and Graphical Simulation Study with Step-by-Step Trajectory Verification", subtitle_style))
    story.append(Spacer(1, 25))

    # Cover Metadata Card
    meta_data = [
        [Paragraph("<b>Assigned Student:</b>", body_style), Paragraph("Akshat Joshi", body_style)],
        [Paragraph("<b>Course Module:</b>", body_style), Paragraph("Unit VI: Storage Management (Mass-Storage Structure)", body_style)],
        [Paragraph("<b>Project Category:</b>", body_style), Paragraph("Algorithmic Implementation, Performance Benchmark & Interactive GUI Simulation", body_style)],
        [Paragraph("<b>Primary Algorithms:</b>", body_style), Paragraph("FCFS (First-Come, First-Served), SSTF (Shortest Seek Time First), SCAN (Elevator)", body_style)],
        [Paragraph("<b>Extended Algorithms:</b>", body_style), Paragraph("C-SCAN (Circular SCAN), LOOK, C-LOOK", body_style)],
        [Paragraph("<b>Evaluation Criteria:</b>", body_style), Paragraph("Total Head Movement (THM), Average Seek Length (ASL), Starvation, Arm Inertia", body_style)],
        [Paragraph("<b>Academic Session:</b>", body_style), Paragraph("2026–2027", body_style)],
        [Paragraph("<b>Standard Benchmark:</b>", body_style), Paragraph("Silberschatz et al. (10th Ed.) Benchmark Sequence: [98, 183, 37, 122, 14, 124, 65, 67] at Head 53", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[150, 350])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 25))

    # Cover Overview Screenshot Preview
    dash_img_path = os.path.join(SCREENSHOTS_DIR, "01_full_dashboard.png")
    if os.path.exists(dash_img_path):
        # Cropped preview of top of dashboard
        story.append(Paragraph("<b>Figure: Interactive Simulation Dashboard (High-Resolution View)</b>", caption_style))
        # Keep width 500 pt, height 260 pt
        img_dash = Image(dash_img_path, width=505, height=270)
        story.append(img_dash)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: PROJECT OVERVIEW & OBJECTIVES
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Project Objectives", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "Magnetic disk drives represent one of the critical mechanical bottlenecks in secondary computer storage. "
        "Because mechanical movement of the read/write head assembly is thousands of times slower than solid-state "
        "semiconductor memory transactions, the disk scheduling algorithm chosen by the operating system kernel directly "
        "governs overall I/O throughput, system latency, and multi-tasking responsiveness.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Core Deliverables Accomplished in this Project:</b>",
        body_style
    ))
    story.append(Paragraph("• <b>Full Interactive GUI Simulator:</b> Designed with an aesthetic dark glassmorphic interface, real-time physical magnetic platter animation, concentric cylinder track rings, and an actuator arm seeking across tracks in real time.", bullet_style))
    story.append(Paragraph("• <b>Rigorous Algorithmic Implementation:</b> Complete implementation of the three required core algorithms (FCFS, SSTF, SCAN) and three advanced industrial extensions (C-SCAN, LOOK, C-LOOK).", bullet_style))
    story.append(Paragraph("• <b>Mathematical Formulation & Verification:</b> Verification against standard textbook benchmark problems (Silberschatz et al., 10th Edition), computing step-by-step seek distances (|C<sub>i</sub> - C<sub>i-1</sub>|), Total Head Movement (THM), and Average Seek Length (ASL).", bullet_style))
    story.append(Paragraph("• <b>Multi-Dimensional Graphical Visualization:</b> Classical textbook cylinder trajectory plots (Arm Seek Trajectory) and comparative performance bar charts dynamically plotted via Chart.js.", bullet_style))
    story.append(Paragraph("• <b>Comprehensive Comparative Matrix:</b> Detailed side-by-side evaluation matrix benchmarking seek efficiency, rotational latency implications, mechanical wear, and starvation risks.", bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: DISK HARDWARE MECHANICS & FORMULAS
    # =========================================================================
    story.append(Paragraph("2. Hard Disk Physical Mechanics & Mathematical Framework", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "A traditional Hard Disk Drive (HDD) consists of one or more flat circular platters coated with magnetic material. "
        "Each platter surface is logically organized into microscopic concentric rings called <b>tracks</b>. Tracks at the same "
        "radial radius across all platters constitute a <b>cylinder</b>. To service an I/O request, the operating system must "
        "position the read/write head over the target cylinder.",
        body_style
    ))

    story.append(Paragraph("<b>Components of Disk Access Time:</b>", h2_style))
    story.append(Paragraph(
        "The total time required to service a disk read or write request is given by:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>T<sub>access</sub> = T<sub>seek</sub> + T<sub>rotational</sub> + T<sub>transfer</sub> + T<sub>controller</sub></b>",
        body_style
    ))
    story.append(Paragraph("• <b>Seek Time (T<sub>seek</sub>):</b> The time required for the actuator arm to physically move the read/write head to the addressed cylinder. <i>This is the dominant mechanical delay minimized by disk scheduling algorithms.</i>", bullet_style))
    story.append(Paragraph("• <b>Rotational Latency (T<sub>rotational</sub>):</b> The delay waiting for the requested sector to rotate beneath the read/write head. Average rotational latency is half a revolution (e.g., ~4.17 ms for a 7200 RPM drive).", bullet_style))
    story.append(Paragraph("• <b>Transfer Time (T<sub>transfer</sub>):</b> The time needed to magnetically read or write the actual data bits from the sector as it passes under the head.", bullet_style))

    story.append(Paragraph("<b>Key Quantitative Evaluation Metrics:</b>", h2_style))

    metrics_table_data = [
        [Paragraph("<b>Metric</b>", body_style), Paragraph("<b>Mathematical Formula</b>", body_style), Paragraph("<b>Operational Definition</b>", body_style)],
        [
            Paragraph("<b>Total Head Movement (THM)</b>", body_style),
            Paragraph("<b>THM = &Sigma;<sub>i=1..N</sub> |C<sub>i</sub> - C<sub>i-1</sub>|</b>", body_style),
            Paragraph("Cumulative absolute cylinder tracks traversed by the head from initial position C<sub>0</sub> across all N serviced requests.", body_style)
        ],
        [
            Paragraph("<b>Average Seek Length (ASL)</b>", body_style),
            Paragraph("<b>ASL = THM / N</b>", body_style),
            Paragraph("Mean track displacement per I/O request. Indicates the expected mechanical travel distance per operation.", body_style)
        ],
        [
            Paragraph("<b>Estimated Seek Time (T<sub>seek</sub>)</b>", body_style),
            Paragraph("<b>T<sub>seek</sub> = THM &times; t<sub>track</sub></b>", body_style),
            Paragraph("Total mechanical seek latency in milliseconds, where t<sub>track</sub> is the track-to-track seek latency factor (default: 5.0 ms).", body_style)
        ],
        [
            Paragraph("<b>Percentage Efficiency Gain (&eta;)</b>", body_style),
            Paragraph("<b>&eta; = ((THM<sub>FCFS</sub> - THM<sub>alg</sub>) / THM<sub>FCFS</sub>) &times; 100%</b>", body_style),
            Paragraph("Quantifies percentage reduction in head movement achieved relative to unoptimized baseline FCFS.", body_style)
        ]
    ]
    t_metrics = Table(metrics_table_data, colWidths=[130, 160, 215])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f2438")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,1), (-1,-1), 5),
        ('BOTTOMPADDING', (0,1), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_metrics)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: THEORETICAL ANALYSIS OF ALGORITHMS
    # =========================================================================
    story.append(Paragraph("3. In-Depth Algorithmic Principles & Mechanics", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph("3.1 First-Come, First-Served (FCFS)", h2_style))
    story.append(Paragraph(
        "<b>Operational Principle:</b> FCFS is the simplest disk scheduling algorithm. It maintains an unmodified FIFO (First-In, First-Out) queue. "
        "Requests are serviced strictly in the chronological order of their arrival into the I/O subsystem. "
        "The disk controller makes no attempt to optimize seek direction or group requests by cylinder proximity.",
        body_style
    ))
    story.append(Paragraph("• <b>Advantages:</b> Completely fair to all processes; mathematically immune to process starvation; trivial to implement with O(1) scheduling complexity.", bullet_style))
    story.append(Paragraph("• <b>Disadvantages:</b> Highly erratic head oscillations (the 'wild swing' phenomenon); high average seek length; unacceptable performance in high-throughput database systems.", bullet_style))

    story.append(Paragraph("3.2 Shortest Seek Time First (SSTF)", h2_style))
    story.append(Paragraph(
        "<b>Operational Principle:</b> SSTF selects the pending request that requires the minimum head movement from the current cylinder position: "
        "<i>Next = argmin<sub>r &isin; Q</sub> |C<sub>current</sub> - r|</i>. In the event of a tie between two equidistant requests, "
        "the tie is conventionally broken by preserving the current direction of head motion.",
        body_style
    ))
    story.append(Paragraph("• <b>Advantages:</b> Substantially reduces Total Head Movement compared to FCFS; approaches the optimal seek time for localized workloads; simple greedy heuristic.", bullet_style))
    story.append(Paragraph("• <b>Disadvantages:</b> <b>High Risk of Starvation:</b> In a heavily loaded system with continuous localized requests, requests on distant tracks may never be serviced (indefinite postponement); not mathematically optimal across the entire sequence.", bullet_style))

    story.append(Paragraph("3.3 SCAN (The Elevator Algorithm)", h2_style))
    story.append(Paragraph(
        "<b>Operational Principle:</b> Analogous to an architectural elevator, the disk arm starts at one end of the disk and sweeps "
        "across cylinders towards the opposite end, servicing all requests encountered along its path. Upon reaching the physical disk boundary "
        "(Cylinder 0 or Max Cylinder), the arm reverses direction and sweeps back, servicing requests in the reverse order.",
        body_style
    ))
    story.append(Paragraph("• <b>Advantages:</b> Eliminates starvation because the arm guarantees servicing all requests within two complete sweeps; significantly smoother seek trajectories and reduced mechanical stress.", bullet_style))
    story.append(Paragraph("• <b>Disadvantages:</b> Unfair delay distribution: cylinders immediately behind the reversing arm must wait for a full round-trip sweep; always travels to the extreme disk boundary even when no pending requests reside there.", bullet_style))

    story.append(Paragraph("3.4 Extended Industrial Algorithms (C-SCAN, LOOK, C-LOOK)", h2_style))
    story.append(Paragraph(
        "• <b>C-SCAN (Circular SCAN):</b> Designed to provide uniform waiting times. Like SCAN, it sweeps in one direction servicing requests. "
        "However, upon reaching the boundary, it instantly resets back to the opposite boundary <i>without servicing requests on the return trip</i>.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>LOOK:</b> A practical optimization over SCAN. The arm only travels as far as the <i>final pending request</i> in the current direction. "
        "If no further requests exist ahead, it reverses immediately without traveling to the unused physical disk boundary.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>C-LOOK:</b> Combines C-SCAN's circular fairness with LOOK's boundary optimization. It reverses direction immediately at the highest "
        "pending request and resets to the lowest pending request, eliminating unnecessary travel to track 0 or track Max.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # Algorithm Comparison Table
    alg_summary_data = [
        [Paragraph("<b>Algorithm</b>", body_style), Paragraph("<b>Core Heuristic</b>", body_style), Paragraph("<b>Boundary Behavior</b>", body_style), Paragraph("<b>Starvation Risk</b>", body_style), Paragraph("<b>Time Complexity</b>", body_style)],
        [Paragraph("<b>FCFS</b>", body_style), Paragraph("FIFO arrival order", body_style), Paragraph("No boundary awareness", body_style), Paragraph("<font color='#16a34a'><b>Zero (Fair)</b></font>", body_style), Paragraph("O(N)", body_style)],
        [Paragraph("<b>SSTF</b>", body_style), Paragraph("Min |C<sub>curr</sub> - r| greedy", body_style), Paragraph("Opportunistic seek", body_style), Paragraph("<font color='#dc2626'><b>High</b></font>", body_style), Paragraph("O(N<sup>2</sup>)", body_style)],
        [Paragraph("<b>SCAN</b>", body_style), Paragraph("Bidirectional continuous sweep", body_style), Paragraph("Travels to physical limit (0 / Max)", body_style), Paragraph("<font color='#16a34a'><b>None</b></font>", body_style), Paragraph("O(N log N)", body_style)],
        [Paragraph("<b>C-SCAN</b>", body_style), Paragraph("Unidirectional circular sweep", body_style), Paragraph("Resets from limit to limit", body_style), Paragraph("<font color='#16a34a'><b>None (Uniform)</b></font>", body_style), Paragraph("O(N log N)", body_style)],
        [Paragraph("<b>LOOK</b>", body_style), Paragraph("Bidirectional request-bound sweep", body_style), Paragraph("Reverses at extreme request", body_style), Paragraph("<font color='#16a34a'><b>None</b></font>", body_style), Paragraph("O(N log N)", body_style)],
        [Paragraph("<b>C-LOOK</b>", body_style), Paragraph("Unidirectional request-bound sweep", body_style), Paragraph("Resets to lowest request", body_style), Paragraph("<font color='#16a34a'><b>None (Uniform)</b></font>", body_style), Paragraph("O(N log N)", body_style)],
    ]
    t_alg_summary = Table(alg_summary_data, colWidths=[65, 140, 130, 95, 75])
    t_alg_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f2438")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,1), (-1,-1), 4),
        ('BOTTOMPADDING', (0,1), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_alg_summary)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: BENCHMARK DATASET & STEP-BY-STEP CALCULATIONS
    # =========================================================================
    story.append(Paragraph("4. Benchmark Dataset & Mathematical Step Calculations", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "To rigorously validate the algorithmic implementations, we execute the classic benchmark workload from "
        "<i>Operating System Concepts</i> (Silberschatz, Galvin & Gagne, 10th Edition, Chapter 11):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Disk Cylinder Range:</b> 0 to 199 (Total 200 tracks)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Initial Read/Write Head Position:</b> Cylinder 53<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Initial Arm Direction:</b> Right / High (Towards Cylinder 199)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>I/O Request Queue Sequence:</b> [98, 183, 37, 122, 14, 124, 65, 67]",
        body_style
    ))

    story.append(Paragraph("4.1 FCFS Step-by-Step Calculation Breakdown", h2_style))
    fcfs_steps_data = [
        ["Step #", "From", "To", "Seek Formula", "Distance (|Δ|)", "Cumulative THM", "Operational Rationale"],
        ["1", "53", "98", "|98 - 53|", "45", "45", "Servicing 1st arrival in FIFO queue"],
        ["2", "98", "183", "|183 - 98|", "85", "130", "Large outward swing to track 183"],
        ["3", "183", "37", "|37 - 183|", "146", "276", "Massive inward reversal across platters"],
        ["4", "37", "122", "|122 - 37|", "85", "361", "Outward swing back towards outer tracks"],
        ["5", "122", "14", "|14 - 122|", "108", "469", "Severe inward swing to inner track 14"],
        ["6", "14", "124", "|124 - 14|", "110", "579", "Severe outward reversal to track 124"],
        ["7", "124", "65", "|65 - 124|", "59", "638", "Inward seek towards middle tracks"],
        ["8", "65", "67", "|67 - 65|", "2", "640", "Final nearby sequential request"]
    ]
    t_fcfs = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body_style) for c in row] for r, row in enumerate(fcfs_steps_data)], colWidths=[45, 38, 38, 85, 75, 95, 129])
    t_fcfs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f2438")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_fcfs)
    story.append(Paragraph("<b>FCFS Summary:</b> Total Head Movement = <b>640 cylinders</b> | Average Seek Length = <b>80.00 tracks/req</b>", callout_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.2 SSTF Step-by-Step Calculation Breakdown", h2_style))
    sstf_steps_data = [
        ["Step #", "From", "To", "Seek Formula", "Distance (|Δ|)", "Cumulative THM", "Operational Rationale"],
        ["1", "53", "65", "|65 - 53|", "12", "12", "Nearest cylinder to initial head 53"],
        ["2", "65", "67", "|67 - 65|", "2", "14", "Nearest cylinder to 65 (|67-65|=2 vs |37-65|=28)"],
        ["3", "67", "37", "|37 - 67|", "30", "44", "Nearest remaining cylinder (|37-67|=30 vs |98-67|=31)"],
        ["4", "37", "14", "|14 - 37|", "23", "67", "Nearest remaining cylinder to 37"],
        ["5", "14", "98", "|98 - 14|", "84", "151", "Left side exhausted; seek to nearest right"],
        ["6", "98", "122", "|122 - 98|", "24", "175", "Nearest cylinder to 98"],
        ["7", "122", "124", "|124 - 122|", "2", "177", "Adjacent cylinder seek"],
        ["8", "124", "183", "|183 - 124|", "59", "236", "Final remaining outermost cylinder"]
    ]
    t_sstf = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body_style) for c in row] for r, row in enumerate(sstf_steps_data)], colWidths=[45, 38, 38, 85, 75, 95, 129])
    t_sstf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f0fdf4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sstf)
    story.append(Paragraph("<b>SSTF Summary:</b> Total Head Movement = <b>236 cylinders</b> | Average Seek Length = <b>29.50 tracks/req</b> (63.1% reduction vs FCFS)", callout_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.3 SCAN Step-by-Step Calculation Breakdown", h2_style))
    scan_steps_data = [
        ["Step #", "From", "To", "Seek Formula", "Distance (|Δ|)", "Cumulative THM", "Operational Rationale"],
        ["1", "53", "65", "|65 - 53|", "12", "12", "Sweeping Right: first request above 53"],
        ["2", "65", "67", "|67 - 65|", "2", "14", "Sweeping Right: next request along path"],
        ["3", "67", "98", "|98 - 67|", "31", "45", "Sweeping Right: servicing cylinder 98"],
        ["4", "98", "122", "|122 - 98|", "24", "69", "Sweeping Right: servicing cylinder 122"],
        ["5", "122", "124", "|124 - 122|", "2", "71", "Sweeping Right: servicing cylinder 124"],
        ["6", "124", "183", "|183 - 124|", "59", "130", "Sweeping Right: highest request serviced"],
        ["7", "183", "199", "|199 - 183|", "16", "146", "Reaches physical boundary limit (199); reverses"],
        ["8", "199", "37", "|37 - 199|", "162", "308", "Sweeping Left: first pending request encountered"],
        ["9", "37", "14", "|14 - 37|", "23", "331", "Sweeping Left: final remaining inner request"]
    ]
    t_scan = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body_style) for c in row] for r, row in enumerate(scan_steps_data)], colWidths=[45, 38, 38, 85, 75, 95, 129])
    t_scan.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0d9488")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f0fdfa")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_scan)
    story.append(Paragraph("<b>SCAN Summary:</b> Total Head Movement = <b>331 cylinders</b> | Average Seek Length = <b>41.38 tracks/req</b> (48.3% reduction vs FCFS)", callout_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: SIMULATION SCREENSHOTS & VISUAL VERIFICATION
    # =========================================================================
    story.append(Paragraph("5. Interactive Simulator Implementation & Live Verification", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "To provide an intuitive and comprehensive demonstration of disk scheduling behavior, we implemented "
        "a client-side simulation suite using HTML5, Canvas API, Chart.js, and ES6 modular JavaScript. "
        "Below are actual high-resolution captures from the working simulator verifying every component.",
        body_style
    ))

    # Configuration & Controls Screenshot
    config_img = os.path.join(SCREENSHOTS_DIR, "02_configuration_panel.png")
    if os.path.exists(config_img):
        story.append(Paragraph("<b>Figure 1: Disk Parameters & Request Sequence Configuration Panel</b>", caption_style))
        story.append(Image(config_img, width=505, height=84))
        story.append(Spacer(1, 6))

    # Platter & Ruler Screenshot
    platter_img = os.path.join(SCREENSHOTS_DIR, "03_hardware_visualizer.png")
    if os.path.exists(platter_img):
        story.append(Paragraph("<b>Figure 2: Live Mechanical Hard Disk Platter & Linear Cylinder Track Ruler</b>", caption_style))
        story.append(Image(platter_img, width=505, height=165))
        story.append(Paragraph(
            "<i>Left:</i> Real-time rotating magnetic platter with concentric cylinder rings, spindle motor, and pivoting actuator arm. "
            "<i>Right:</i> Linear cylinder scale (0 to 199) with active head indicator (blue bar), pending request markers (orange), and step playback controller.",
            caption_style
        ))
        story.append(Spacer(1, 6))

    # Active seeking state
    active_img = os.path.join(SCREENSHOTS_DIR, "04_active_seeking_state.png")
    if os.path.exists(active_img):
        story.append(Paragraph("<b>Figure 3: Active Simulation Playback (Serviced Cylinders Turning Green)</b>", caption_style))
        story.append(Image(active_img, width=505, height=165))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: TRAJECTORY PLOTS & GRAPHICAL ANALYSIS
    # =========================================================================
    story.append(Paragraph("6. Trajectory Plots & Comparative Visual Analytics", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "The standard Silberschatz Operating Systems textbook utilizes a 2D Trajectory Plot where the <b>horizontal axis represents "
        "disk cylinder numbers (0 to 199)</b> and the <b>vertical axis represents chronological servicing order (Step 0 to N)</b>. "
        "The slopes and path lengths directly illustrate the mechanical efficiency of the arm motion.",
        body_style
    ))

    fcfs_chart = os.path.join(SCREENSHOTS_DIR, "05_trajectory_fcfs.png")
    sstf_chart = os.path.join(SCREENSHOTS_DIR, "06_trajectory_sstf.png")
    scan_chart = os.path.join(SCREENSHOTS_DIR, "07_trajectory_scan.png")

    if os.path.exists(fcfs_chart) and os.path.exists(sstf_chart):
        t_charts = Table([
            [Image(fcfs_chart, width=248, height=148), Image(sstf_chart, width=248, height=148)],
            [Paragraph("<b>Figure 4: FCFS Trajectory (THM: 640)</b><br/>Notice extreme back-and-forth arm oscillations.", caption_style),
             Paragraph("<b>Figure 5: SSTF Trajectory (THM: 236)</b><br/>Localized greedy sweeps with minimal distance.", caption_style)]
        ], colWidths=[252, 252])
        t_charts.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t_charts)
        story.append(Spacer(1, 6))

    overlay_chart = os.path.join(SCREENSHOTS_DIR, "08_trajectory_overlay_all.png")
    bars_chart = os.path.join(SCREENSHOTS_DIR, "09_comparison_barcharts.png")

    if os.path.exists(overlay_chart) and os.path.exists(bars_chart):
        t_charts2 = Table([
            [Image(overlay_chart, width=248, height=148), Image(bars_chart, width=248, height=148)],
            [Paragraph("<b>Figure 6: Multi-Algorithm Trajectory Overlay</b><br/>Simultaneous comparison of all arm pathways.", caption_style),
             Paragraph("<b>Figure 7: Comparative Performance Bar Charts</b><br/>Total Head Movement & Average Seek Length.", caption_style)]
        ], colWidths=[252, 252])
        t_charts2.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t_charts2)

    story.append(Spacer(1, 10))

    # Mathematical Calculation Table Screenshot
    calc_table_img = os.path.join(SCREENSHOTS_DIR, "10_step_calculation_table.png")
    if os.path.exists(calc_table_img):
        story.append(Paragraph("<b>Figure 8: Live In-App Mathematical Step-by-Step Calculation Table</b>", caption_style))
        story.append(Image(calc_table_img, width=505, height=248))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 7: COMPARATIVE EVALUATION & RESULTS MATRIX
    # =========================================================================
    story.append(Paragraph("7. Comprehensive Comparative Results & Performance Evaluation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "Table 1 presents the full comparative performance benchmark across all evaluated algorithms on the Silberschatz dataset, "
        "calculated at an industry-standard track-to-track seek latency factor of <b>t<sub>track</sub> = 5.0 ms</b>.",
        body_style
    ))

    # Comprehensive Matrix Table
    comp_matrix_data = [
        ["Algorithm", "Total Head Movement", "Avg Seek Length", "Est. Seek Time", "Efficiency Gain vs FCFS", "Starvation Risk", "Arm Wear Index"],
        ["FCFS", "640 cylinders", "80.00 tracks/req", "3,200.0 ms", "Baseline (0.0%)", "Zero (Fair)", "Severe (High Stress)"],
        ["SSTF", "236 cylinders", "29.50 tracks/req", "1,180.0 ms", "+63.1% Gain", "High Risk", "Moderate"],
        ["SCAN", "331 cylinders", "41.38 tracks/req", "1,655.0 ms", "+48.3% Gain", "Zero (Fair)", "Low (Smooth Sweep)"],
        ["C-SCAN", "382 cylinders", "47.75 tracks/req", "1,910.0 ms", "+40.3% Gain", "Zero (Fair)", "Low (Circular Sweep)"],
        ["LOOK", "299 cylinders", "37.38 tracks/req", "1,495.0 ms", "+53.3% Gain", "Zero (Fair)", "Very Low (Optimal Range)"],
        ["C-LOOK", "322 cylinders", "40.25 tracks/req", "1,610.0 ms", "+49.7% Gain", "Zero (Fair)", "Very Low (Optimal Circular)"]
    ]
    t_comp_matrix = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body_style) for c in row] for r, row in enumerate(comp_matrix_data)], colWidths=[65, 80, 75, 75, 80, 65, 65])
    t_comp_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f2438")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#f8fafc"), colors.HexColor("#ffffff")]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_comp_matrix)
    story.append(Spacer(1, 10))

    # In-App Matrix Screenshot
    matrix_img = os.path.join(SCREENSHOTS_DIR, "11_comparative_matrix.png")
    if os.path.exists(matrix_img):
        story.append(Paragraph("<b>Figure 9: In-App Comparative Results Matrix & Workload Behavioral Breakdown</b>", caption_style))
        story.append(Image(matrix_img, width=505, height=295))
        story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Analytical Insights & Engineering Trade-Offs:</b>", h2_style))
    story.append(Paragraph(
        "1. <b>Seek Distance vs. Fairness:</b> While <b>SSTF achieves the lowest THM (236 cylinders)</b>, its greedy nature introduces unacceptable "
        "starvation for edge cylinders. In production servers with heavy I/O load, SCAN and LOOK are universally preferred because they provide "
        "bounded response times without starvation.",
        body_style
    ))
    story.append(Paragraph(
        "2. <b>Mechanical Stress & Arm Inertia:</b> Disk arm heads are physical assemblies subject to momentum and friction. "
        "FCFS requires rapid reversals, generating significant mechanical vibration and heat. SCAN and C-SCAN move monotonically, "
        "drastically reducing physical wear-and-tear.",
        body_style
    ))
    story.append(Paragraph(
        "3. <b>LOOK vs. SCAN Superiority:</b> LOOK eliminates SCAN's redundant travel to track 199, trimming seek distance from 331 to 299 cylinders "
        "(a 32-track savings, representing nearly 10% efficiency boost).",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 8: REAL-WORLD OS IMPLEMENTATION & REFERENCES
    # =========================================================================
    story.append(Paragraph("8. Modern Operating System Context & Storage Evolution", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "In production enterprise operating systems such as the Linux kernel, disk scheduling principles have evolved into sophisticated "
        "I/O elevator subsystems:",
        body_style
    ))
    story.append(Paragraph("• <b>Deadline Scheduler:</b> Implements a modified SCAN/LOOK sweep but imposes strict FIFO expiration timers (e.g., 500 ms for reads, 5 s for writes) to guarantee that starvation cannot occur even under saturating workloads.", bullet_style))
    story.append(Paragraph("• <b>CFQ (Completely Fair Queuing):</b> Allocates proportional I/O time slices to competing processes, interleaving SCAN-like sweeps within each process's synchronous queue.", bullet_style))
    story.append(Paragraph("• <b>BFQ (Budget Fair Queueing):</b> Enhances CFQ by allocating sector budgets instead of time slices, providing guaranteed minimum bandwidth for interactive audio/video streams.", bullet_style))
    story.append(Paragraph("• <b>Modern Solid-State Drives (SSDs) & NVMe:</b> Flash memory has no moving arm or rotational latency, making physical track seeking obsolete. Instead, SSD I/O schedulers (such as <i>None</i> / <i>MQ-Deadline</i> / <i>Kyber</i>) focus on multi-queue parallelism, wear-leveling, and garbage collection serialization.", bullet_style))

    story.append(Spacer(1, 10))

    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))
    story.append(Paragraph(
        "This project successfully developed an interactive, highly visual, and mathematically rigorous simulator for disk scheduling algorithms. "
        "Through empirical simulation of the Silberschatz benchmark, we quantitatively demonstrated that <b>SSTF (236 cylinders)</b> and "
        "<b>LOOK (299 cylinders)</b> deliver superior mechanical efficiency over unoptimized <b>FCFS (640 cylinders)</b>, while <b>SCAN and C-SCAN</b> "
        "provide the optimal engineering balance between high throughput and deterministic starvation prevention.",
        body_style
    ))

    story.append(Spacer(1, 15))

    story.append(Paragraph("10. Authentic Academic References", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10, spaceBefore=2))

    refs = [
        "<b>[1] Silberschatz, A., Galvin, P. B., & Gagne, G. (2018).</b> <i>Operating System Concepts</i> (10th Edition). Chapter 11: Mass-Storage Structure (Disk Structure, Disk Scheduling, Swap-Space Management). John Wiley & Sons. ISBN: 978-1-119-32091-3.",
        "<b>[2] Tanenbaum, A. S., & Bos, H. (2015).</b> <i>Modern Operating Systems</i> (4th Edition). Chapter 5: Input/Output (Disk Hardware, Disk Formatting, Disk Arm Scheduling Algorithms). Pearson. ISBN: 978-0-13-359162-0.",
        "<b>[3] Stallings, W. (2018).</b> <i>Operating Systems: Internals and Design Principles</i> (9th Edition). Chapter 11: I/O Management and Disk Scheduling. Pearson Education. ISBN: 978-0-13-467095-9.",
        "<b>[4] Bovet, D. P., & Cesati, M. (2005).</b> <i>Understanding the Linux Kernel</i> (3rd Edition). Chapter 14: The Block Device Driver Architecture & I/O Schedulers. O'Reilly Media.",
        "<b>[5] Love, R. (2010).</b> <i>Linux Kernel Development</i> (3rd Edition). Chapter 14: The Block I/O Layer & Elevator Architecture. Addison-Wesley Professional."
    ]
    for r in refs:
        story.append(Paragraph(r, bullet_style))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
