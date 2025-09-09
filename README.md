# rv16-lib
A shared Python utility library for the *raVioleria16* project.

This library contains common functions for configuration management, logging, and other shared logic used across multiple apps and services in the project.

## Installation
To install this library in your project, add the Git repository to your `requirements.txt` file:
```
git+[https://github.com/raVioleria16/rv16-lib.git@main#egg=rv16-lib](https://github.com/raVioleria16/rv16-lib.git@main#egg=rv16-lib)
```

Then, run:
```
pip install -r requirements.txt
```
## Example Usage
1. Load configuration from `app.yaml` file:
```python
from rv16_lib import get_object_from_config

config = get_object_from_config(filename="app.yaml")
```

2. Logging with uvicorn-style
```python
from rv16_lib import get_logger

logger = get_logger("my-service-name")
logger.info("This is an informational message.")
logger.error("An error occurred!")
```
