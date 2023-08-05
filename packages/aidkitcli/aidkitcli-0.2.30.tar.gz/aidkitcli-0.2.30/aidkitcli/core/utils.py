from dataclasses import asdict
from typing import List, Mapping

from aidkitcli.core.stored_model import DataColumn, StoredModel
from aidkitcli.data_access.stored_model_access import create_stored_model, save_stored_model
from aidkitcli.data_access.upload import upload_model


def create_toml(title: str, data: str, stored_model: StoredModel, **kwargs) -> dict:
    """
    Create a dictionary with the structure of the config TOML files and
    the information needed to run an analysis.

    :param title: title of the configuration
    :param data: name of the data set
    :param stored_model: StoredModel dataclass with the model information
    :param kwargs: additional keyword arguments related to the analyses
    :return: dictionary containing the information needed to run an analysis
    """
    toml_dict = dict()
    toml_dict["title"] = title
    toml_dict["data"] = list(data.split())
    toml_dict["model"] = asdict(stored_model)
    toml_dict["analyses"] = {**kwargs}
    return toml_dict


def configure_model(
    model_path: str,
    type: List[str],
    task: List[str],
    framework: List[str],
    start_eval: int,
    prediction_window: int,
    input: Mapping[str, DataColumn],
    output: Mapping[str, DataColumn],
    configured_model_path: str,
):
    """
    Create a configuration file containing the metadata of the model and store
    it as a .toml file at a specified location. If the model given as
    model_path does not exist on the server yet, it will be uploaded.

    :param model_path: path to the model file (.h5 or .pickle file)
    :param type: feedforward or recurrent
    :param task: classification or regression
    :param framework: keras or scikit
    :param start_eval: index of the first data point to be used for
        evaluations
    :param prediction_window: number of predictions to be aggregated by mean
        calculation
    :param DataColumn input: dictionary where each key is the name of an
        input column and each value is a DataColumn data class
    :param DataColumn output: dictionary where each key is the name of an
        output column and each value is a DataColumn data class
    :param configured_model_path: path where to store the configured model
        (.toml file)
    """
    model_id = upload_model(model_path)[0]

    stored_model = create_stored_model(
        model_id=model_id,
        type=type,
        task=task,
        framework=framework,
        start_eval=start_eval,
        prediction_window=prediction_window,
        input=input,
        output=output
    )

    save_stored_model(stored_model=stored_model, path=configured_model_path)
