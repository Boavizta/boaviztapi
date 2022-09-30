# Component route

Available components :

* cpu
* ram
* power-supply
* ssd
* hdd
* case
* motherboard
* assembly

## ```/v1/component/<component_name>```

You can send an empty component. In this case, only default values will be used

``` json
{}
```

You can set a units. If so, all the impacts will be multiplied by the number of units.

``` json
{
    "units": 2
}
```

### ```/v1/component/cpu```

*All needed information are sent*
``` json
{
   "core_units": 24,
   "die_size_per_core": 0.245
}
```

*Incomplete CPU, die-size will be retrieved with the cpu family and core_units*
``` json
{
   "core_units": 24,
   "family": "Skylake",
}
```

*Incomplete CPU, family will be retrieved from cpu name, die-size will be retrieved with the cpu family and core_units*
``` json
{
   "core_units": 24,
   "name": "Intel Xeon Gold 6138f",
}
```

## ```/v1/component/ssd```

``` json
{
    "capacity": 400,
    "density": 50.6
}
```
*All needed information are sent*

``` json
{
   "capacity": 500,
   "manufacturer": "Samsung",
}
```
*Incomplete SSD, die-size will be retrieved with the manufacturer name*


## ```/v1/component/ram```

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
    "manufacturer": "Samsung",
    "process": 30.0
}
```
*Incomplete RAM, die-size will be retrieved with the manufacturer name and the process*


## ```/v1/component/hdd```

``` json
{}
```
*HDD impacts have a default value*


## ```/v1/component/motherboard```

``` json
{}
```
*motherboard impacts have a default value*


## ```/v1/component/power_supply```

``` json
{
    "unit_weight": 10
}
```
*All needed information are sent*

## ```/v1/component/case```

``` json
{
  "case_type": "rack"
}
```
*rack impacts have a default value*

``` json
{
  "case_type": "blade"
}
```
*blade impacts have a default value*

``` json
{}
```
*case_type will be set to rack by default*

## Usage

### Given

See [usage](usage.md)

### Modeled

#### ```/v1/component/cpu```

See [usage](usage.md)

#### ```/v1/component/ram```

See [usage](usage.md)