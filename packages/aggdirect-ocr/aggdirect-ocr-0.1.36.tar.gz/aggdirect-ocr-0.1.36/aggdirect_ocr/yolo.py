"""
Class definition of YOLO_v3 ticket number detection model on image
"""
from timeit import default_timer as timer
from . import ml_model as ml_model
import numpy as np
# from uuid import uuid4
from . import yolo3_utils as yolo3_utils
from . import yolo3_architecture as yolo3_architecture
# from keras.utils import multi_gpu_model
import tensorflow.compat.v1 as tf
import tensorflow.python.keras.backend as K
from tensorflow.keras.layers import Input
from .train_yolo import train_yolo
import os
from . import logger
# Get log file
my_logger = logger.logger('ocr')

tf.disable_eager_execution()


class YOLO(ml_model.MLModel):
    def __init__(self, model_name, config, model_date=None, **kwargs):
        super().__init__(model_name, config, model_date)

    def _get_objects_from_s3(self, dest_dir):
        s3_client = self._get_s3_client()
        file_to_download = '{mod_name}_latest.{ext}'.format(
                mod_name=self.model_name, ext='h5')
        s3_client.download_file(
            os.environ['S3_MODEL_BUCKET'],
            file_to_download, dest_dir+file_to_download)
        return dest_dir+file_to_download

    def _get_class(self):
        with open(self.classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        with open(self.anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(",")]
        return np.array(anchors).reshape(-1, 2)

    def load_model(self):
        mHeight = self.config['model_image_height']
        mWidth = self.config['model_image_width']
        self.classes_path = self.config['classes_path']
        self.anchors_path = self.config['anchors_path']
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.score = self.config['score']
        self.iou = self.config['iou']
        self.model_image_size = (mHeight, mWidth)
        self.gpu_num = self.config['gpu_num']

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        self.yolo_model = (
            yolo3_architecture.yolo_body(
                Input(shape=(None, None, 3)), num_anchors // 3, num_classes
            )
        )
        weights_path = self._get_objects_from_s3(self.config['model_dir'])

        # Load weights in model
        self.yolo_model.load_weights(weights_path)

        # delete local files
        os.remove(weights_path)

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2,))

        # Following multi-gpu code is **NOT TESTED**--Suchita
        # if self.gpu_num >= 2:
        #     self.yolo_model = multi_gpu_model(
        #         self.yolo_model, gpus=self.gpu_num)
        boxes, scores, classes = yolo3_utils.yolo_eval(
            self.yolo_model.output,
            self.anchors,
            len(self.class_names),
            self.input_image_shape,
            score_threshold=self.score,
            iou_threshold=self.iou,
        )
        self.boxes = boxes
        self.scores = scores
        self.classes = classes

    def train(self):
        my_logger.info('I am training YOLO')
        train_yolo(self.config)

    def predict(self, image, show_stats=True):
        start = timer()

        if self.model_image_size != (None, None):
            assert self.model_image_size[0] % 32 == 0, "Multiples of 32"
            assert self.model_image_size[1] % 32 == 0, "Multiples of 32"
            boxed_image = yolo3_utils.letterbox_image(
                image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (
                image.width - (image.width % 32),
                image.height - (image.height % 32),
            )
            boxed_image = yolo3_utils.letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype="float32")
        image_data /= 255.0
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                # K.learning_phase(): 0,
            },
        )
        out_prediction = []

        for i, c in reversed(list(enumerate(out_classes))):
            box = out_boxes[i]
            score = out_scores[i]

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype("int32"))
            left = max(0, np.floor(left + 0.5).astype("int32"))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype("int32"))
            right = min(image.size[0], np.floor(right + 0.5).astype("int32"))

            # image was expanded to model_image_size: make sure it did not pick
            # up any box outside of original image (run into this bug when
            # lowering confidence threshold to 0.01)
            if top > image.size[1] or right > image.size[0]:
                continue

            # output as xmin, ymin, xmax, ymax, class_index, confidence
            out_prediction.append([left, top, right, bottom, c, score])

        end = timer()
        return out_prediction, end - start


if __name__ == "__main__":
    import yaml
    with open('config/current_model.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    yolo_model = YOLO('yolov3', config['yolo_model'])
