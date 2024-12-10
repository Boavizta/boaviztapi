# Completing and updating Scaleway Instances data

The Scaleway export can be done via the [scw-environmental-footprint](https://github.com/Shillaker/scw-environmental-footprint) project, specifically following [this doc](https://github.com/Shillaker/scw-environmental-footprint/blob/main/docs/boavizta.md).

This does the following:

- Lists all types of Instances using the Scaleway API
- Maps these to a set of hard-coded base server types (see below)
- Generates two CSV files: `instances.csv` (the instance types), and `servers.csv` (the base servers)

To add to Boavizta:

- Copy `instances.csv` to `boaviztapi/data/archetypes/cloud/scaleway.csv` (simply overwrite if updating)
- Add the lines form `servers.csv` to `boaviztapi/data/archetypes/server.csv` (delete all existing servers starting with `scw_` if you are updating)

## Testing

1. Update CSV files
2. Build the Docker image locally: `docker build -t boaviztapi-dev .`
3. Run it `docker run -p "5000:5000" -t boaviztapi-dev`

You can then run the script to check the changes using the `check.py` script in this directory:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 check.py
```

## Scripting

It would be much better if this code lived in the Boavizta repo. It can be scripted relatively easily:

1. Hard-code the base server types held in the [scw-environmental-footprint](https://github.com/Shillaker/scw-environmental-footprint) repo [here](https://github.com/Shillaker/scw-environmental-footprint/blob/main/model/instances.go)
2. Use the [scaleway-sdk-python](https://github.com/scaleway/scaleway-sdk-python) to list all the Instance types
3. Map these the the underlying base server types based on the prefix of the Instance type
4. Print two CSV files: i) `instances.csv` with the instance types; ii) `servers.csv` with the specs of the base servers
