# Smart complete

The API should always send back an impact independently on the completeness of the descriptive data of a component.
If a needed data is not given, the system complete it with the closest component data found in the database or by a default value. 
When several component correspond the maximum impact is given.


```
IF component IS complete
    MEASURE with the data sent
ELSE IF FIND(component) == 0
    MEASURE with default data (max)
ELSE IF FIND(component) == 1
    MEASURE with the found component
ELSE IF FIND(component) > 1
    MEASURE with found component with the maximum impact
```