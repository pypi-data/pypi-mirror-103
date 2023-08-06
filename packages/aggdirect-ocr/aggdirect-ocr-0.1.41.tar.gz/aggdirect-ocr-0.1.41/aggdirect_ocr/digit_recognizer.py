from .ml_model import MLModel
import time
import os
import pytesseract
import numpy as np
import cv2
from .digit_recognizer_utils import correct_orientation,\
    preprocess_ROI, add_padding_and_clip, variance_of_laplacian,\
    cleanup_ticket_number


class DigitRecognizer(MLModel):
    def __init__(self, model_name, model_id=None, config_version='current_model', do_not_update=False):
        super().__init__(model_name, model_id, config_version, do_not_update)

    def _get_objects_from_s3(self, dest_dir):
        s3_client = self._get_s3_client()
        file_to_download = '{mod_name}_latest.{ext}'.format(
                mod_name=self.model_name, ext='traineddata')
        s3_client.download_file(
            os.environ['S3_MODEL_BUCKET'],
            file_to_download, dest_dir+file_to_download)
        return dest_dir

    def load_model(self):
        model_path = self._get_objects_from_s3(self.config['model_dir'])
        self.model_path = model_path
        self.oem = self.config['oem']
        self.psm = self.config['psm']
        self.lang = '{mod_name}_latest'.format(mod_name=self.model_name)

    def train(self):
        print('yay, I am training')
        time.sleep(60)

    def predict(self, image_pil, predictions):
        start = time.time()
        image_array = np.array(image_pil)

        # 1. Check if any boxes detected, if not return None for ticket_number
        # and other YOLO parameters. Return message = 'NotDetected'
        # If more than two BB are detected select the one
        # with highest confidence
        if len(predictions) == 0:
            text = angle = None
            xmin = ymin = None
            xmax = ymax = None
            label = confidence = None
            msg = 'NotDetected'
            end = time.time()
            return text, angle, xmin, ymin, xmax, ymax, label, confidence,\
                msg, end-start
        elif len(predictions) >= 2:
            temp = np.array(predictions)
            index = np.argmax(temp, axis=0)[-1]
            predictions = predictions[index]
            xmin, ymin, xmax, ymax, label, confidence = predictions
        else:
            xmin, ymin, xmax, ymax, label, confidence = predictions[0]

        # 2. For each BB YOLO detected a label. For now this is can be 0 for \
        # ticket_number. In future add the label-mapping here
        if label == 0:
            label = 'ticket_number'

        # 3. Get orientation of image
        angle = correct_orientation(image_array, (xmin, ymin, xmax, ymax))

        # 4. Add padding to the BB for better text recognition
        startX, startY, endX, endY = add_padding_and_clip(
            angle,  # angle of rotation
            xmin, ymin, xmax, ymax,  # BB coordinates
            np.shape(image_array)[1],  # height of image
            np.shape(image_array)[0])  # width of image

        # 6. Extract ROI from image
        roi = image_array[startY:endY, startX:endX]

        # 7. Rotate roi based on angle
        if angle == 270:
            roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 90:
            roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif angle == 180:
            roi = cv2.rotate(roi, cv2.ROTATE_180)

        # 8. We use different pre-processing parameters for blurry images\
        # for better text recognition. Compute the blurriness of image
        blurriness = variance_of_laplacian(roi)

        # 9. Lower value of blurriness indicates image is more blurry
        # use adaptive thresholding to convert a color image to a
        # black and white image since tesseract works better on such images
        if blurriness < 100:
            roi = preprocess_ROI(roi, 21, 5)
        else:
            roi = preprocess_ROI(roi, 17, 10)

        # 10. Load tesseract configs
        my_config = r'--tessdata-dir "{}" --oem {} --psm {}'.format(
            self.model_path, self.oem, self.psm)

        # 11. Run tesseract on pre-processed ROI
        text = pytesseract.image_to_string(
            roi, config=my_config, lang=self.lang)

        # 12. Remove blanks spaces, alphabets and special characters from\
        # recognized text
        text = cleanup_ticket_number(text)

        msg = 'Success'
        end = time.time()
        return text, angle, xmin, ymin, xmax, ymax, label, confidence, msg,\
            end-start
