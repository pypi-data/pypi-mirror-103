"""Representation of stored Plots & Metrics."""

from dataclasses import asdict, dataclass
import toml
from typing import List

from aidkitcli.data_access.authentication import get_url


@dataclass
class Plot:
    """Data class containing all the information about a plot.

    :param name: name of the plot
    :param description: explanation of what is displayed on the plot
    :param url: clickable link to the plot
    """
    name: str
    description: str
    url: str


@dataclass
class Metric:
    """Data class containing all the information about a metric.

    :param name: name of the metric
    :param description: description of the metric
    :param value: numerical value of the metric
    """
    name: str
    description: str
    value: float


@dataclass
class Report:
    """Data class containing the list of plots & metrics returned by an
    analysis.

    :param Plot plots: list of displayed plots
    :param Metric metrics: list of calculated metrics
    """
    plots: List[Plot]
    metrics: List[Metric]

    def __str__(self):
        return toml.dumps(asdict(self))

    def save(self, path: str):
        report_dict = asdict(self)
        with open(path, 'w') as f:
            toml.dump(report_dict, f)


def dict2report(report_dict: dict) -> Report:
    """Create an instance of the Report class from a dictionary containing the
    information about the plots and metrics returned by an analysis.

    :param report_dict: dictionary containing the information about the plots
        and metrics
    :return: instance of the Report class
    """
    plots_dict = report_dict.get('plots', [])
    metrics_dict = report_dict.get('metrics', [])
    plots_model = [
        Plot(
            name=plot['name'],
            description=plot['description'],
            url=get_url() + plot['url']
        )
        for plot in plots_dict
    ]
    metrics_model = [
        Metric(
            name=metric['name'],
            description=metric['description'],
            value=metric['value']
        )
        for metric in metrics_dict
    ]
    report_model = Report(
        plots=plots_model,
        metrics=metrics_model
    )
    return report_model
