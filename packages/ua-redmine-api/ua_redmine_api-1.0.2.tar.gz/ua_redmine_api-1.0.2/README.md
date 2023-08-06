# UA-EDS-API
Provides easy interface for making REST requests to University of Arizona Redmine Database.

## Motivation
To make a python API that could generically interact with the REST architecture of Redmine.

## Code Example
```python
from ua_redmine_api import ua_redmine_api

redmine_api = ua_redmine_api.RedmineApi("host", "username", "password")

data = redmine_api.get("endpoint")
```

## Installation
pip install --user ua-redmine-api

## Credits
[RyanJohannesBland](https://github.com/RyanJohannesBland)
[EtienneThompson](https://github.com/EtienneThompson)

## License
MIT
