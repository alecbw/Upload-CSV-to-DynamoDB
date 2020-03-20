# Related article
To come

# Using this

Included is a python file for batch uploading to an existing DynamoDB table

```
python3 CSV_to_Dynamo.py -filename example_file.csv -table exampleTable
```


If you have yet to make a Dynamo table (or want to make a new one), you can use the provided serverless.yml template to quickly spin up (and later down, if you'd like) a table.

```
export DYNAMO_TABLE_NAME=exampleTable
export DYNAMO_PRIMARY_KEY=example_primary_key
sls deploy --config "serverless-datastores.yml"
```
