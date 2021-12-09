# Component route

## Minimum server input

You can send an empty component :

```/v1/component/<component_name>```

``` json
{}
```

In this case, only default value are used.

*Components have no units since they represent a single instance of a component.*

## CPU

```/v1/component/cpu```

``` json
{
   "core_units": 24,
   "die_size_per_core": 0.245
}
```
*All needed information are sent*

``` json
{
   "core_units": 24,
   "family": "Skylake",
   "manufacture_date": 2017
}
```
*Incomplete CPU, die-size will be retreive with the cpu family and manufacture date*


## SSD

```/v1/component/ssd```

``` json
{
    "capacity": 400,
    "density": 50.6
}
```
*All needed information are sent*

``` json
{
   "core_units": 24,
   "manufacturer": "Samsung",
}
```
*Incomplete SSD, die-size will be retrieved with the manufacturer name*


## RAM

```/v1/component/ssd```

``` json
{
    "capacity": 32,
    "density": 1.79
}
```
*All needed information are sent*

``` json
{           
    "capacity": 32,
    "manufacturer": "Samsung"
    "process": 30.0
}
```
*Incomplete RAM, die-size will be retrieved with the manufacturer name and the process*


## HDD

```/v1/component/hdd```

``` json
{}
```
*HDD impacts have a default value*


## Motherboard

```/v1/component/motherboard```

``` json
{}
```
*motherboard impacts have a default value*


## Power supply

```/v1/component/power_supply```

``` json
{
    "unit_weight": 10
}
```
*All needed information are sent*


## rack

```/v1/component/rack```

``` json
{}
```
*rack impacts have a default value*


## blade

```/v1/component/blade```

``` json
{}
```
*blade impacts have a default value*

