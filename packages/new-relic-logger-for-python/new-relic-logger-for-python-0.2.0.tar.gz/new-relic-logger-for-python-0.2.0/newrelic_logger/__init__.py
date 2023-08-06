import os

from .newrelic_logger import NewRelicLogger

if not os.environ.get("NEW_RELIC_LOGGER_AUTOIMPORT_DISABLE", False):
    NewRelicLogger()
