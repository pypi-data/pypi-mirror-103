# tidytuesdayPy

Download TidyTuesday data.  Inspired by [tidytuesdayR](https://github.com/thebioengineer/tidytuesdayR).

## Usage

```python
from tidytuesday import TidyTuesday

tt = TidyTuesday("2021-04-06")
```

If you do not provide a date (*i.e.* just `TidyTuesday()`), then the latest TidyTuesday will be used.  Note that this will not be good for reproducability in the future!

You can then access each data set from the data field using the filename, dropping the extension.

```python
df = tt.data["forest"]
```

You can also access the readme.

```python
print(tt.readme)
```

## TODO

- Implement parsers for rds formats
- Documentation
