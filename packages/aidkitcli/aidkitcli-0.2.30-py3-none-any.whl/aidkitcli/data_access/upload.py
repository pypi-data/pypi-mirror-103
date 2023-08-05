"""Upload and list stored models and data sets."""
import base64
import hashlib

from aidkitcli.data_access.api import RESTApi
from aidkitcli.data_access.utils import path_to_bytes

NUMBER_OF_CHARS_FOR_HASH = 8


def _get_hash(binary_content: bytes) -> str:
    m = hashlib.md5()
    m.update(binary_content)
    binary_hash = m.digest()
    return base64.b16encode(binary_hash).decode()[:NUMBER_OF_CHARS_FOR_HASH]


def upload_model(model_path: str, only_if_necessary: bool = True):
    """Upload a stored model model.

    Checks before whether the server has the model in question already
    stored, using md5 hashes.
    :param model_path: path to the model to be uploaded
    :param only_if_necessary: if true, the method checks whether the model
        already exists on the server and only uploads the model if
        necessary
    """
    file_content = path_to_bytes(model_path)
    hash = _get_hash(file_content)
    if only_if_necessary and hash in list_models():
        return [hash]
    api = RESTApi()
    return api.post_model(
        model_content=file_content,
        model_id=hash
    )


def list_models():
    """List all the uploaded models."""
    api = RESTApi()
    return api.list_models()


def upload_data(zip_path: str, only_if_necessary: bool = True):
    """Upload a data set.

    The data set is expected to consist of an `INPUT` and an `OUTPUT`
    folder and to be packed into a zip file.

    Checks before whether the server has the data set in question already
    stored, using md5 hashes.
    :param zip_path: path to the zip file to be uploaded
    :param only_if_necessary: if true, the method checks whether the data set
        already exists on the server and only uploads the data set if
        necessary"""
    file_content = path_to_bytes(zip_path)
    hash = _get_hash(file_content)
    if only_if_necessary and hash in list_data():
        return hash
    api = RESTApi()
    return api.post_data(
        zip_content=file_content,
        data_id=hash,
    )


def list_data():
    """List all the uploaded data sets."""
    api = RESTApi()
    return api.list_data()
