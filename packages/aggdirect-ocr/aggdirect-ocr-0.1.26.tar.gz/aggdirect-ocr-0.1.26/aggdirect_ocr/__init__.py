from . import ml_model
from . import dump_ticket_classifier
from yaml import load, FullLoader
import pkgutil


def get_config(model_used):
    config = load(pkgutil.get_data(__name__, "config/{}.yaml".format(model_used)), Loader=FullLoader)
    return config


