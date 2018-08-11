# Python utilities
Helper utility code

## 1. file_util.py
Helper utilities to abstract away File IO.

## 2. config_reader.py
ConfigReader to read config files and return a dict with the content of those files
Standard syntax for config files is lines of key = values, comments are accepted with #


Example test_config.txt:
```
test_1 = value 1
test_2 = 14.5 # comment 1
# comment 2
test_3 = True
```


Example Usage:

```
config = ConfigReader('/path/to/test_config.txt')
a = config.test_1
b = config.test_2
c = config.test_3
```