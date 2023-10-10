# End user device routes

Available device :

* laptop      
* desktop     
* monitor     
* smartphone  
* tablet      
* television  
* box         
* usb_stick   
* external_ssd
* external_hdd

## POST ```/v1/user_terminal/<name>```

You can send an empty device. In this case, archetype's values will be used

``` json
{}
```

For some devices, you can set a type. See [end user device](../../Explanations/devices/terminals_&_peripherals.md) for more information about types.

``` json
{
    "type": 2
}
```


## Usage

``` json
{
    "usage":{...}
}
```

See [usage](usage.md)