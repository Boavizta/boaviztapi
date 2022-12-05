****## General

#### How does the API data set differ from other Boavizta' data set ?
While the [digital product carbon footprint repository](https://github.com/Boavizta/environmental-footprint-data) aggregates non-transparent manufacturer data, the API reports impacts via an open, auditable and improvable bottom-up approach. 
Our impacts factors relies on scientific publications.

#### How the API data differs to other datasets (like Negaoctet or Ecoinvent for example) ?
The API is not intended to offer the same level of quality as paid databases. However, it allows anyone to evaluate the impacts of digital products in a free, automated, open, auditable and community-improvable way.

## Methodology

#### How does the API compute environmental impacts related to manufacture ?

Manufacture impacts are retrieved with a bottom-up approach. The impacts are evaluated according to the technical configuration of the components sent by the user or completed by the API.

See: [Manufacture methodology](./Explanations/manufacture_methodology.md)


#### How does the API compute environmental impacts related to usage ?

Manufacture impacts are retrieved by multiplying a power hover a duration with an impact factor relative to the place of use of the evaluated product.

See: [Usage methodology](Explanations/usage/usage.md)

#### How does the API handle electrical consumption ?

Electrical consumption can either be given by the user or modeled according to the context of use and the technical configuration of the product. 

See: [Electricity methodology](Explanations/usage/elec_conso.md)

#### How do we compute the impacts of cloud instances ?

The technical configuration of cloud instances are pre-recorded in the API.
Their impacts are computed through the bottom-up process. The electricity is modeled from the technical configuration and the context of usage given by the user.

See: [Cloud methodology](Explanations/devices/cloud.md)

#### How does the API amortize manufacturing costs ?
The API implements two methods to amortize manufacturing-related impacts
Either the total cost of manufacturing impacts is given, or a linear amortization over the life cycle of the products can be applied. 

See: [Allocation methodology](Explanations/manufacture_methodology/#allocation)

#### How do we handle missing data ?
The API returns impacts regardless of the level of detail given by the user. To do this, two strategies are possible: 

* Default data can be used
* Data can be completed according to other values sent by the user

See: [Auto complete](Explanations/auto_complete.md)

#### Why don't we take into account transport and end of life impacts ?

We want to take into account the impacts related to transportation and end of life. However, we lack open impact factors to do so. If you have ideas to fill this gap, please let us know.

## Technical

#### How can I use the API ?

There are many ways to use the API :

* You can use our test endpoint : api.boavizta.org 
* You can deploy it yourself : 
  * With docker : ```docker run ghcr.io/boavizta/boaviztapi:latest```
* You can use it through our SDK
  * Python : https://pypi.org/project/boaviztapi-sdk/
  * Rust : https://github.com/Boavizta/boaviztapi-sdk-rust

See: [Deploy](Reference/deploy.md)

#### What do I need to deploy the API ?

Nothing ! The API is stateless.

## Contribution

#### How to contribute or point inconsistencies / errors in the dataset ?

You can either [open an issues](https://github.com/Boavizta/boaviztapi/issues) on our GitHub or [contact us](https://boavizta.org/contact).

#### How can I help ?

Several contributions are possible :

* Code : Contribute to the [open issues](https://github.com/Boavizta/boaviztapi/issues)
* Methodology : Open issues on our [GitHub](https://github.com/Boavizta/boaviztapi/) to criticize, propose improvements, or extend the scope of our methodology.
* Crowdsourcing : Help us collect missing data (TBD)****
