from utility.util_datastores import batch_write_dynamodb_items, write_dynamodb_item

from decimal import *
from datetime import datetime
import logging
import csv
import argparse

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_none(value):
    None_List = ['None', 'none', 'False', 'false', 'No', 'no', None, False, ["None"], ["False"]]

    if not value:
        return True
    elif value in None_List:
        return True

    return False


def standardize_dynamo_query(input_data):
    if not isinstance(input_data, dict):
        logging.error("wrong data type for dynamodb")
        return None

    timestamp = str(datetime.utcnow().timestamp())
    input_data['updatedAt'] = timestamp

    if 'createdAt' not in input_data:
        input_data['createdAt'] = timestamp

    # An AttributeValue may not contain an empty string
    for k, v in input_data.items():
        if is_none(v):
            input_data[k] = None
        if isinstance(v, float):
            input_data[k] = Decimal(str(v))
    return input_data


# Note this will overwrite items with the same primary key (upsert)
def batch_write_dynamodb_items(lod_to_write, table):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)

    with table.batch_writer() as batch:
        for item in lod_to_write:
            standard_item = standardize_dynamo_query(item)
            if standard_item:
                batch.put_item(Item=standard_item)

    logging.info(f"Succcessfully did a Dynamo Batch Write to {table}")
    return True


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-filename', required=True, help="The name of your input file. Include .csv")
    argparser.add_argument('-table', required=True, help="The name of the table you're writing to")

    args = argparser.parse_args()

    with open(args.filename) as f:
        file_as_lod = [row for row in csv.DictReader(f, skipinitialspace=True)]

    print(f"Your input file has {len(file_as_lod)} rows")
    batch_write_dynamodb_items(file_as_lod, args.table)
