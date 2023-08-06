from .ml_model import MLModel
import time
import os
import tensorflow as tf
import numpy as np
from uuid import uuid4
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from . import logger
my_logger = logger.logger('ocr')


class DumpTicketClassifier(MLModel):
    def __init__(self, model_name, model_id=None, config_version='current_model', do_not_update=False):
        super().__init__(model_name, model_id, config_version, do_not_update)

    def _get_objects_from_s3(self, dest_dir='ocr/dao/models/'):
        s3_client = self._get_s3_client()
        file_to_download = '{mod_name}_latest.{ext}'.format(
                mod_name=self.model_name, ext='h5')
        s3_client.download_file(
            os.environ['S3_MODEL_BUCKET'],
            file_to_download, dest_dir+file_to_download)
        return dest_dir+file_to_download

    def model_architecture(self, num_classes, img_height, img_width):
        # Define model architecture
        self.model = Sequential([
            layers.experimental.preprocessing.Rescaling(
                1./255, input_shape=(img_height, img_width, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(num_classes)
        ])

        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(
                from_logits=True),
            metrics=['accuracy'])

    def load_model(self):
        # Load classification model architecture
        self.classes = self.config['classes']
        num_classes = len(self.classes)
        self.model_architecture(
            num_classes,  # Number of output classes
            self.config['model_image_height'],  # Input image height
            self.config['model_image_width'])  # Input image width
        weights_path = self._get_objects_from_s3(self.config['model_dir'])
        # Load weights in model
        self.model.load_weights(weights_path)
        self.graph = tf.compat.v1.get_default_graph()
        # delete local files
        os.remove(weights_path)

    def train(self):
        my_logger.info('I am training')
        # Gather training params from config file
        img_height = self.config['model_image_height']
        img_width = self.config['model_image_width']
        train_data_dir = self.config['train_data_dir']
        batch_size = self.config['batch_size']
        epochs = self.config['epochs']
        val_split = self.config['val_split']

        # Load data for training
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            train_data_dir,
            validation_split=val_split,
            subset="training",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            train_data_dir,
            validation_split=val_split,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)

        # Save checkpoints with new version number. Only the checkpoint with
        # highest validation accuracy will be saved.
        new_params_id = uuid4().hex
        file_name = '{mod_name}_{model_id}.{ext}'.format(
                mod_name=self.model_name, model_id=new_params_id, ext='h5')
        new_weights_path = self.config['model_dir']+file_name
        my_logger.info('New weights will be saved as '+str(new_weights_path))

        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
                filepath=new_weights_path,
                save_weights_only=True,
                monitor='val_accuracy',
                mode='max',
                save_best_only=True)

        # Load classification model architecture
        self.classes = self.config['classes']
        self.model_architecture(
            len(self.classes),  # Number of output classes
            self.config['model_image_height'],  # Input image height
            self.config['model_image_width'])  # Input image width
        weights_path = self._get_objects_from_s3(self.config['model_dir'])
        my_logger.info('Initial weights loaded from '+str(weights_path))
        # Load weights in model
        self.model.load_weights(weights_path)

        # delete local files
        os.remove(weights_path)

        # Train model
        self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[model_checkpoint_callback]
            )

        # Upload new weights to S3
        self._upload_file(
            self._get_s3_client(), new_weights_path,
            os.environ['S3_MODEL_BUCKET'], file_name)

        # Update manifest on S3
        file_name = 'manifest_{mod_name}.{ext}'.format(
            mod_name=self.model_name, ext='txt')

        save_to = self.config['model_dir']+file_name
        self._save_new_manifest(new_params_id, save_to)

        self._upload_file(
            self._get_s3_client(), save_to,
            os.environ['S3_MODEL_BUCKET'], file_name)

        # Delete weights and manifest
        os.remove(save_to)
        os.remove(new_weights_path)

    def predict(self, image_array: np.ndarray):
        start = time.time()
        # 1. Resize image to match model input
        image_array = tf.image.resize(
            image_array,
            size=[180, 180])

        # 2. Add batch dimension
        image_array = tf.expand_dims(image_array, 0)  # Create a batch

        # 3. Make predictions
        with self.graph.as_default():
            predictions = self.model.predict(image_array, steps=1)

        # 4. Apply softmax function to get a probability score
        exponentials = np.exp(predictions[0])
        sum_exponentials = sum(exponentials)
        score = exponentials/sum_exponentials
        end = time.time()
        return self.classes[np.argmax(score)], end-start
