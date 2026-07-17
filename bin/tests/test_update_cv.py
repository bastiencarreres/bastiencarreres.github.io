import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from update_cv import (
    parse_sections,
    parse_cventries,
    strip_latex,
    tex_to_resume_updates,
)


SAMPLE_TEX = r"""
\begin{document}

\section*{Education}
\cventry{PhD -- Astrophysics and Cosmology}{Aix-Marseille Université}{Marseille, France}{2023}{Thesis title: Measurement of the growth rate of structures.}
\cvspace
\cventry{Master's degree -- Subatomic Physics and Cosmology}{Université Grenoble-Alpes}{Grenoble, France}{2020}{Graduated with honors}

\section*{Research Experience}
\cventry{Post-doctoral Associate}{Duke University}{Durham, NC, USA}{Nov.~2023~--~Present}{Supervisor: Prof. Dan Scolnic.\\
Subjects: Cosmology with low-$z$ SNe~Ia.}

\section*{Teaching \& Mentoring Experience}
\subsection*{Teaching}
\cventry{Calculus tutoring}{Université de Montpellier}{Montpellier, France}{Oct.~2017~--~Dec.~2017}{Tutoring for first-year college students.}
\subsection*{Student Mentoring}
\cventry{PhD student Mentoring}{Duke University}{}{Nov.~2023~--~Present}{Maria Acevedo -- Subject: Cosmology with the DEBASS survey.}

\section*{Responsibilities \& Services}
\cventry{Reviewer for MNRAS}{}{}{Feb.~2025~--~Present}{Review of 1 publication.}

\section*{Awards \& Grant}
\cventry{Marie Skłodowska-Curie Actions Postdoctoral Fellowship}{European Commission}{}{2025}{
Project ``PEGASUS'': Probing dark Energy \\
Amount: €276,187\\
Host organisation: University of Oxford, UK\\
}

\end{document}
"""


def test_parse_sections_finds_all():
    sections = parse_sections(SAMPLE_TEX)
    assert set(sections) >= {
        "Education",
        "Research Experience",
        "Teaching & Mentoring Experience",
        "Responsibilities & Services",
        "Awards & Grant",
    }


def test_parse_cventries_extracts_fields():
    sections = parse_sections(SAMPLE_TEX)
    entries = parse_cventries(sections["Education"])
    assert len(entries) == 2
    assert entries[0]["title"] == "PhD -- Astrophysics and Cosmology"
    assert entries[0]["org"] == "Aix-Marseille Université"
    assert entries[0]["location"] == "Marseille, France"
    assert entries[0]["dates"] == "2023"
    assert "growth rate" in entries[0]["details"]


def test_parse_cventries_tracks_subsections():
    sections = parse_sections(SAMPLE_TEX)
    entries = parse_cventries(sections["Teaching & Mentoring Experience"])
    assert entries[0]["subsection"] == "Teaching"
    assert entries[1]["subsection"] == "Student Mentoring"


def test_strip_latex():
    assert strip_latex(r"low-$z$ SNe~Ia") == "low-z SNe Ia"
    assert strip_latex(r"Nov.~2023~--~Present") == "Nov. 2023 -- Present"
    assert strip_latex(r"``PEGASUS''") == '"PEGASUS"'
    assert strip_latex(r"line one\\line two") == "line one\nline two"
    assert strip_latex(r"\href{https://x.org}{text}") == "text"
    assert strip_latex(r"\textbf{bold}") == "bold"
    assert strip_latex(r"Amount: \$5,000") == "Amount: $5,000"


def test_tex_to_resume_updates_shapes():
    updates = tex_to_resume_updates(SAMPLE_TEX)
    assert set(updates) == {
        "education",
        "research_experience",
        "teaching",
        "volunteer",
        "grants",
    }
    edu = updates["education"]
    assert edu[0]["institution"] == "Aix-Marseille Université"
    assert edu[0]["studyType"] == "PhD -- Astrophysics and Cosmology"
    assert edu[1]["score"] == "Graduated with honors"

    teach = updates["teaching"]
    assert teach[0]["course"] == "Calculus tutoring"
    assert "subsection" not in teach[0]
    assert teach[1]["subsection"] == "Student Mentoring"

    vol = updates["volunteer"]
    assert vol[0]["position"] == "Reviewer for MNRAS"
    assert vol[0]["summary"] == "Review of 1 publication."

    grants = updates["grants"]
    assert grants[0]["title"] == "Marie Skłodowska-Curie Actions Postdoctoral Fellowship"
    assert grants[0]["awarder"] == "European Commission"
    assert grants[0]["date"] == "2025"
    assert any("276,187" in h for h in grants[0]["highlights"])
