import cv2
import numpy as np

class ImageProcessor():
    @staticmethod
    def __detect_rotation(image):        
        edges = cv2.Canny(image, 50, 150, apertureSize=3)
        
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is not None:
            angles = []
            for rho, theta in lines[:, 0]:
                angle = np.degrees(theta) - 90
                if -45 <= angle <= 45:
                    angles.append(angle)
            
            if angles:
                median_angle = np.median(angles)
                return median_angle
        return 0
    
    @staticmethod
    def __rotate_image(image, angle):
        if angle == 0:
            return image
        
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h), 
            flags=cv2.INTER_CUBIC, 
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    @staticmethod
    def tight_crop(img, pad=0):
        H, W = img.shape[:2]

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            img, connectivity=8
        )

        mask = np.zeros_like(img)

        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area > 25:
                mask[labels == i] = 255

        img = mask

        coords = cv2.findNonZero(img) 
        x, y, w, h = cv2.boundingRect(coords)

        x0 = max(x, 0)
        y0 = max(y, 0)
        x1 = min(x + w, W)
        y1 = min(y + h, H)

        img = cv2.copyMakeBorder(
            img[y0:y1, x0:x1], 
            pad, pad, pad, pad, 
            cv2.BORDER_CONSTANT,
            value=0
        )

        return img
    
    @staticmethod
    def process(image):
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

        image = cv2.adaptiveThreshold(
            src=image,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY_INV,
            blockSize=19,
            C=10
        )        

        rotation_angle = ImageProcessor.__detect_rotation(image)
        if abs(rotation_angle) > 1:
            return ImageProcessor.__rotate_image(image, rotation_angle)
        return image
