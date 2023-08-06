# GCP Cloud logger

Package for [Google Cloud Logging client](https://github.com/googleapis/python-logging)

---

### Install

```
pip install gcp-cloud-logger
```

### Usage

```python
from gcp_cloud_logger import cloud_logger as logger

# Default use GOOGLE_APPLICATION_CREDENTIALS to get credential.json path
logger.setup(
    name="logger_name",
    credential_path="",
    credential_json="", # optional, if set will write json to credential_path
)

# Info
logger.info("Test info log message")

# Warning
logger.warn("Test warning log message")

# Error
logger.error("Test error log message")

# Critical
logger.critical("Test critical log message")
```

### Usage before version 0.1.0

```python
from gcp_cloud_logger import CloudLogger

# Default use GOOGLE_APPLICATION_CREDENTIALS to get credential.json path

logger = CloudLogger(
    name="gcp_cloud_logger",
    credential_path="/path/to/your/credential.json",
)

# Info
logger.info("Test info log message")

# Warning
logger.warn("Test warning log message")

# Error
logger.error("Test error log message")

# Critical
logger.critical("Test critical log message")
```

### Result

![Result log](/docs/result.png)
