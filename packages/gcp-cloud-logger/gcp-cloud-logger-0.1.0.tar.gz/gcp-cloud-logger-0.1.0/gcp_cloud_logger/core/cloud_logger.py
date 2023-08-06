import os
import ujson as json
from google.cloud import logging as cloud_logging


class CloudLogger(object):
    def __init__(self):
        pass

    __logger = None

    def setup(self, **kwargs):
        """Setup cloud logging credential

        Keyword Args:
            name (str): logger name, format: projects/{project_id}/logs/{name}
            credential_path (str): service account key json file path
            credential_json (str or dict): service account key json string
        """

        credential_path = kwargs.get("credential_path") or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

        if credential_path is None:
            raise Exception(
                "credential_path or GOOGLE_APPLICATION_CREDENTIALS is not exists"
            )

        credential_json = kwargs.get("credential_json")

        if credential_json is not None:
            self.__credential_setup(credential_path, credential_json)

        if not os.path.isfile(credential_path):
            raise Exception("Credential file is not exists")

        client = cloud_logging.Client.from_service_account_json(credential_path)

        self.__logger = client.logger(kwargs.get("name", "gcp_cloud_logger"))

    def __credential_setup(self, credential_path: str, credential_json) -> str:
        if type(credential_json) == str:
            credential_json = json.loads(credential_json)

        if not os.path.isfile(credential_path):
            with open(credential_path, "w", encoding="utf-8") as json_file:
                json_file.write(json.dumps(credential_json))
                json_file.close()

        return credential_path

    def info(self, content):
        self.log_text(content, severity="INFO")

    def warn(self, content):
        self.log_text(content, severity="WARNING")

    def error(self, content):
        self.log_text(content, severity="ERROR")

    def critical(self, content):
        self.log_text(content, severity="CRITICAL")

    def log_text(self, content, **kwargs):
        if self.__logger is None:
            raise Exception("Please setup credential info before use cloud logger")

        if type(content) in (dict, list):
            content = json.dumps(content)

        self.__logger.log_text(content, severity=kwargs.get("severity", "INFO"))
