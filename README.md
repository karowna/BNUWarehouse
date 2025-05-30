# BNUWarehouse
An application of OOP principles, displayed in the from of a warehouse management system. A combination of the principles learnt from classroom sessions and of personal learnings to get a grip of how OOP works in Python.

Use for opening the program
```
python3 -m tui.main.py
```

Use for opening the program with mock data entered already

```
python3 -m tui.main.py --mock
```

Use for running unit tests
```
coverage run -m unittest discover && coverage report && coverage html
```

Use for running unit tests and running the program
```
coverage run -m unittest discover && coverage report && coverage html | python3 -m tui.main.py
```

To format the code nicely use
```
black .
```

