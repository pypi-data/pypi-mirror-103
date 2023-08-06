from abc import ABCMeta, abstractmethod
from apscheduler.schedulers.background import BackgroundScheduler
import boto3
import os
from . import logger
import logging
import pkgutil
from yaml import load, FullLoader
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)

# Get log file
my_logger = logger.logger('ocr')


class MLModel(metaclass=ABCMeta):
    def __init__(self, model_name, model_id=None, config_version='current_model', do_not_update=False):
        self.model_name = model_name
        self.config = self._get_config(config_version)
        self.do_not_update = do_not_update
        self.model_id = self._get_model_id(model_id)
        self.load_model()
        my_logger.info('Model {} Loaded'.format(self.model_name))
        my_logger.info('Model id from manifest '+str(self.model_id))
        self.schedule_model_check()

    @staticmethod
    def _get_s3_client():
        return boto3.client(
            "s3",
            aws_access_key_id=os.environ['S3_KEY'],
            aws_secret_access_key=os.environ['S3_SECRET']
        )

    def _get_config(self, config_version):
        config = load(pkgutil.get_data(__name__, "config/{}.yaml".format(config_version)), Loader=FullLoader)
        return config[self.model_name]

    def _upload_file(self, s3_client, file_name, bucket, object_name):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name.
        :return: True if file was uploaded, else False
        """
        my_logger.info('Uploading file to S3 '+str(file_name))
        s3_client.upload_file(file_name, bucket, object_name)

    def _save_new_manifest(self, new_model_id, save_to):
        f = open(save_to, "w")
        f.write(new_model_id)
        f.close()

    def _get_model_id(self, model_id):  # read the manifest file from s3
        if model_id is None:
            return self._read_s3_manifest()
        else:
            return model_id

    def _is_new_manifesto(self, manifest_id):
        my_logger.info(
            'Manifest id {new_date}, in-memory id {old_date}'.format(
                new_date=manifest_id, old_date=self.model_id))
        if manifest_id == self.model_id:
            return 0
        else:
            return 1

    def _read_s3_manifest(self):
        s3_client = self._get_s3_client()
        filename = 'manifest_{mod_name}.{ext}'.format(
            mod_name=self.model_name, ext='txt')
        # read from manifesto
        manifest_id = s3_client.get_object(
            Bucket=os.environ['S3_MODEL_BUCKET'],
            Key=filename
            )['Body'].read().decode('utf-8')
        return manifest_id

    def _load_if_model_updated(self):
        my_logger.info('Checking manifest {}'.format(self.model_name))
        manifest_id = self._read_s3_manifest()
        if self._is_new_manifesto(manifest_id):
            self.load_model()
            self.model_id = manifest_id
            my_logger.info('Loaded latest {} model'.format(self.model_name))
        else:
            my_logger.info('No updated {} model'.format(self.model_name))
            pass

    def schedule_model_check(self):
        if not self.do_not_update:
            scheduler = BackgroundScheduler()
            scheduler.add_job(self._load_if_model_updated, 'interval', minutes=5)
            scheduler.add_job(self.train, 'interval', minutes=10)
            scheduler.start()

    @abstractmethod
    def train(self):
        raise NotImplementedError

    @abstractmethod
    def predict(self):
        raise NotImplementedError

    @abstractmethod
    def load_model(self):  # TODO load here from s3
        raise NotImplementedError
