import os
import sys
from pathlib import Path
from docx import Document

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from report_generator.styles import configure_document
from report_generator.front_matter import add_front_matter
from report_generator.chapter1 import add_chapter_1
from report_generator.chapter2 import add_chapter_2
from report_generator.chapter3 import add_chapter_3
from report_generator.chapter4 import add_chapter_4
from report_generator.chapter5 import add_chapter_5
from report_generator.chapter6 import add_chapter_6
from report_generator.chapter7 import add_chapter_7
from report_generator.chapter8 import add_chapter_8
from report_generator.chapter9 import add_chapter_9
from report_generator.references import add_references

def generate_full_report():
    print("=" * 80)
    print("   HEARTCARE AI - FINAL-YEAR B.TECH PROJECT REPORT GENERATOR (.DOCX)")
    print("=" * 80)
    
    doc = Document()
    print("[1/12] Configuring document page layout, margins, and headers...")
    configure_document(doc)

    print("[2/12] Generating Front Matter (Title Page, Cert, Decl, Ack, Abstract, TOC, LOF, LOT)...")
    add_front_matter(doc)

    print("[3/12] Generating Chapter 1 – Introduction...")
    add_chapter_1(doc)

    print("[4/12] Generating Chapter 2 – Literature Survey...")
    add_chapter_2(doc)

    print("[5/12] Generating Chapter 3 – Project Flow and Methodology...")
    add_chapter_3(doc)

    print("[6/12] Generating Chapter 4 – System Design...")
    add_chapter_4(doc)

    print("[7/12] Generating Chapter 5 – Implementation...")
    add_chapter_5(doc)

    print("[8/12] Generating Chapter 6 – Result Analysis...")
    add_chapter_6(doc)

    print("[9/12] Generating Chapter 7 – Testing...")
    add_chapter_7(doc)

    print("[10/12] Generating Chapter 8 – Maintenance of the System...")
    add_chapter_8(doc)

    print("[11/12] Generating Chapter 9 – Deployment...")
    add_chapter_9(doc)

    print("[12/12] Generating Academic References (Harvard System)...")
    add_references(doc)

    # Save destinations
    output_filename = "HeartCare_AI_Final_Year_Project_Report.docx"
    workspace_path = root_dir / output_filename
    
    print(f"\n[*] Saving Microsoft Word document to: {workspace_path} ...")
    doc.save(str(workspace_path))

    # Also save a copy to artifact directory if available
    artifact_dir = Path("C:/Users/shiva/.gemini/antigravity-ide/brain/1a4b561f-9e16-4f36-9a21-70fccbe8453d")
    if artifact_dir.exists():
        artifact_path = artifact_dir / output_filename
        doc.save(str(artifact_path))
        print(f"[*] Artifact copy saved to: {artifact_path}")

    file_size_kb = os.path.getsize(str(workspace_path)) / 1024
    print("=" * 80)
    print(f" [SUCCESS] REPORT GENERATION COMPLETE!")
    print(f" Output File: {workspace_path}")
    print(f" File Size:   {file_size_kb:.1f} KB")
    print("=" * 80)

if __name__ == "__main__":
    generate_full_report()
