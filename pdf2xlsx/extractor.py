from .file_handler import FileHandler
from .reader import Reader
from .post_processor import PostProcessor
from .image_processor import ImageProcessor
from .table_processor import TableProcessor
from tqdm import tqdm

class Extractor():
    def __init__(
            self, 
            lang_list=["ru", "en"],
        ):

        self.__reader = Reader(
            lang_list=lang_list, 
        )
        
        self.__post_processor = PostProcessor(
            index_col_pos=0,
            fix_index=True,
            separate_policy="table",
            has_header_on_new_page=True,
        )
        
    def extract(self, path_to_pdf: str, path_to_xlsx: str, char_columns=[], num_columns=[], dpi=300):
        images = FileHandler.read_pdf(path_to_pdf, dpi)

        tables = []
        for image in tqdm(images):
            processed_image = ImageProcessor.process(image)

            cells_array = TableProcessor.get_cells(processed_image)

            for cells in cells_array:
                table = self.__reader.read(cells, char_columns, num_columns)
                if table and any(any(cell.strip() for cell in row) for row in table):
                    tables.append(table)

        tables = self.__post_processor.process(tables)

        FileHandler.save_to_excel(path_to_xlsx, tables)
