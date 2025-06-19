from PIL import Image
from pdf2image import convert_from_path
import pandas as pd

class FileHandler():
    @staticmethod
    def read_pdf(path_to_pdf: str, dpi=300) -> list[Image.Image]:
        images = convert_from_path(path_to_pdf, dpi)
        return images
    
    @staticmethod
    def save_to_excel(output_path: str, tables: list[pd.DataFrame]) -> None:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                table.to_excel(writer, sheet_name=f"{i+1}", index=False, header=False)
