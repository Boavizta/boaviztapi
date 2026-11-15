# SDKs

Client libraries also exist for some languages. They are maintained by the community, not by Boavizta: report
bugs to their own repositories.

| Language | Library | Maintainer | Status |
|----------|---------|------------|--------|
| PHP | [boaviztapi-php](https://github.com/DavidJLN/boavizta-api-php) | [@DavidJLN](https://github.com/DavidJLN) | Community, unofficial |
| Python (MCP server) | [boaviztapi-mcp](https://github.com/malikmalikayesha/boaviztapi-mcp) | [@malikmalikayesha](https://github.com/malikmalikayesha) | Community, unofficial |

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

## MCP server (Python)

[boaviztapi-mcp](https://github.com/malikmalikayesha/boaviztapi-mcp) is a
[Model Context Protocol](https://modelcontextprotocol.io) server, so AI assistants (Claude, ChatGPT,
Cursor and other MCP clients) can query BoaviztAPI. It requires Python 3.10+ and runs with
[uv](https://docs.astral.sh/uv/):

```bash
uvx boaviztapi-mcp
```

To add it to an MCP client, for example Claude Desktop:

```json
{
  "mcpServers": {
    "boaviztapi": {"command": "uvx", "args": ["boaviztapi-mcp"]}
  }
}
```

It uses the public instance by default; set `BOAVIZTAPI_URL` to use your own. Asked "What is the
carbon footprint of 4 NVIDIA H100 SXM GPUs for one year in Germany?", the assistant calls
`/v1/component/gpu` and reports the embedded and use impacts with units, ranges and warnings.

See the [server's README](https://github.com/malikmalikayesha/boaviztapi-mcp#readme) for the tools
and configuration.

## Add your SDK

Open a pull request on [boaviztapi](https://github.com/Boavizta/boaviztapi) that adds a row to the
table above and to `SDKs.md` at the root of the repository.
