from .file_handler import FileHandler
from .reader import Reader
from .post_processor import PostProcessor
from .image_processor import ImageProcessor
from .table_processor import TableProcessor
from tqdm import tqdm

class Extractor():
    def __init__(
            self, 
            path_to_pdf: str, 
            output_path: str,
            lang_list=["ru", "en"],
            dpi=300, 
            char_cols=[],
            num_cols=[],
        ):
        self.__io_handler = FileHandler(
            path_to_pdf,
            output_path,
            dpi=dpi
        )

        self.__reader = Reader(
            lang_list=lang_list, 
            char_cols=char_cols,
            num_cols=num_cols,
        )
        
        self.__post_processor = PostProcessor(
            index_col_pos=0,
            fix_index=True,
            separate_policy="table",
            has_header_on_new_page=True,
        )
        
    def extract(self):
        images = self.__io_handler.read_pdf()

        tables = []
        for image in tqdm(images):
            processed_image = ImageProcessor.process(image)

            cells_array = TableProcessor.get_cells(processed_image)

            for cells in cells_array:
                table = self.__reader.read(cells)
                if table and any(any(cell.strip() for cell in row) for row in table):
                    tables.append(table)

        tables = self.__post_processor.process(tables)

        self.__io_handler.save_to_excel(tables)
