from PIL import Image
from pdf2image import convert_from_path
import pandas as pd

class FileHandler():
    def __init__(self, path_to_pdf: str, output_path: str, dpi=300):
        self.path_to_pdf = path_to_pdf
        self.output_path = output_path
        self.dpi = dpi
        
    def read_pdf(self) -> list[Image.Image]:
        images = convert_from_path(self.path_to_pdf, dpi=self.dpi)
        return images
    
    def save_to_excel(self, tables: list[pd.DataFrame]) -> None:
        with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                table.to_excel(writer, sheet_name=f"{i+1}", index=False, header=False)
