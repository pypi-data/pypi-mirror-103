## New Relic APM Logger
This library enables the standard python logger to send its logs to New Relic using an async strategy.
Note: These logs are linked to the application only in the context of a web transaction. 

## Configuration
Configure the APM agent according to the [documentation](https://docs.newrelic.com/docs/agents/python-agent/installation/standard-python-agent-install/). A `newrelic.ini` should be generated.

By default (unless NEW_RELIC_LOGGER_AUTOIMPORT_DISABLE is True), to enable the python logging module, include this line in your file. 
```python
import newrelic_logger
```
if auto import is disabled, it must be instantiated in the code
```python
from newrelic_logger import NewRelicLogger
NewRelicLogger(...)
```
### NewRelicLogger Arguments
NewRelicLogger constructor receives the following optional arguments:

|Name|Type|Description|
|---|---|---|
|app_id|int|The app id for the newrelic APM
|app_name|str|The app name for the newrelic APM
|license_key|str|The license_key for comunicating with the new relic api
|region|str|The region for newrelic, either "US" or "EU"
|log_level|ENUM|The numeric level of the logging event (one of DEBUG, INFO etc.)

### Environment Variables
Optionally, some arguments can be configured by environment variables. These are:

|Name|Description|
|---|---|
|NEW_RELIC_LOGGER_AUTOIMPORT_DISABLE|Disable the auto import functionality
|NEW_RELIC_LOGGER_PATCH_PRINT_DISABLE|Disables routing from print() function into logger.info()
|NEW_RELIC_APP_ID|The app id for the newrelic APM
|NEW_RELIC_APP_NAME|he app name for the newrelic APM
|NEW_RELIC_LICENSE_KEY|The license_key for comunicating with the new relic api
|NEW_RELIC_REGION|The region for newrelic, either "US" or "EU"

## Usage
Just use the normal python logger, for example, to send an info message:
```python
import logging
logging.info("This is an info message")
```

## Running the program
Run the application using the new relic agent either by using the admin script integration, or the manual integration, as mentioned in the [documentation](https://docs.newrelic.com/docs/agents/python-agent/installation/python-agent-advanced-integration/). For example, for the admin script:
```bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program YOUR_COMMAND_OPTIONS
```
and for the manual integration:
```python
import newrelic.agent
newrelic.agent.initialize('/some/path/newrelic.ini')
```