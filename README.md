# PDF to XLSX Table Extractor

A Python library for extracting tables from PDF documents and converting them to Excel format using computer vision and OCR techniques.

## Features

- **Automatic table detection** in PDF pages using computer vision
- **Intelligent table structure recognition** with cell boundary detection
- **Multi-page table handling** with automatic concatenation
- **Rotation correction** for skewed scans
- **Column type specification** (numeric, text, or mixed) for better recognition

## Usage

### Basic Usage

```python
from pdf2xlsx import Extractor

extractor = Extractor(lang_list=["en"])
extractor.extract("document.pdf", "tables.xlsx")
```

### Advanced Configuration

```python
# Configure text recognition languages
extractor = Extractor(lang_list=["en", "ru"])

# Specify column types for better OCR accuracy
extractor.extract(
    path_to_pdf="document.pdf",
    path_to_xlsx="output.xlsx",
    char_columns=[1, 2, 3],  # Text-only columns
    num_columns=[0, 4, 5],   # Numeric columns
    dpi=300                  # Higher DPI for better quality
)
```

### Extractor Parameters

- `lang_list`: List of languages for OCR (default: `["ru", "en"]`)

### Extract Method Parameters

- `path_to_pdf`: Input PDF file path
- `path_to_xlsx`: Output Excel file path
- `char_columns`: List of column indices containing only text
- `num_columns`: List of column indices containing only numbers
- `dpi`: PDF rendering resolution (default: 300)

### PostProcessor Configuration

The `PostProcessor` class supports these parameters:
- `separate_policy`: How to separate tables
  - `"table"`: New Excel sheet for each detected table
  - `"page"`: New sheet for each PDF page
  - `"none"`: All tables in one sheet
- `has_header_on_new_page`: Skip repeated headers on new pages

## Installation

### Python Dependencies

```bash
pip install poppler-utils
pip install pillow
pip install pdf2image
pip install pandas
pip install opencv-python
pip install numpy
pip install easyocr
pip install openpyxl
pip install tqdm
```

## Requirements

- Python 3.7+
- OpenCV
- EasyOCR
- PIL (Pillow)
- pandas
- pdf2image
- numpy
- openpyxl
- poppler-utils (system dependency)

## Limitations

- OCR accuracy depends on scan quality
- Large PDFs may require significant processing time
- Processing time scales with PDF size and DPI settings
