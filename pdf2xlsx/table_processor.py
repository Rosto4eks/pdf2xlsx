import cv2
import numpy as np
from .image_processor import ImageProcessor

class TableProcessor():
    @staticmethod
    def __detect_tables(image):
        h, w = image.shape[:2]
        
        hor_kernel_length = max(w // 10, 10)
        ver_kernel_length = max(h // 10, 10)

        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (hor_kernel_length, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, ver_kernel_length))
        
        horizontal_lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, vertical_kernel)
        
        table_mask = cv2.add(horizontal_lines, vertical_lines)
        
        kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        table_mask = cv2.morphologyEx(table_mask, cv2.MORPH_CLOSE, kernel_close)
        
        contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        tables = []
        min_area = w * h * 0.01 


        dilation_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        table_mask = cv2.dilate(table_mask, dilation_kernel, iterations=1)
        img_without_lines = image.copy()
        img_without_lines[table_mask > 0] = 0
        
        for contour in contours:
            x, y, w_cont, h_cont = cv2.boundingRect(contour)
            area = w_cont * h_cont
            
            if area > min_area:  
                table_image = image[y:y + h_cont, x:x + w_cont]
                tables.append((table_image, img_without_lines, (x, y)))
        
        return tables
    
    @staticmethod
    def __extract_table_structure(table_image):
        h, w = table_image.shape[:2]

        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, 
            (max(w // 10, 10), 1)
        )

        vertical_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, 
            (1, max(h // 10, 10))
        )
        
        horizontal = cv2.morphologyEx(table_image, cv2.MORPH_OPEN, horizontal_kernel)
        vertical = cv2.morphologyEx(table_image, cv2.MORPH_OPEN, vertical_kernel)
        
        return TableProcessor.__get_cells_from_lines(horizontal, vertical, w, h)
    
    @staticmethod
    def __get_cells_from_lines(horizontal, vertical, width, height):
        h_lines = []
        h_projection = np.sum(horizontal, axis=1)
        h_positions = np.where(h_projection > width * 0.5)[0]
        
        if len(h_positions) > 0:
            h_lines.append(h_positions[0])
            for i in range(1, len(h_positions)):
                if h_positions[i] - h_positions[i-1] > 5:
                    h_lines.append(h_positions[i])
        
        v_lines = []
        v_projection = np.sum(vertical, axis=0)
        v_positions = np.where(v_projection > height * 0.5)[0]
        
        if len(v_positions) > 0:
            v_lines.append(v_positions[0])
            for i in range(1, len(v_positions)):
                if v_positions[i] - v_positions[i-1] > 5:
                    v_lines.append(v_positions[i])
        
        cells = []
        for i in range(len(h_lines) - 1):
            row_cells = []
            for j in range(len(v_lines) - 1):
                cell = (v_lines[j], h_lines[i], 
                       v_lines[j+1] - v_lines[j], 
                       h_lines[i+1] - h_lines[i])
                row_cells.append(cell)
            cells.append(row_cells)
        
        return cells
    
    @staticmethod
    def get_cells(image):
        all_cells = []

        for table_image, img_without_lines, table_offset in TableProcessor.__detect_tables(image):
            cells = TableProcessor.__extract_table_structure(table_image)

            offset_x, offset_y = table_offset
            adjusted_cells = []
            for row in cells:
                adjusted_row = []
                for cell in row:
                    x, y, w, h = cell
                    x += offset_x
                    y += offset_y

                    img_h, img_w = img_without_lines.shape[:2]
                    adjusted_cell = img_without_lines[
                        max(0, y - 2) : min(img_h, y + h + 2),
                        max(0, x - 2) : min(img_w, x + w + 2),
                    ]
                    adjusted_row.append(adjusted_cell)
                adjusted_cells.append(adjusted_row)
            all_cells.append(adjusted_cells)

        return all_cells
