# Marshmallow Mongoengine Query Schema
## _Mongoengine filters in your API with no effort!_

A marshmallow schema for use in url query which checks for possible mongoengine [query filters](https://docs.mongoengine.org/guide/querying.html) (as well as `only` and `order_by` args)
and converts their types based on requirements for filters (eg. ints for number comparition operators)
and fields themselves (eg. list inner type when using for example `list__0`)

Supports all mongoengine filters except [geo queries](https://docs.mongoengine.org/guide/querying.html#geo-queries)

> *Note: This has nothing to do with [marshmallow-mongoengine](https://pypi.org/project/marshmallow-mongoengine/), I just couldn't think of better name*

### Usage:
```py
from marshmallow_mongoengine_query_schema import QuerySchema


class SomeQuerySchema(QuerySchema):
    __query_fields__ = SomeSchema().declared_fields
    class Meta:  # optional settings
        query_enable_filters = False
        query_enable_only = True
        query_enable_order_by = False
        query_allowed_infixes = ['__']
```

### Usage in url:
```
example.com/someendpoint?no_comments=5&name__startswith=b&list__size=2&list__0=somestring
```
Every type is converted automatically but there's couple of things to point out:
> When list type is needed, comma delimited list is used in url: `?list=a,b,c,d`

> `match` operator and `__raw__` are expecting a dictionary(json): `?__raw__={"name": "hello"}`

### Installation
Very complicated black magic stuff:
```sh
pip3 install marshmallow_mongoengine_query_schema
```

### License

MIT
