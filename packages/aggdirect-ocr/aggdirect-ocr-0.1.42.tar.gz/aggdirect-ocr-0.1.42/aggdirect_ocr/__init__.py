from . import ml_model
from . import dump_ticket_classifier
from . import digit_recognizer
from . import digit_recognizer_utils
from . import yolo
from yaml import load, FullLoader
import pkgutil
import os
import shutil


def get_config(model_used):
    config = load(pkgutil.get_data(__name__, "config/{}.yaml".format(model_used)), Loader=FullLoader)
    return config


def create_required_directories():
    if not os.path.isdir("aggdirect_ocr_models"):
        os.mkdir("aggdirect_ocr_models")

    if not os.path.isdir("aggdirect_ocr_training_data"):
        os.mkdir("aggdirect_ocr_training_data")


def remove_all_data():
    if os.path.isdir('aggdirect_ocr_models'):
        shutil.rmtree('aggdirect_ocr_models')
    if os.path.isdir('aggdirect_ocr_training_data'):
        shutil.rmtree('aggdirect_ocr_training_data')


create_required_directories()
