import easyocr
from .image_processor import ImageProcessor

class Reader():
    digit_list = "0123456789"
    char_list ="абвгдеёжзийклмнопрстуфхцчшщьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ.-№ "
    dchar_list = char_list + digit_list + "()%/"
    def __init__(self, lang_list=["ru", "en"], char_cols=[], num_cols=[]):
        self.reader = easyocr.Reader(lang_list=lang_list)
        self.char_cols = char_cols
        self.num_cols = num_cols
        

    def read(self, cells):
        data = []
        for row_num, row in enumerate(cells):
            row_data = []
            for i, cell_image in enumerate(row):
                cell_image = ImageProcessor.tight_crop(cell_image, pad=5)

                allowlist = self.dchar_list
                if i in self.char_cols:
                    allowlist=self.char_list
                elif i in self.num_cols:
                    allowlist = self.digit_list
                if row_num == 0:
                    allowlist = None

                result = self.reader.readtext(
                    cell_image, 
                    paragraph=True, 
                    allowlist=allowlist, 
                    detail=0, 
                    mag_ratio=1.2,
                )
                text = result[0] if len(result) > 0 else ""
                row_data.append(text)

            data.append(row_data)

        return data
