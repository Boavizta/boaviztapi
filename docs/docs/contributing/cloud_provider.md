# Add a new cloud provider

This guide will you add a new cloud provider into BoaviztAPI.

## Register the cloud provider

To register the new cloud provider, you will need to update the `providers.csv` file and add new line with the following required information.

- `provider.name`: The provider short name (e.g. "aws"),
- `provider.description`: Full name of the provider (e.g. "Amazon Web Services").

The file `provided.csv` is located at `boaviztapi/data/archetypes/cloud/providers.csv`.

## Add cloud instances

Then you will need to add cloud instances for that provider into a new CSV that must created using the same name as `provider.name` (e.g. `aws.csv`). The file must be created in the same location as the `providers.csv` file. You will need to have the exact same columns in the new CSV file compared to others. You can copy and paste the content of already existent list of instances from another cloud provider and remove all rows, but the first one.

To add new cloud instances please refer to this documentation: [Add a cloud instance](cloud_instance.md)