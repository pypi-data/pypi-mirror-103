## GearScore python client

The package provides functionality to calculate GS for an item, with possibility to save items to local DB (sqlite).


### How to use
Create table before first package usage, it can be done with:
```python
from gear_score.db import ensure_tables_created

await ensure_tables_created()
```

After that, you can get info about a single item:
```python
from gear_score.getters import PublicDbGetter

getter = PublicDbGetter()
item = await getter.get(40633)
print(item.gs)

```

You can get info about multiple items at once, first checking in local db and then in public:
```python
from gear_score.utils import get_items_from_local_or_remote

items = await get_items_from_local_or_remote(50444, 50445, 50446)
```


TODO:
- tests
- proper documentation
- logging
- automatic db tables creation