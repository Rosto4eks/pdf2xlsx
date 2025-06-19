from pdf2xlsx import Extractor

if __name__ == "__main__":
    extractor = Extractor(
        "./pdfs/d.pdf",
        "./xlsx/tables.xlsx",
        lang_list=["ru"],
        dpi=300,
        char_cols=[1, 2],
        num_cols=[0, 5]
    )
    extractor.extract()