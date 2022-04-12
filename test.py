import os
import json
from google.cloud import spanner
from google.cloud.spanner_v1.keyset import KeySet
from google.cloud.spanner_v1.transaction import Transaction


client = spanner.Client()
instance = client.instance(os.environ["SPANNER_INSTANCE"])
database = instance.database(os.environ["SPANNER_DATABASE"])

TABLE_NAME = "JsonTable"
COLUMN_NAMES = [
    "id",
    "jsonColumn",
]
ROW_ID = "test"


def read():
    with database.snapshot(multi_use=True) as snapshot:
        rows = snapshot.read(
            TABLE_NAME,
            COLUMN_NAMES,
            KeySet(keys=[[ROW_ID]]),
        )
        # This fails or returns the wrong result (see the comments in `write()`).
        print(list(rows))


def write():
    def insert(transaction: Transaction):
        transaction.insert_or_update(
            TABLE_NAME,
            COLUMN_NAMES,
            [
                # The following row is read as:
                # [['test', {'someJson': 'yo', 'number': 'otherValue'}]]
                (
                    ROW_ID,
                    json.dumps(
                        [{"someJson": 1, "yo": ""}, {"otherValue": "👋", "number": 3}]
                    ),
                ),
                # The following row is read as:
                # [['test', {'someJson': 'yo'}]]
                # (
                #     ROW_ID,
                #     json.dumps([{"someJson": 1, "yo": ""}, {"someJson": 1, "yo": ""}]),
                # ),
                # The following row fails upon reading with the following error:
                # ValueError: dictionary update sequence element #0 has length 1; 2 is required
                # (
                #     ROW_ID,
                #     json.dumps([{"someJson": 1}]),
                # )
            ],
        )

    # This succeeds and correctly writes the JSON data.
    database.run_in_transaction(insert)


write()
read()
