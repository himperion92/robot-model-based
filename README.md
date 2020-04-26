# robot-model-based
Robot Framework integrated solution for Model Based Testing using graphical test sequence design.

## Key Concepts

### yED
Graph editor tool. Graphs can be exported in .graphml format that will be used as an input of graphwalker-based tools. [https://www.yworks.com/products/yed](https://www.yworks.com/products/yed)

### Robot Framework
Generic Python-native test automation tool. [https://robotframework.org/](https://robotframework.org/)

## Examples

_Example for `robot_model_based`_:

_1.  Full test coverage:_
```
python -m robot_model_based_cli -g <path_to_project>/demo/models/coffee_machine_system.graphml -s full -t "Coffee System" -l "CoffeeMachineExtendedLibrary" -r reports
```

_2.  Randomized 50% coverage:_
```
python -m robot_model_based_cli -g <path_to_project>/demo/models/coffee_machine_system.graphml -s random -c 50 -t "Coffee System" -l "CoffeeMachineExtendedLibrary" -r reports
```

## Constraints
* Current version of `robot_model_based` does not support Guards (conditions) within the edges, it does support Actions 
(arguments) tho. Nodes cannot contain neither Actions or Guards.
* Current version of `robot_model_based` does not support test case documentation generation.
* Current version of `robot_model_based` does not support specific path configuration.


