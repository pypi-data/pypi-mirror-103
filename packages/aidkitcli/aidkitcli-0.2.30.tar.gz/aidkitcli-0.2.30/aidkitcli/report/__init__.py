"""After the execution of an analysis, the plots and metrics will be displayed
on our secured web-GUI `https://<subdomain>.aidkit.ai`.

Moreover, a report will be returned in the CLI. This report will contain the
list of plots and metrics calculated as well as a link to the plots and the
values of the metrics (:ref:`example-analysis-report`).

The report is useful to integrate aidkit seamlessly into your MLOps workflow.
It is also possible to save it as a TOML file at a desired location to
simplify the comparison between different ML models
(:ref:`example-print-save-report`).
"""
from aidkitcli.core.report import Metric, Plot, Report
