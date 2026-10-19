# SDKs

Client libraries also exist for some languages. They are maintained by the community, not by Boavizta: report
bugs to their own repositories.

| Language | Library | Maintainer | Status |
|----------|---------|------------|--------|
| PHP | [boaviztapi-php](https://github.com/DavidJLN/boavizta-api-php) | [@DavidJLN](https://github.com/DavidJLN) | Community, unofficial |

## PHP

[boaviztapi-php](https://github.com/DavidJLN/boavizta-api-php) covers the v1 routes and requires
PHP 8.2+. It works with any PSR-18 HTTP client.

```bash
composer require davidjln/boaviztapi-php symfony/http-client nyholm/psr7
```

Climate impact of one year of an AWS `a1.4xlarge` instance:

```php
use Boavizta\Api\BoaviztaClient;
use Boavizta\Api\Enum\Criterion;
use Boavizta\Api\Request\ImpactOptions;

$client = BoaviztaClient::create();
$result = $client->cloud()->instanceImpact('aws', 'a1.4xlarge', new ImpactOptions(duration: 8760));

$gwp = $result->impact(Criterion::Gwp);
echo $gwp->embedded->value . ' ' . $gwp->unit; // manufacturing impact
```

See the [library's README](https://github.com/DavidJLN/boavizta-api-php#readme) for configuration
(timeout, cache, errors).

## Add your SDK

Open a pull request on [boaviztapi](https://github.com/Boavizta/boaviztapi) that adds a row to the
table above and to `SDKs.md` at the root of the repository.
