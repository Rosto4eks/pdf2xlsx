from pdf2xlsx import Extractor
import argparse
import os
from pathlib import Path

class Client():
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='PDF to XLSX converter via ocr and cv'
        )
        parser.add_argument('pdf_path',  type=str, help='path to pdf')
        parser.add_argument('--xlsx_path', type=str, default="", help='path to xlsx')

        self.parser = parser

    def __parse_paths(self):
        args = self.parser.parse_args()

        pdf_path = Path(args.pdf_path)

        if not pdf_path.exists():
            raise Exception("incorrect pdf file path")
    
        if not pdf_path.is_file():
            raise Exception("incorrect pdf file path")
        
        xlsx_path = args.xlsx_path
        
        if not xlsx_path:
            directory = pdf_path.parent
            filename = pdf_path.stem + ".xlsx"
            xlsx_path = os.path.join(directory, filename)
        else:
            xlsx_path = Path(xlsx_path)

            if not xlsx_path.exists():
                raise Exception("incorrect pdf file path")
        
            if not xlsx_path.is_file():
                raise Exception("incorrect pdf file path")
        
        return pdf_path, xlsx_path


    def run(self):
        pdf_path, xlsx_path = self.__parse_paths()

        extractor = Extractor(
            pdf_path,
            xlsx_path,
            lang_list=["ru"],
            dpi=300,
            char_cols=[1, 2],
            num_cols=[0, 5]
        )
        extractor.extract()

if __name__ == "__main__":
    client = Client()
    client.run()