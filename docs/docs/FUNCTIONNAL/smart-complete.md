# Smart complete

The API should always send back an impact independently on the completeness of the descriptive data of a component.
If a needed data is not given, the system complete it with the closest component data found in the database or by a default value. 
When several component correspond the maximum impact is given.



### Process

The user send data concerning the server components.

Matching components are found by the characteristics send by the user. ```FIND()```

Default data are always the maximizing data (in terms of impacts)


```
FOREACH COMPONENTS
   IF component IS complete
       DO NOTHING
   ELSE IF FIND(component) == 0
       USE DEFAULT DATA 
   ELSE IF FIND(component) == 1
      USE FOUND COMPONENT
   ELSE IF FIND(component) > 1
       USE FOUND MAXIMIZING COMPONENT
```