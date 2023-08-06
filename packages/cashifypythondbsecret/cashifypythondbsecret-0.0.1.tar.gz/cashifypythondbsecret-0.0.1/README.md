# cashify-python-db-secret

Cashify Python Repo to get Database values from AWS Secret manager.

Pre-requisite:
1. Boto3 library (https://pypi.org/project/boto3/)


How to use:
1. Use steps under if want to use directly from source code
- Install library using pip install git+https://git@github.com/saket-cashify/cashify-python-db-secret.git
- Simply import the package and use function "get_secret" with arguments (secret_name, region_name) in try block and "get_secret_fallback" with arguments (secret_name, region_name) in except block to get general secret.
- add this line to requirements.txt file to install "-e git+https://git@github.com/saket-cashify/cashify-python-db-secret.git#egg=cashifypythondbsecret" automatically

2. Use these steps to use from PyPi
- pip install cashifypythondbsecret
- Simply import the package and use function "get_secret" with arguments (secret_name, region_name) in try block and "get_secret_fallback" with arguments (secret_name, region_name) in except block to get general secret.
- cashifypythondbsecret==0.0.1 to requirements
