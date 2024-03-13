# IoT device routes

## POST ```/v1/user_terminal/<name>```

You can send an empty device. In this case, archetype's values will be used

``` json
{}
```

You can also describe an IoT device by its functional blocks 

``` json
{
    "functional_blocks":[
       {
        "type":"security", 
        "hsl_level":"HSL-1"
       },
       {
        "type":"user_interface", 
        "hsl_level":"HSL-2"
       }
     ]
}
```

## Usage

``` json
{
    "usage":{...}
}
```

See [usage](usage.md)