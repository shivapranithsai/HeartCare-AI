from docx.shared import Pt, Inches
from report_generator.styles import (
    add_chapter_title, add_section_heading, add_paragraph
)

def add_references(doc):
    """Generates the References section in strict Harvard Referencing style."""
    add_chapter_title(doc, "10", "REFERENCES")

    add_paragraph(
        doc,
        "The following genuine academic publications, clinical guidelines, and technological documentation informed the research, "
        "algorithmic formulation, and architectural design of HeartCare AI. Citations adhere strictly to the Harvard referencing system:"
    )

    refs = [
        ("Benjamin, E.J., Muntner, P., Alonso, A., Bittencourt, M.S., Callaway, C.W., Carson, A.P., Sanchez, F.J., Chamberlain, A.M., Chang, A.R., Cheng, S. and Das, S.R., 2019. ",
         "Heart disease and stroke statistics—2019 update: a report from the American Heart Association. ",
         "Circulation, 139(10), pp. e56–e528. DOI: 10.1161/CIR.0000000000000659."),

        ("Chicco, D. and Jurman, G., 2020. ",
         "Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone. ",
         "BMC Medical Informatics and Decision Making, 20(1), pp. 1–16. DOI: 10.1186/s12911-020-1023-5."),

        ("Detrano, R., Janosi, A., Steinbrunn, W., Pfisterer, M., Schmid, J.J., Sandhu, S., Guppy, K.H., Lee, S. and Froelicher, V., 1989. ",
         "International application of a new probability algorithm for the diagnosis of coronary artery disease. ",
         "The American Journal of Cardiology, 64(5), pp. 304–310. DOI: 10.1016/0002-9149(89)90524-9."),

        ("Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q. and Liu, T.Y., 2017. ",
         "LightGBM: A highly efficient gradient boosting decision tree. ",
         "In: Advances in Neural Information Processing Systems (NeurIPS 2017), Vol. 30, pp. 3146–3154."),

        ("Lundberg, S.M. and Lee, S.I., 2017. ",
         "A unified approach to interpreting model predictions. ",
         "In: Advances in Neural Information Processing Systems (NeurIPS 2017), Vol. 30, pp. 4765–4774."),

        ("Mohan, S., Thirumalai, C. and Srivastava, G., 2019. ",
         "Effective heart disease prediction using hybrid machine learning techniques. ",
         "IEEE Access, 7, pp. 81542–81554. DOI: 10.1109/ACCESS.2019.2923707."),

        ("Tiangolo, S., 2024. ",
         "FastAPI: High-performance, easy to learn, fast to code, ready for production. ",
         "Available at: <https://fastapi.tiangolo.com/> [Accessed 15 September 2026]."),

        ("Whelton, P.K., Carey, R.M., Aronow, W.S., Casey, D.E., Collins, K.J., Dennison Himmelfarb, C., DePalma, S.M., Gidding, S., Jamerson, K.A., Jones, D.W. and MacLaughlin, E.J., 2018. ",
         "2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA guideline for the prevention, detection, evaluation, and management of high blood pressure in adults. ",
         "Journal of the American College of Cardiology, 71(19), pp. e127–e248. DOI: 10.1016/j.jacc.2017.11.006."),

        ("World Health Organization, 2021. ",
         "Cardiovascular diseases (CVDs): Key Facts and Global Mortality. ",
         "Geneva: World Health Organization. Available at: <https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)> [Accessed 10 September 2026].")
    ]

    for authors, title, publication in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)

        r_auth = p.add_run(authors)
        r_auth.font.name = "Calibri"
        r_auth.font.size = Pt(10)
        r_auth.font.bold = True

        r_title = p.add_run(f'"{title}" ')
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(10)

        r_pub = p.add_run(publication)
        r_pub.font.name = "Calibri"
        r_pub.font.size = Pt(10)
        r_pub.font.italic = True
