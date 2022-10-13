# Duration

Usage impacts are measured for a specific time duration given by the user.
The API handles three different time units :

| time unit |
|-----------|
| HOURS     |
| DAYS      |
| YEARS     |

When duration is not given, the impact is measured for the default duration. Typically, 1 hour.
_Note: units are cumulative, if multiple units are used, they are summed up._

## Example

```
HOURS = 1
DAYS = 1
YEARS =  1
```

will be converted in **8785** hours (`1+1*24+1*24*365`).