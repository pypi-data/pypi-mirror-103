# AnnDB API Client Python
This package provides a Python client library for [AnnDB](https://anndb.com) API.

## Installation
```bash
pip install anndb-api
```

## Getting started
Start by creating a client instance with your API key.
```python
import anndb_api

client = anndb_api.Client('<YOUR_API_KEY>')
```
You can then use the client instance to create a dataset instance which allows you to modify and search the data stored in the index.
```python
dataset = client.vector('<DATASET_NAME>')

# Insert item
id = dataset.insert(np.random.normal(size=(32,)))

# Update item
id = dataset.update(id, np.random.normal(size=(32,)), metadata={'foo': 'bar'})

# Delete item
dataset.delete(id)

# Search
results = dataset.search(np.random.normal(size=(32,)), 5)
```
The full documentation of the client can be found in the [AnnDB documentation](https://docs.anndb.com)