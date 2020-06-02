import logging
from pathlib import Path

from haystack.indexing.file_converters.pdftotext import PDFToTextConverter

logger = logging.getLogger(__name__)


def test_extract_pages():
    converter = PDFToTextConverter()
    pages = converter.extract_pages(file_path=Path("samples/docs/sample_pdf_1.pdf"))
    assert len(pages) == 4  # the sample PDF file has four pages.
    assert pages[0] != ""  # the page 1 of PDF contains text.
    assert pages[2] == ""  # the page 3 of PDF file is empty.


def test_table_removal():
    converter = PDFToTextConverter(remove_numeric_tables=True)
    pages = converter.extract_pages(file_path=Path("samples/docs/sample_pdf_1.pdf"))

    # assert numeric rows are removed from the table.
    assert "324" not in pages[0]
    assert "54x growth" not in pages[0]
    assert "$54.35" not in pages[0]

    # assert text is retained from the document.
    assert "Adobe Systems made the PDF specification available free of charge in 1993." in pages[0]


def test_language_validation(caplog):
    converter = PDFToTextConverter(valid_languages=["en"])
    pages = converter.extract_pages(file_path=Path("samples/docs/sample_pdf_1.pdf"))
    assert "The language for samples/docs/sample_pdf_1.pdf is not one of ['en']." not in caplog.text

    converter = PDFToTextConverter(valid_languages=["de"])
    pages = converter.extract_pages(file_path=Path("samples/docs/sample_pdf_1.pdf"))
    assert "The language for samples/docs/sample_pdf_1.pdf is not one of ['de']." in caplog.text
