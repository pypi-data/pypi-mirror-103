from .train_yolo_utils import (
    get_classes,
    get_anchors,
    create_model,
    data_generator_wrapper
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    ReduceLROnPlateau,
    EarlyStopping,
)
import numpy as np
from . import logger

my_logger = logger.logger('ocr')


def train_yolo(config):
    class_names = get_classes(config['classes_path'])
    num_classes = len(class_names)
    anchors = get_anchors(config['anchors_path'])

    train_data_dir = config['train_data_dir']

    input_shape = (config['model_image_height'], config['model_image_width'])
    epoch = config['epochs']
    val_split = config['val_split']
    batch_size = config['batch_size']

    model = create_model(
        input_shape=input_shape,
        anchors=anchors,
        num_classes=num_classes,
        load_pretrained=False,
        weights_path='checkpoint-1.h5'
    )  # make sure you know what you freeze

    my_logger.info('Initial model created using weights '+str(
        'checkpoint-1.h5'))

    checkpoint = ModelCheckpoint(
        "checkpoint.h5",
        monitor="val_loss",
        save_weights_only=True,
        save_best_only=True,
        period=2,
    )
    reduce_lr = ReduceLROnPlateau(
        monitor="val_loss", factor=0.1, patience=3, verbose=1)
    early_stopping = EarlyStopping(
        monitor="val_loss", min_delta=0, patience=10, verbose=1
    )

    with open(train_data_dir+"/data_train.txt") as f:
        lines = f.readlines()

    np.random.shuffle(lines)
    num_val = int(len(lines) * val_split)
    num_train = len(lines) - num_val

    my_logger.info(
        "Train on {} samples, val on {} samples, with batch size {}.".format(
            num_train, num_val, batch_size
        )
    )

    # Unfreeze and continue training, to fine-tune.
    full_callbacks = [checkpoint, reduce_lr, early_stopping]

    model.compile(
        optimizer=Adam(lr=1e-4),
        loss={"yolo_loss": lambda y_true, y_pred: y_pred}
    )  # recompile to apply the change

    my_logger.info("Unfreeze all layers.")

    model.fit_generator(
        data_generator_wrapper(
            lines[:num_train], batch_size, input_shape, anchors, num_classes
        ),
        steps_per_epoch=max(1, num_train // batch_size),
        validation_data=data_generator_wrapper(
            lines[num_train:], batch_size, input_shape, anchors, num_classes
        ),
        validation_steps=max(1, num_val // batch_size),
        epochs=epoch,
        callbacks=full_callbacks,
    )
    model.save_weights("trained_weights_final.h5")


if __name__ == '__main__':
    import yaml

    # Load model config file
    with open('config/current_model.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    train_yolo(config['yolo_model'])
