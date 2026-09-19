import os
import sys
from reportlab.lib.pagesizes import A4
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
    and professional running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total report pages generated: {num_pages}")
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
        header_text = "Disk Scheduling Algorithms: FCFS, SSTF & SCAN Performance Analysis  |  Akshat Joshi"
        self.drawString(45, 805, header_text)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(45, 798, 550, 798)

        # Running Footer
        footer_text = "Unit VI: Storage Management • Operating Systems Lab Special Project"
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(45, 30, footer_text)
        self.drawRightString(550, 30, page_str)
        self.line(45, 40, 550, 40)

        self.restoreState()


def build_pdf():
    # A4 dimensions: 595.27 x 841.89 pt. Margins: 45 pt -> Printable width: 505.27 pt.
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Color Tokens
    PRIMARY = colors.HexColor("#0f2438")     # Deep Navy
    SECONDARY = colors.HexColor("#0284c7")   # Electric Ocean Blue
    ACCENT = colors.HexColor("#0d9488")      # Teal / Cyan
    TEXT_DARK = colors.HexColor("#1e293b")   # Slate Dark
    TEXT_MUTED = colors.HexColor("#64748b")  # Slate Muted
    BG_LIGHT = colors.HexColor("#f8fafc")    # Light slate bg
    BORDER_CLR = colors.HexColor("#cbd5e1")  # Border gray

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=28,
        textColor=PRIMARY
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=SECONDARY
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=0,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=TEXT_DARK,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=2.5
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0369a1")
    )

    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=TEXT_MUTED,
        alignment=1,
        spaceBefore=3,
        spaceAfter=5
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE & COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<font size=9 color='#64748b'><b>OPERATING SYSTEMS (UNIT VI: STORAGE MANAGEMENT) • ACADEMIC EVALUATION</b></font>", body_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=3.5, color=SECONDARY, spaceAfter=18, spaceBefore=0))

    story.append(Paragraph("Disk Scheduling Algorithms:<br/>FCFS, SSTF and SCAN Performance Analysis", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("A Comprehensive Theoretical, Mathematical, and Graphical Simulation Study with Step-by-Step Trajectory Verification", subtitle_style))
    story.append(Spacer(1, 20))

    meta_data = [
        [Paragraph("<b>Assigned Student:</b>", body_style), Paragraph("<b>Akshat Joshi</b>", body_style)],
        [Paragraph("<b>Course Curriculum:</b>", body_style), Paragraph("Operating Systems (Unit VI: Storage Management)", body_style)],
        [Paragraph("<b>Project Category:</b>", body_style), Paragraph("Special Direct Reading Project (25 Points Allocation)", body_style)],
        [Paragraph("<b>GitHub Repository:</b>", body_style), Paragraph("<font color='#0284c7'><b>https://github.com/MRIDULsinghRAWAT/Disk-scheduling-</b></font>", body_style)],
        [Paragraph("<b>Primary Algorithms:</b>", body_style), Paragraph("FCFS (First-Come, First-Served), SSTF (Shortest Seek Time First), SCAN (Elevator)", body_style)],
        [Paragraph("<b>Extended Algorithms:</b>", body_style), Paragraph("C-SCAN (Circular SCAN), LOOK, C-LOOK", body_style)],
        [Paragraph("<b>Theoretical Benchmark:</b>", body_style), Paragraph("Silberschatz et al. (10th Ed.) Benchmark: [98, 183, 37, 122, 14, 124, 65, 67] at Head 53", body_style)],
        [Paragraph("<b>Core Deliverables:</b>", body_style), Paragraph("Interactive GUI, Mechanical Platter Simulation, Trajectory Graphs, Calculations, Comparison Matrix", body_style)],
        [Paragraph("<b>Academic Session:</b>", body_style), Paragraph("2026–2027 Academic Year", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[140, 365])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 16))

    # Executive Abstract Box
    abstract_html = (
        "<b>Project Abstract:</b> Secondary storage devices, specifically electromechanical magnetic hard disks, represent "
        "the primary I/O bottleneck in modern computer architectures. Because physical head displacement (seek latency) "
        "dominates disk access time by several orders of magnitude over electronic memory transfers, the disk scheduling "
        "subsystem within the Operating System kernel plays a critical role in system throughput, latency, and fairness.<br/><br/>"
        "This project presents a high-fidelity interactive simulation software and comparative performance analysis "
        "implementing the required syllabus algorithms (FCFS, SSTF, SCAN) alongside extended variants (C-SCAN, LOOK, C-LOOK). "
        "Every algorithm is mathematically modeled, visually simulated with real-time platter and actuator kinematics, "
        "evaluated against standard textbook benchmark problems, and benchmarked across Total Head Movement (THM), "
        "Average Seek Length (ASL), seek latency, starvation susceptibility, and mechanical arm stress."
    )
    t_abstract = Table([[Paragraph(abstract_html, body_style)]], colWidths=[505])
    t_abstract.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0f9ff")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#0284c7")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_abstract)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: OVERVIEW & HARDWARE MECHANICS
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Expected Deliverables", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "Operating systems must arbitrate access to secondary storage when multiple processes generate simultaneous read and write "
        "requests. In accordance with the official Operating Systems project guidelines, this work delivers:",
        body_style
    ))
    story.append(Paragraph("• <b>Rigorous Theoretical Exposition:</b> Mathematical formulation of disk latency parameters and scheduling heuristics.", bullet_style))
    story.append(Paragraph("• <b>High-Fidelity Graphical Simulation (GUI):</b> Live interactive magnetic platter animation with concentric cylinder tracks, pivoting actuator arm, linear cylinder ruler (0 to Max), and step-by-step playback controls.", bullet_style))
    story.append(Paragraph("• <b>Step-by-Step Calculation Engine:</b> Complete mathematical breakdowns showing absolute seek distances (|C<sub>i</sub> - C<sub>i-1</sub>|), cumulative Total Head Movement (THM), and operational rationale.", bullet_style))
    story.append(Paragraph("• <b>Multi-Dimensional Graphical Visualizations:</b> Silberschatz 2D Trajectory line plots (Cylinder vs Step Order) and comparative bar charts.", bullet_style))
    story.append(Paragraph("• <b>Comparative Performance Matrix:</b> Comprehensive evaluation table comparing THM, Average Seek Length (ASL), seek time, efficiency vs baseline FCFS, starvation risk, and algorithmic time complexity.", bullet_style))
    story.append(Paragraph("• <b>Source Code Repository:</b> Hosted publicly on GitHub at <font color='#0284c7'><b>https://github.com/MRIDULsinghRAWAT/Disk-scheduling-</b></font>.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Hard Disk Physical Mechanics & Mathematical Formulations", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "A Hard Disk Drive (HDD) consists of spinning magnetic platters mounted on a common spindle rotating at constant speed "
        "(e.g., 5400, 7200, or 15000 RPM). Platters are divided into concentric circular <b>tracks</b>, and tracks aligned vertically "
        "across all platter surfaces form a <b>cylinder</b>. A mechanical actuator arm moves the read/write head assembly radially across cylinders.",
        body_style
    ))

    story.append(Paragraph("<b>Components of Disk Access Time:</b>", h2_style))
    story.append(Paragraph(
        "The total latency incurred when servicing a disk read/write operation is expressed as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>T<sub>access</sub> = T<sub>seek</sub> + T<sub>rotational</sub> + T<sub>transfer</sub> + T<sub>controller</sub></b>",
        body_style
    ))
    story.append(Paragraph("• <b>Seek Time (T<sub>seek</sub>):</b> The time required for the actuator arm to mechanically position the head over the target cylinder track. <i>This is the primary mechanical delay optimized by scheduling algorithms.</i>", bullet_style))
    story.append(Paragraph("• <b>Rotational Latency (T<sub>rotational</sub>):</b> The delay waiting for the desired sector to rotate under the head (average = 1 / (2 &times; RPM)).", bullet_style))
    story.append(Paragraph("• <b>Transfer Time (T<sub>transfer</sub>):</b> The time needed to magnetically stream the data bits between the platter surface and disk controller buffer.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Mathematical Evaluation Metrics:</b>", h2_style))

    metrics_table_data = [
        [Paragraph("<b>Evaluation Metric</b>", body_style), Paragraph("<b>Mathematical Formula</b>", body_style), Paragraph("<b>Operational Significance</b>", body_style)],
        [
            Paragraph("<b>Total Head Movement (THM)</b>", body_style),
            Paragraph("<b>THM = &Sigma;<sub>i=1..N</sub> |C<sub>i</sub> - C<sub>i-1</sub>|</b>", body_style),
            Paragraph("Total cylinder tracks traversed by the read/write head from initial head C<sub>0</sub> across all N requests.", body_style)
        ],
        [
            Paragraph("<b>Average Seek Length (ASL)</b>", body_style),
            Paragraph("<b>ASL = THM / N</b>", body_style),
            Paragraph("Mean track displacement per I/O operation. Directly indicates expected mechanical travel per request.", body_style)
        ],
        [
            Paragraph("<b>Estimated Seek Time (T<sub>seek</sub>)</b>", body_style),
            Paragraph("<b>T<sub>seek</sub> = THM &times; t<sub>track</sub></b>", body_style),
            Paragraph("Total mechanical seek latency in ms, using track-to-track latency factor t<sub>track</sub> (default: 5.0 ms/track).", body_style)
        ],
        [
            Paragraph("<b>Percentage Efficiency Gain (&eta;)</b>", body_style),
            Paragraph("<b>&eta; = ((THM<sub>FCFS</sub> - THM<sub>alg</sub>) / THM<sub>FCFS</sub>) &times; 100%</b>", body_style),
            Paragraph("Quantitative reduction in head travel achieved relative to the unoptimized baseline FCFS.", body_style)
        ]
    ]
    t_metrics = Table(metrics_table_data, colWidths=[130, 160, 215])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CLR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('TOPPADDING', (0,1), (-1,-1), 4),
        ('BOTTOMPADDING', (0,1), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_metrics)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: THEORETICAL ANALYSIS OF ALGORITHMS
    # =========================================================================
    story.append(Paragraph("3. Theoretical Analysis of Disk Scheduling Algorithms", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("3.1 First-Come, First-Served (FCFS)", h2_style))
    story.append(Paragraph(
        "<b>Mechanism:</b> Requests are serviced strictly in the chronological order of their arrival into the I/O queue. "
        "The controller makes no attempt to reorder requests or optimize head trajectory.<br/>"
        "• <i>Strengths:</i> Complete fairness across all processes; mathematically immune to starvation; O(1) queue insertion.<br/>"
        "• <i>Weaknesses:</i> Prone to severe wild swings across the platters, resulting in extremely high Total Head Movement and high mechanical stress.",
        body_style
    ))

    story.append(Paragraph("3.2 Shortest Seek Time First (SSTF)", h2_style))
    story.append(Paragraph(
        "<b>Mechanism:</b> A greedy heuristic that selects the pending request closest to the current head position: "
        "<i>Next = argmin<sub>r &isin; Q</sub> |C<sub>current</sub> - r|</i>. Direction is preserved during ties.<br/>"
        "• <i>Strengths:</i> Dramatically reduces Total Head Movement compared to FCFS, maximizing immediate I/O throughput.<br/>"
        "• <i>Weaknesses:</i> <b>Starvation:</b> Continuous arrivals of localized requests near the head will indefinitely postpone requests residing on distant tracks.",
        body_style
    ))

    story.append(Paragraph("3.3 SCAN (The Elevator Algorithm)", h2_style))
    story.append(Paragraph(
        "<b>Mechanism:</b> The head begins at its current position and moves in a specified direction (e.g., towards higher cylinders), servicing "
        "all requests encountered along its path. Upon reaching the physical disk boundary (track 199 or 0), the arm reverses direction and sweeps back.<br/>"
        "• <i>Strengths:</i> Eliminates starvation entirely; delivers bounded worst-case waiting times; smooth monotonic arm motion.<br/>"
        "• <i>Weaknesses:</i> Redundant travel to the physical boundary (track 199) even when no requests exist there; slight unfairness for requests just behind the reversing arm.",
        body_style
    ))

    story.append(Paragraph("3.4 Extended Algorithms: C-SCAN, LOOK, and C-LOOK", h2_style))
    story.append(Paragraph(
        "• <b>C-SCAN (Circular SCAN):</b> Provides uniform waiting times by servicing requests in one direction only. Upon reaching the boundary, "
        "the arm immediately returns to the starting boundary <i>without servicing requests on the return trip</i>.<br/>"
        "• <b>LOOK:</b> An optimization over SCAN where the arm reverses immediately upon servicing the final pending request in the current direction, "
        "completely avoiding unnecessary travel to the physical disk limits.<br/>"
        "• <b>C-LOOK:</b> Combines C-SCAN's circular fairness with LOOK's boundary optimization, snapping back from the highest requested cylinder directly to the lowest requested cylinder.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Summary of Algorithmic Trade-Offs:</b>", h2_style))

    alg_summary_data = [
        [Paragraph("<b>Algorithm</b>", body_style), Paragraph("<b>Heuristic Basis</b>", body_style), Paragraph("<b>Boundary Behavior</b>", body_style), Paragraph("<b>Starvation Risk</b>", body_style), Paragraph("<b>Complexity</b>", body_style)],
        [Paragraph("<b>FCFS</b>", body_style), Paragraph("FIFO arrival order", body_style), Paragraph("No boundary awareness", body_style), Paragraph("<font color='#16a34a'><b>Zero (Fair)</b></font>", body_style), Paragraph("O(N)", body_style)],
        [Paragraph("<b>SSTF</b>", body_style), Paragraph("Min |C<sub>curr</sub> - r| greedy", body_style), Paragraph("Opportunistic seek", body_style), Paragraph("<font color='#dc2626'><b>High</b></font>", body_style), Paragraph("O(N<sup>2</sup>)", body_style)],
        [Paragraph("<b>SCAN</b>", body_style), Paragraph("Bidirectional sweep", body_style), Paragraph("Travels to physical limit (0 / Max)", body_style), Paragraph("<font color='#16a34a'><b>None</b></font>", body_style), Paragraph("O(N log N)", body_style)],
        [Paragraph("<b>C-SCAN</b>", body_style), Paragraph("Unidirectional circular sweep", body_style), Paragraph("Resets from limit to limit", body_style), Paragraph("<font color='#16a34a'><b>None (Uniform)</b></font>", body_style), Paragraph("O(N log N)", body_style)],
        [Paragraph("<b>LOOK</b>", body_style), Paragraph("Bidirectional bounded sweep", body_style), Paragraph("Reverses at extreme request", body_style), Paragraph("<font color='#16a34a'><b>None</b></font>", body_style), Paragraph("O(N log N)", body_style)],
        [Paragraph("<b>C-LOOK</b>", body_style), Paragraph("Unidirectional bounded sweep", body_style), Paragraph("Resets to lowest request", body_style), Paragraph("<font color='#16a34a'><b>None (Uniform)</b></font>", body_style), Paragraph("O(N log N)", body_style)],
    ]
    t_alg_summary = Table(alg_summary_data, colWidths=[65, 140, 130, 95, 75])
    t_alg_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 3.5),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CLR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('TOPPADDING', (0,1), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,1), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_alg_summary)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: BENCHMARK DATASET & STEP CALCULATIONS
    # =========================================================================
    story.append(Paragraph("4. Benchmark Dataset & Mathematical Step Calculations", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "<b>Silberschatz et al. (10th Edition) Standard Problem Parameters:</b><br/>"
        "• Total Cylinders: <b>0 to 199</b> (200 tracks) | Initial Head Position: <b>53</b> | Arm Direction: <b>Right (towards 199)</b><br/>"
        "• I/O Request Queue Sequence: <b>[98, 183, 37, 122, 14, 124, 65, 67]</b>",
        body_style
    ))

    story.append(Paragraph("4.1 FCFS Step Calculations (THM = 640, ASL = 80.00)", h2_style))
    fcfs_steps_data = [
        ["Step #", "From", "To", "Formula", "Seek (|Δ|)", "Cum. THM", "Operational Rationale"],
        ["1", "53", "98", "|98 - 53|", "45", "45", "1st request in FIFO queue"],
        ["2", "98", "183", "|183 - 98|", "85", "130", "Large outward swing to track 183"],
        ["3", "183", "37", "|37 - 183|", "146", "276", "Massive inward reversal across platters"],
        ["4", "37", "122", "|122 - 37|", "85", "361", "Outward swing back towards outer tracks"],
        ["5", "122", "14", "|14 - 122|", "108", "469", "Severe inward swing to track 14"],
        ["6", "14", "124", "|124 - 14|", "110", "579", "Severe outward reversal to track 124"],
        ["7", "124", "65", "|65 - 124|", "59", "638", "Inward seek towards middle tracks"],
        ["8", "65", "67", "|67 - 65|", "2", "640", "Final nearby sequential request"]
    ]
    t_fcfs = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body_style) for c in row] for r, row in enumerate(fcfs_steps_data)], colWidths=[40, 35, 35, 75, 55, 65, 200])
    t_fcfs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CLR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_fcfs)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.2 SSTF Step Calculations (THM = 236, ASL = 29.50, 63.1% Gain)", h2_style))
    sstf_steps_data = [
        ["Step #", "From", "To", "Formula", "Seek (|Δ|)", "Cum. THM", "Operational Rationale"],
        ["1", "53", "65", "|65 - 53|", "12", "12", "Nearest cylinder to initial head 53"],
        ["2", "65", "67", "|67 - 65|", "2", "14", "Nearest cylinder to 65 (|67-65|=2 vs |37-65|=28)"],
        ["3", "67", "37", "|37 - 67|", "30", "44", "Nearest remaining cylinder (|37-67|=30 vs |98-67|=31)"],
        ["4", "37", "14", "|14 - 37|", "23", "67", "Nearest remaining cylinder to 37"],
        ["5", "14", "98", "|98 - 14|", "84", "151", "Left side exhausted; seek to nearest right"],
        ["6", "98", "122", "|122 - 98|", "24", "175", "Nearest cylinder to 98"],
        ["7", "122", "124", "|124 - 122|", "2", "177", "Adjacent cylinder seek"],
        ["8", "124", "183", "|183 - 124|", "59", "236", "Final remaining outermost cylinder"]
    ]
    t_sstf = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body_style) for c in row] for r, row in enumerate(sstf_steps_data)], colWidths=[40, 35, 35, 75, 55, 65, 200])
    t_sstf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f0fdf4")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CLR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sstf)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.3 SCAN Step Calculations (THM = 331, ASL = 41.38, 48.3% Gain)", h2_style))
    scan_steps_data = [
        ["Step #", "From", "To", "Formula", "Seek (|Δ|)", "Cum. THM", "Operational Rationale"],
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
    t_scan = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body_style) for c in row] for r, row in enumerate(scan_steps_data)], colWidths=[40, 35, 35, 75, 55, 65, 200])
    t_scan.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f0fdfa")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CLR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_scan)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: SIMULATOR GUI & HARDWARE SCREENSHOTS
    # =========================================================================
    story.append(Paragraph("5. Interactive Simulator GUI & Physical Disk Simulation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "To bring disk scheduling concepts alive, a high-fidelity simulator was built using modern web standards. "
        "The application provides real-time animated physical disk mechanics, dynamic linear ruler tracking, and custom sequence builders.",
        body_style
    ))

    config_img = os.path.join(SCREENSHOTS_DIR, "02_configuration_panel.png")
    if os.path.exists(config_img):
        story.append(Paragraph("<b>Figure 1: Disk Parameters & Request Sequence Configuration Panel</b>", caption_style))
        story.append(Image(config_img, width=505, height=82))
        story.append(Spacer(1, 4))

    platter_img = os.path.join(SCREENSHOTS_DIR, "03_hardware_visualizer.png")
    if os.path.exists(platter_img):
        story.append(Paragraph("<b>Figure 2: Physical Disk Platter Assembly & Linear Cylinder Track Ruler</b>", caption_style))
        story.append(Image(platter_img, width=505, height=160))
        story.append(Spacer(1, 4))

    active_img = os.path.join(SCREENSHOTS_DIR, "04_active_seeking_state.png")
    if os.path.exists(active_img):
        story.append(Paragraph("<b>Figure 3: Live Playback in Progress (Active Head Seeking & Serviced Pins in Green)</b>", caption_style))
        story.append(Image(active_img, width=505, height=160))
        story.append(Paragraph(
            "<i>Note:</i> In Figure 3, the playback engine has completed 4 steps. The read/write head is actively positioned at track 37. "
            "Pins for serviced cylinders turn bright green, while pending requests remain amber.",
            caption_style
        ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: VISUAL TRAJECTORY PLOTS & BAR CHARTS
    # =========================================================================
    story.append(Paragraph("6. Trajectory Plots & Comparative Visual Analytics", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "The classical Silberschatz trajectory graph plots <b>Disk Cylinder on the horizontal axis (0 to 199)</b> against "
        "<b>Servicing Order (Step 0 to N) on the vertical axis</b>. The slope and shape of the path illustrate mechanical efficiency.",
        body_style
    ))

    fcfs_chart = os.path.join(SCREENSHOTS_DIR, "05_trajectory_fcfs.png")
    sstf_chart = os.path.join(SCREENSHOTS_DIR, "06_trajectory_sstf.png")
    scan_chart = os.path.join(SCREENSHOTS_DIR, "07_trajectory_scan.png")
    overlay_chart = os.path.join(SCREENSHOTS_DIR, "08_trajectory_overlay_all.png")

    if os.path.exists(fcfs_chart) and os.path.exists(sstf_chart):
        t_row1 = Table([
            [Image(fcfs_chart, width=248, height=140), Image(sstf_chart, width=248, height=140)],
            [Paragraph("<b>Figure 4: FCFS Trajectory (THM: 640)</b><br/>High oscillation and erratic swings across platters.", caption_style),
             Paragraph("<b>Figure 5: SSTF Trajectory (THM: 236)</b><br/>Localized greedy sweeps resulting in minimal head travel.", caption_style)]
        ], colWidths=[252, 252])
        t_row1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('TOPPADDING', (0,0), (-1,-1), 1), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
        story.append(t_row1)
        story.append(Spacer(1, 4))

    if os.path.exists(scan_chart) and os.path.exists(overlay_chart):
        t_row2 = Table([
            [Image(scan_chart, width=248, height=140), Image(overlay_chart, width=248, height=140)],
            [Paragraph("<b>Figure 6: SCAN Trajectory (THM: 331)</b><br/>Monotonic sweep to boundary 199 then reverse.", caption_style),
             Paragraph("<b>Figure 7: Multi-Algorithm Trajectory Overlay</b><br/>Simultaneous comparison of all 6 arm pathways.", caption_style)]
        ], colWidths=[252, 252])
        t_row2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('TOPPADDING', (0,0), (-1,-1), 1), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
        story.append(t_row2)
        story.append(Spacer(1, 4))

    bars_chart = os.path.join(SCREENSHOTS_DIR, "09_comparison_barcharts.png")
    if os.path.exists(bars_chart):
        story.append(Paragraph("<b>Figure 8: Comparative Metrics Bar Charts (Total Head Movement & Average Seek Length)</b>", caption_style))
        story.append(Image(bars_chart, width=460, height=140))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: IN-APP CALCULATION TABLE & RESULTS MATRIX
    # =========================================================================
    story.append(Paragraph("7. In-App Calculation Engine & Results Matrix Screenshots", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    calc_table_img = os.path.join(SCREENSHOTS_DIR, "10_step_calculation_table.png")
    if os.path.exists(calc_table_img):
        story.append(Paragraph("<b>Figure 9: In-App Live Mathematical Step-by-Step Calculation Table</b>", caption_style))
        story.append(Image(calc_table_img, width=505, height=215))
        story.append(Spacer(1, 6))

    matrix_img = os.path.join(SCREENSHOTS_DIR, "11_comparative_matrix.png")
    if os.path.exists(matrix_img):
        story.append(Paragraph("<b>Figure 10: In-App Comparative Results Matrix & Workload Behavioral Analysis</b>", caption_style))
        story.append(Image(matrix_img, width=505, height=240))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: COMPARATIVE EVALUATION, MODERN OS CONTEXT & REFERENCES
    # =========================================================================
    story.append(Paragraph("8. Comparative Analysis & Modern OS Engineering", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    # Comprehensive Summary Table
    comp_matrix_data = [
        ["Algorithm", "Total Head Movement", "Avg Seek Length", "Est. Seek Time", "Efficiency vs FCFS", "Starvation Risk", "Arm Wear Index"],
        ["FCFS", "640 cylinders", "80.00 tracks/req", "3,200.0 ms", "Baseline (0.0%)", "Zero (Fair)", "Severe (High Stress)"],
        ["SSTF", "236 cylinders", "29.50 tracks/req", "1,180.0 ms", "+63.1% Gain", "High Risk", "Moderate"],
        ["SCAN", "331 cylinders", "41.38 tracks/req", "1,655.0 ms", "+48.3% Gain", "Zero (Fair)", "Low (Smooth Sweep)"],
        ["C-SCAN", "382 cylinders", "47.75 tracks/req", "1,910.0 ms", "+40.3% Gain", "Zero (Fair)", "Low (Circular Sweep)"],
        ["LOOK", "299 cylinders", "37.38 tracks/req", "1,495.0 ms", "+53.3% Gain", "Zero (Fair)", "Very Low (Optimal Range)"],
        ["C-LOOK", "322 cylinders", "40.25 tracks/req", "1,610.0 ms", "+49.7% Gain", "Zero (Fair)", "Very Low (Optimal Circular)"]
    ]
    t_comp_matrix = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body_style) for c in row] for r, row in enumerate(comp_matrix_data)], colWidths=[65, 80, 75, 75, 80, 65, 65])
    t_comp_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [BG_LIGHT, colors.white]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CLR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_comp_matrix)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Engineering Trade-Offs:</b>", h2_style))
    story.append(Paragraph(
        "1. <b>Throughput vs Fairness:</b> SSTF provides maximal raw throughput (236 cylinders), but its starvation vulnerability makes it "
        "unsuitable for mission-critical enterprise systems without aging mechanisms. SCAN and LOOK provide bounded response times.<br/>"
        "2. <b>Mechanical Stress:</b> FCFS creates abrupt reversals that accelerate mechanical wear on spindle bearings and voice coils. "
        "SCAN's monotonic sweeping motions significantly extend hardware lifespan.<br/>"
        "3. <b>LOOK Superiority over SCAN:</b> LOOK eliminates SCAN's redundant travel to track 199, saving 32 tracks (nearly 10% gain).",
        body_style
    ))

    story.append(Paragraph("<b>Modern Operating System I/O Schedulers:</b>", h2_style))
    story.append(Paragraph(
        "• <b>Linux Deadline Scheduler:</b> Implements a SCAN/LOOK elevator sweep combined with FIFO expiration deadlines (e.g., 500 ms for reads, 5 s for writes) to strictly prevent starvation.<br/>"
        "• <b>CFQ &amp; BFQ:</b> Allocate fair bandwidth budgets and time slices across competing processes.<br/>"
        "• <b>NVMe &amp; Solid-State Storage (SSDs):</b> Because flash memory has no moving read/write heads, seek latency is zero. "
        "Modern SSD schedulers (<i>None</i>, <i>Kyber</i>) focus on multi-queue hardware submission queues rather than physical track reordering.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=6, spaceBefore=2))
    story.append(Paragraph(
        "This project successfully designed, implemented, and empirically validated a full interactive disk scheduling simulation system. "
        "The quantitative benchmark confirmed that SSTF (236) and LOOK (299) achieve dramatic seek reductions over unoptimized FCFS (640), "
        "while SCAN variants deliver the most reliable balance between throughput, starvation avoidance, and hardware longevity.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("10. Authentic Academic References", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=6, spaceBefore=2))

    refs = [
        "<b>[1] Silberschatz, A., Galvin, P. B., & Gagne, G. (2018).</b> <i>Operating System Concepts</i> (10th Edition). Chapter 11: Mass-Storage Structure. John Wiley & Sons. ISBN: 978-1-119-32091-3.",
        "<b>[2] Tanenbaum, A. S., & Bos, H. (2015).</b> <i>Modern Operating Systems</i> (4th Edition). Chapter 5: Input/Output. Pearson. ISBN: 978-0-13-359162-0.",
        "<b>[3] Stallings, W. (2018).</b> <i>Operating Systems: Internals and Design Principles</i> (9th Edition). Chapter 11: I/O Management and Disk Scheduling. Pearson. ISBN: 978-0-13-467095-9.",
        "<b>[4] Bovet, D. P., & Cesati, M. (2005).</b> <i>Understanding the Linux Kernel</i> (3rd Edition). Chapter 14: The Block Device Driver Architecture & I/O Schedulers. O'Reilly Media.",
        "<b>[5] Love, R. (2010).</b> <i>Linux Kernel Development</i> (3rd Edition). Chapter 14: The Block I/O Layer & Elevator Architecture. Addison-Wesley Professional."
    ]
    for r in refs:
        story.append(Paragraph(r, bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
