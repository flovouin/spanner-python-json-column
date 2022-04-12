# Python Spanner client bug

This demonstrates a bug in the Python Spanner client, which either fails or incorrectly parses a JSON column when an array is at the top level.

## TL;DR

The issue is with the [`JsonObject`](https://github.com/googleapis/python-spanner/blob/e54899cc692d5583e979b77a1c1bdd82b81a5983/google/cloud/spanner_v1/data_types.py#L27) class, which does not handle being passed a list:

```python
from google.cloud.spanner_v1.data_types import JsonObject

# This fails with:
# ValueError: dictionary update sequence element #0 has length 1; 2 is required
JsonObject([{"myFirstObject": 1}])
```

## Running the example

Start the emulator and create the local instance and database:

```shell
gcloud emulators spanner start

gcloud config set api_endpoint_overrides/spanner http://localhost:9020/
gcloud config set project demo-python
gcloud config set auth/disable_credentials true
gcloud config set spanner/instance local

gcloud spanner instances create local --config emulator-config --nodes 0 --description Test
gcloud spanner databases create --ddl-file ddl.sql json-db
```

Run the example:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./run.sh
```
