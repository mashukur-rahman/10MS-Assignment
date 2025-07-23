import pdfplumber
import pytesseract
from PIL import Image
import re
from typing import List, Optional

def extract_text_from_pdf(pdf_path: str, page_numbers: Optional[List[int]] = None) -> List[str]:
    """
    Extract and normalize text from specified pages of a PDF using OCR (Bengali).
    If page_numbers is None, extract from all pages.
    Returns a list of normalized text strings (one per page).
    """
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        pages = page_numbers if page_numbers is not None else range(len(pdf.pages))
        for i in pages:
            page = pdf.pages[i]
            pil_image = page.to_image(resolution=600).original
            text = pytesseract.image_to_string(pil_image, lang="ben")
            if text:
                normalized = re.sub(r'\n{2,}', '<<PARA>>', text)
                normalized = re.sub(r'\n', ' ', normalized)
                normalized = re.sub(r'<<PARA>>', '\n\n', normalized)
                texts.append(normalized)
            else:
                texts.append("")
    return texts 