from pdf2xlsx import Extractor

if __name__ == "__main__":
    extractor = Extractor(
        lang_list=["ru"],
    )
    extractor.extract(
        "./pdfs/d.pdf",
        "./xlsx/tables.xlsx",
        char_columns=[1, 2],
        num_columns=[0, 5],
        dpi=300,
    )