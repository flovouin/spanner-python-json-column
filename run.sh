export GOOGLE_CLOUD_PROJECT=demo-python
export SPANNER_EMULATOR_HOST=localhost:9010
export SPANNER_INSTANCE=local
export SPANNER_DATABASE=json-db

python test.py
