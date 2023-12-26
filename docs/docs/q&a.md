## General

#### How does the API data set differ from other Boavizta' data set?
While the [digital product carbon footprint repository](https://github.com/Boavizta/environmental-footprint-data) aggregates non-transparent manufacturer data, the API reports impacts via an open, auditable and improvable bottom-up approach. 
Our impacts factors relies on peered reviewed publications taken from scientific or industrial literature.

#### How the API data differs to other datasets (like Negaoctet or Ecoinvent for example)?
The API is not intended to offer the same level of quality as paid databases. However, it allows anyone to evaluate the impacts of digital assets in a free, automated, open, auditable and community-improvable way.

## Methodology

#### How does the API compute environmental impacts related to raw material acquisition, manufacture, transport and end of life?

Those impacts are retrieved with a bottom-up approach when possible. The impacts are evaluated according to the technical configuration of the components sent by the user or completed by the API. Note that end of life is not taken into account in this approach for now. We want to take them into account. However, we lack open impact factors to do so. If you have ideas to fill this gap, please let us know.

When a bottom-up approach is not possible we rely on non-specific impact factors per type of equipment.

See: [Embedded methodology](./Explanations/embedded_methodology.md)


#### How does the API compute environmental impacts related to usage?

Usage impacts are retrieved by multiplying a power over a duration with an impact factor relative to the place of use of the evaluated asset.

See: [Usage methodology](Explanations/usage/usage.md)

#### How does the API handle electrical consumption?

Electrical consumption can either be given by the user or modeled according to the context of use and the technical configuration of the asset. 

See: [Electricity methodology](Explanations/usage/elec_conso.md)

#### How do we compute the impacts of cloud instances?

The technical configuration of cloud instances are pre-recorded in the API.
Their impacts are computed through the bottom-up process. The electricity is modeled from the technical configuration and the context of usage given by the user.

See: [Cloud methodology](Explanations/services/cloud.md)

#### How does the API amortize embedded impacts?
The API implements two methods to amortize embedded impacts
Either the total embedded impact is given or a linear amortization over the life cycle of the assets can be applied.

See: [Allocation methodology](Explanations/embedded_methodology.md#allocation)

#### How do we handle missing data?
The API returns impacts regardless of the level of detail given by the user. To do this, two strategies are possible: 

* Default data can be used depending on the "archetype" selected by the user

See: [Archetype](Explanations/archetypes.md)


* Data can be completed according to other values sent by the user

See: [Auto complete](Explanations/auto_complete.md)

## Technical

#### How can I use the API?

There are many ways to use the API :

* You can use our test endpoint : api.boavizta.org 
* You can deploy it yourself : 
  * With docker : ```docker run ghcr.io/boavizta/boaviztapi:latest```
  * From the source code : https://github.com/boavizta/boaviztapi/
* You can use it through our SDK
  * Python : https://pypi.org/project/boaviztapi-sdk/
  * Rust : https://github.com/Boavizta/boaviztapi-sdk-rust

See: [Deploy](Reference/deploy.md)

#### What do I need to deploy the API?

Nothing! The API is stateless.

## Contribution

#### How to contribute or point inconsistencies / errors in the dataset?

You can either [open an issues](https://github.com/Boavizta/boaviztapi/issues) on our GitHub or [contact us](https://boavizta.org/contact).

#### How can I help?

Several contributions are possible :

* Code: Contribute to the [open issues](https://github.com/Boavizta/boaviztapi/issues)
* Methodology: Open issues on our [GitHub](https://github.com/Boavizta/boaviztapi/) to criticize, propose improvements, or extend the scope of our methodology.
* Crowdsourcing: Help us collect missing data
