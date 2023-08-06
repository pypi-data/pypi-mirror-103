OARepo rdm records model
====================
[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

Instalation
----------
```bash
    pip install oarepo-rdm-records
```
Usage
-----
The library provides a modified [InvenioRDMRecords](https://github.com/inveniosoftware/invenio-rdm-records.git) data
model for OARepo resource records. 

JSON Schema
----------
Add this package to your dependencies and use it via $ref in json
schema as ``"[server]/dataset-v2.0.0.json#/definitions/DataSet"``. 
Elastic Search mapping is handled automatically via Eleastic Search templates.

### Usage example
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "allOf": [
    {
      "$ref": "dataset-v2.0.0.json#/definitions/DataSet"
    }
  ]
}
```

```json
{
  "type": "object",
  "properties": {
    "these": {
        "titles" : {"cs": "neco", "en": "something"}
        }
  }
}
```

Modified fields of data model
-----------------------------
##### titles
- fully required oarepo multilingual data type
##### descriptions
- fully optional oarepo multilingual data type
##### subjects
- ```subject``` is required oarepo multilingual data type
##### locations
- ```description``` is optional oarepo multilingual data type
##### licenses
- ```license``` is required oarepo multilingual data type

 [image]: https://img.shields.io/travis/oarepo/oarepo-rdm-records.svg
  [1]: https://travis-ci.org/oarepo/oarepo-rdm-records
  [2]: https://img.shields.io/coveralls/oarepo/oarepo-rdm-records.svg
  [3]: https://coveralls.io/r/oarepo/oarepo-rdm-records
  [4]: https://img.shields.io/github/license/oarepo/oarepo-rdm-records.svg
  [5]: https://github.com/oarepo/oarepo-rdm-records/blob/master/LICENSE
  [6]: https://img.shields.io/pypi/v/oarepo-rdm-records.svg
  [7]: https://pypi.org/pypi/oarepo-rdm-records