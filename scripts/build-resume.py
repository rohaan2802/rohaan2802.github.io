"""Generate the one-page A4 resume (original layout). Run: python scripts/build-resume.py"""

from io import BytesIO
from pathlib import Path

from fpdf import FPDF
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resume" / "Mohammad_Rohaan_Resume.pdf"
PHOTO = ROOT / "images" / "portfolio_img.png"
FONT_DIR = Path(r"C:\Windows\Fonts")
CALIBRI = FONT_DIR / "calibri.ttf"
CALIBRI_B = FONT_DIR / "calibrib.ttf"

INK = (0, 0, 0)
MUTED = (40, 40, 40)


def _font_pair():
    if CALIBRI.exists() and CALIBRI_B.exists():
        return "Body", str(CALIBRI), str(CALIBRI_B)
    return "Helvetica", None, None


def rounded_photo(path: Path, px: int = 280, radius: int = 28) -> BytesIO:
    im = Image.open(path).convert("RGBA")
    side = min(im.size)
    left = (im.width - side) // 2
    top = (im.height - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize((px, px), Image.Resampling.LANCZOS)
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, px - 1, px - 1), radius=radius, fill=255)
    out = Image.new("RGBA", (px, px), (255, 255, 255, 0))
    out.paste(im, mask=mask)
    buf = BytesIO()
    out.save(buf, format="PNG")
    buf.seek(0)
    return buf


def line_icon(kind: str, size: int = 64) -> BytesIO:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = max(3, size // 12)
    m = size * 0.16
    if kind == "phone":
        d.rounded_rectangle((size * 0.34, m, size * 0.66, size - m), radius=size * 0.1, outline=INK, width=w)
        d.rectangle((size * 0.44, size * 0.22, size * 0.56, size * 0.28), fill=INK)
    elif kind == "email":
        d.rectangle((m, size * 0.28, size - m, size * 0.74), outline=INK, width=w)
        d.line([(m, size * 0.28), (size / 2, size * 0.54), (size - m, size * 0.28)], fill=INK, width=w)
    elif kind == "web":
        d.ellipse((m, m, size - m, size - m), outline=INK, width=w)
        d.ellipse((size * 0.34, m, size * 0.66, size - m), outline=INK, width=max(2, w - 1))
        d.line([(m, size / 2), (size - m, size / 2)], fill=INK, width=w)
    elif kind == "github":
        d.ellipse((m, m * 1.05, size - m, size - m * 0.7), outline=INK, width=w)
        d.arc((size * 0.28, size * 0.55, size * 0.72, size * 0.98), 200, 340, fill=INK, width=w)
    elif kind == "linkedin":
        d.rounded_rectangle((m, m, size - m, size - m), radius=size * 0.12, outline=INK, width=w)
        d.rectangle((size * 0.30, size * 0.42, size * 0.40, size * 0.72), fill=INK)
        d.ellipse((size * 0.30, size * 0.28, size * 0.40, size * 0.38), fill=INK)
        d.polygon(
            [
                (size * 0.48, size * 0.72),
                (size * 0.48, size * 0.42),
                (size * 0.58, size * 0.42),
                (size * 0.70, size * 0.58),
                (size * 0.70, size * 0.72),
                (size * 0.60, size * 0.72),
                (size * 0.60, size * 0.62),
                (size * 0.58, size * 0.52),
                (size * 0.48, size * 0.52),
            ],
            fill=INK,
        )
    buf = BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    return buf


class Resume(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=False, margin=10)
        self.set_margins(14, 11, 14)
        family, regular, bold = _font_pair()
        self.family = family
        if regular:
            self.add_font("Body", "", regular)
            self.add_font("Body", "B", bold)

    def section(self, title):
        self.ln(1.4)
        self.set_font(self.family, "B", 11)
        self.set_text_color(*INK)
        self.cell(0, 5.2, title.upper(), new_x="LMARGIN", new_y="NEXT")
        y = self.get_y()
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.35)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(2.0)

    def rich_para(self, parts, size=10, leading=4.35):
        """parts: list of (text, bold)."""
        self.set_font(self.family, "", size)
        usable = self.w - self.l_margin - self.r_margin
        x0 = self.l_margin
        x = x0
        y = self.get_y()
        line_h = leading
        for text, bold in parts:
            self.set_font(self.family, "B" if bold else "", size)
            words = text.split(" ")
            for i, word in enumerate(words):
                chunk = word if i == len(words) - 1 else word + " "
                ww = self.get_string_width(chunk)
                if x + ww > x0 + usable and x > x0:
                    x = x0
                    y += line_h
                self.set_xy(x, y)
                self.cell(ww, line_h, chunk)
                x += ww
        self.set_xy(x0, y + line_h + 0.4)

    def skill_line(self, label, rest, size=9.6, leading=4.15):
        self.set_x(self.l_margin)
        label_txt = f"{label}: "
        self.set_font(self.family, "B", size)
        self.set_text_color(*INK)
        lw = self.get_string_width(label_txt)
        y = self.get_y()
        self.cell(lw, leading, label_txt)
        self.set_xy(self.l_margin + lw, y)
        self.set_font(self.family, "", size)
        self.multi_cell(self.w - self.r_margin - self.l_margin - lw, leading, rest)

    def project(self, title, stack, bullets, links=None):
        self.set_font(self.family, "B", 10)
        self.set_text_color(*INK)
        self.write(4.2, title)
        self.set_font(self.family, "", 10)
        self.write(4.2, f"  ({stack})")
        if links:
            self.set_font(self.family, "", 9)
            for label, url in links:
                self.write(4.2, "  ·  ")
                self.set_text_color(0, 0, 0)
                self.set_font(self.family, "B", 9)
                self.write(4.2, label, link=url)
                self.set_font(self.family, "", 9)
        self.ln(4.4)
        self.set_text_color(*INK)
        for b in bullets:
            self.set_font(self.family, "", 9.6)
            indent = 4.2
            x = self.l_margin
            y = self.get_y()
            self.set_xy(x, y)
            self.cell(indent, 4.05, "•")
            self.set_xy(x + indent, y)
            self.multi_cell(self.w - self.r_margin - x - indent, 4.05, b)
        self.ln(0.7)


def _contact_cell(pdf, icon_buf, text, url, x, y, w):
    pdf.image(icon_buf, x=x, y=y + 0.35, w=3.6, h=3.6)
    pdf.set_xy(x + 4.6, y)
    pdf.set_font(pdf.family, "", 9.2)
    pdf.set_text_color(*INK)
    pdf.cell(w - 4.6, 4.3, text, link=url)


def build():
    pdf = Resume()
    pdf.add_page()

    photo_w = 32.5
    photo_x = pdf.l_margin
    photo_y = 11
    pdf.image(rounded_photo(PHOTO), x=photo_x, y=photo_y, w=photo_w, h=photo_w)

    text_x = photo_x + photo_w + 5.5
    pdf.set_xy(text_x, photo_y + 0.2)
    pdf.set_font(pdf.family, "B", 18.5)
    pdf.set_text_color(*INK)
    pdf.cell(0, 7.2, "MOHAMMAD ROHAAN", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(text_x)
    pdf.set_font(pdf.family, "", 11)
    pdf.cell(0, 5.0, "BSCS Candidate  ·  FAST NUCES, Islamabad", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(text_x)
    pdf.set_font(pdf.family, "B", 10.5)
    pdf.cell(0, 5.0, "Software Engineering  ·  AI/ML  ·  Data Science", new_x="LMARGIN", new_y="NEXT")

    col_w = (pdf.w - text_x - pdf.r_margin) / 2
    row1 = photo_y + 18.6
    _contact_cell(pdf, line_icon("phone"), "+92 311 0433555", "tel:+923110433555", text_x, row1, col_w)
    _contact_cell(
        pdf,
        line_icon("email"),
        "m.rohaanarshad@gmail.com",
        "mailto:m.rohaanarshad@gmail.com",
        text_x + col_w,
        row1,
        col_w,
    )
    row2 = row1 + 5.0
    _contact_cell(
        pdf,
        line_icon("web"),
        "https://rohaan2802.github.io",
        "https://rohaan2802.github.io/",
        text_x,
        row2,
        col_w,
    )
    _contact_cell(
        pdf,
        line_icon("github"),
        "https://github.com/rohaan2802",
        "https://github.com/rohaan2802",
        text_x + col_w,
        row2,
        col_w,
    )
    row3 = row2 + 5.0
    _contact_cell(
        pdf,
        line_icon("linkedin"),
        "linkedin.com/in/m-rohaan-944a82320",
        "https://www.linkedin.com/in/m-rohaan-944a82320/",
        text_x,
        row3,
        col_w * 2,
    )

    pdf.set_y(max(photo_y + photo_w, row3 + 6.2) + 1.2)

    pdf.section("Objective")
    pdf.rich_para(
        [
            ("Final-year BSCS student at ", False),
            ("FAST NUCES, Islamabad", True),
            (" (June 2027). I build full-stack systems and applied AI: a ", False),
            ("live bilingual voice agent", True),
            (", NLP quiz generation, YOLOv8 detection, and a ", False),
            ("Spring Boot", True),
            (" library platform with Scrum delivery and documented test cases. Seeking software engineering or AI/ML internships and junior roles.", False),
        ]
    )

    pdf.section("Education")
    pdf.set_font(pdf.family, "B", 10.5)
    y = pdf.get_y()
    pdf.cell(0, 5.0, "FAST NUCES — Islamabad, Pakistan")
    pdf.set_xy(pdf.l_margin, y)
    pdf.set_font(pdf.family, "", 10)
    pdf.cell(0, 5.0, "Expected June 2027", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(pdf.family, "", 10)
    y = pdf.get_y()
    pdf.cell(0, 4.6, "Bachelor of Science in Computer Science (BSCS)")
    pdf.set_xy(pdf.l_margin, y)
    pdf.set_font(pdf.family, "I" if pdf.family == "Helvetica" else "", 10)
    if pdf.family != "Helvetica":
        pdf.set_font(pdf.family, "", 10)
    pdf.cell(0, 4.6, "Final-year BSCS candidate", align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.section("Technical Skills")
    pdf.skill_line("Languages", "Python, Java, C, C++, JavaScript, SQL, PHP, C#")
    pdf.skill_line(
        "AI / ML / Data",
        "scikit-learn, pandas, NLP (TF-IDF, BLEU/ROUGE/METEOR), YOLOv8, Streamlit, VAPI, Groq, Deepgram, model evaluation",
    )
    pdf.skill_line(
        "Software Eng",
        "Java 17, Spring Boot 3.5, Spring Security, Spring MVC, Thymeleaf, JPA/Hibernate, MySQL 8, Next.js, REST APIs, Scrum, Git, Maven",
    )
    pdf.skill_line(
        "Web & Databases",
        "HTML, CSS, PHP, SQL Server, T-SQL, ER/EER modeling, normalization",
    )
    pdf.skill_line(
        "Systems",
        "C++, OpenMP, multithreading, benchmarking, DSA, Linux",
    )
    pdf.skill_line(
        "Embedded / Robotics",
        "Arduino, ESP32, Raspberry Pi, ultrasonic sensors, MATLAB (robotics simulation)",
    )

    pdf.section("Relevant Coursework")
    pdf.set_font(pdf.family, "", 9.7)
    pdf.multi_cell(
        0,
        4.15,
        "Data Structures & Algorithms, Operating Systems, Computer Networks, Database Systems, Software Engineering, Probability & Statistics, Parallel & Distributed Computing, Numerical Computing / HPC, Design & Analysis of Algorithms, Machine Learning / Data Science, Computer Vision.",
    )

    pdf.section("Selected Projects")
    pdf.project(
        "AI Voice Cold-Calling Agent",
        "Next.js, VAPI, Groq, Deepgram",
        [
            "Live English/Urdu sales voice agent: web Call Agent, objection handling, language lock, recordings, transcripts, and paginated call history.",
            "Next.js app on Vercel; VAPI-orchestrated speech-to-text, Groq LLM, and TTS, with an outbound dialer for US +1 numbers.",
        ],
        links=[
            ("Live", "https://web-rouge-xi-23.vercel.app"),
            ("GitHub", "https://github.com/rohaan2802/Cold-Calling-Agent"),
        ],
    )
    pdf.project(
        "AI Quiz Generator",
        "Python, Streamlit, scikit-learn",
        [
            "RACE reading-comprehension quizzes: Linear SVM question/answer ranking plus Random Forest distractors and logistic-regression hints.",
            "Streamlit UI for passage load, hints, scoring, and analytics; hint generation METEOR 0.69 (BLEU/ROUGE also reported).",
        ],
        links=[("GitHub", "https://github.com/rohaan2802/AI_Quiz_Generator")],
    )
    pdf.project(
        "LibraryMS",
        "Java 17, Spring Boot, MySQL, Scrum",
        [
            "Role-based library system (Admin / Librarian / Student) with Spring Security: catalog, borrow/return, FIFO reservations, fines, and admin reports.",
            "Three Scrum sprints; 22/22 black-box and white-box test cases passed.",
        ],
        links=[("GitHub", "https://github.com/rohaan2802/LibraryMS")],
    )
    pdf.project(
        "Shuttlecock Detection",
        "YOLOv8, transfer learning",
        [
            "Fine-tuned YOLOv8 from COCO weights on 15,000 labeled images; evaluated with precision, recall, and mAP.",
            "Real-time webcam inference; robotics collection pipeline designed for Raspberry Pi + Arduino.",
        ],
        links=[("GitHub", "https://github.com/rohaan2802/ShuttleCock-Detection")],
    )
    pdf.project(
        "Hospital DB System",
        "SQL Server, PHP, ER/EER",
        [
            "Replaced manual hospital records with a normalized ER/EER schema, integrity constraints, seed data, and 12 operational SQL queries.",
            "PHP/JavaScript portals for patient intake, ward admin, consultant grading, and staff reports.",
        ],
        links=[("GitHub", "https://github.com/rohaan2802/HospitalMS")],
    )

    pdf.ln(0.6)
    pdf.set_font(pdf.family, "B", 10)
    pdf.set_text_color(*INK)
    pdf.write(4.2, "K-means Triangle Inequality")
    pdf.set_font(pdf.family, "", 10)
    pdf.write(4.2, "  (C++, OpenMP) — Elkan vs Lloyd; up to 2.2x vs naive at 128-D.  ")
    pdf.set_font(pdf.family, "B", 9)
    pdf.write(4.2, "GitHub", link="https://github.com/rohaan2802/KMeanTriangleInequality")
    pdf.ln(4.6)
    pdf.set_font(pdf.family, "B", 10)
    pdf.write(4.2, "Git Lite")
    pdf.set_font(pdf.family, "", 10)
    pdf.write(4.2, "  (C++) — Version-control subset: commit DAG, content hashing, diff, and merge.  ")
    pdf.set_font(pdf.family, "B", 9)
    pdf.write(4.2, "GitHub", link="https://github.com/rohaan2802/GitLite_DSA_Project")
    pdf.ln(5)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"Wrote {OUT} pages={pdf.pages_count} y={pdf.get_y():.1f} page_h={pdf.h:.1f}")
    if pdf.pages_count != 1:
        raise SystemExit("Resume must stay 1 page")
    if pdf.get_y() > 287:
        raise SystemExit("Content too close to bottom edge")


if __name__ == "__main__":
    build()
