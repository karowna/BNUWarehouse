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

To format the code nicely use (in root)
```
black .
```