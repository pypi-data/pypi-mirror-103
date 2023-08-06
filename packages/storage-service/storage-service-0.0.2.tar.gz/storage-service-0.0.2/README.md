# Storage Service

**Storage Service** is a Django + DRF package that help to work with model. 
Main advantage of this class is to provide **bulk** operations over the model data 
and upsert for single object with M2M relations. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install storage-service.

```bash
pip install storage_service
```

## Usage

```python
from storage_service.storage import StorageService

from blogs.helpers import BlogHelper  # optional
from blogs.serializers import BlogSerializer  # drf package


class BlogService(StorageService):
    def __init__(self):
        super().__init__()

        self.helper = BlogHelper  # optional

        self.model = BlogSerializer.Meta.model

        self.create_serializer_class = BlogSerializer
        self.get_serializer_class = BlogSerializer

        self.unique_identifier: str = 'pk'  # required unique model field
        self.unique_identifiers: list = []  # in case when you need more unique model fiedls
```

## Methods
* `def serialize(self, entities, many=False):` - helps deserialize list of objects to dict.


* `def get_next_id(self):` - returns next model primary key.


* `def get_by(self, key: str = '', value=None, serialize=True):` - helps to retrieve 
model data by provided **key** & **value** parameters. If **serialize** is set to `True` then 
method will return deserialized  model data. Otherwise will be returned object.


* `def get_pk(self, pk: int = 0, serialize=False):` - helps to retrieve 
model data by provided **pk** value. If **serialize** is set to `True` then 
method will return deserialized  model data. Otherwise will be returned object.


* `def delete_by(self, key: str = '', value=None):` - helps to delete 
model data by provided **key** & **value** parameters.


* `def set_identifiers(self, data)` - is helper method for bulk type & upsert methods.
Method to add identifiers as dict and to remove identifiers as default element.


* `def indexed(elements=None, index: int = 0, retrieve: bool = False):` - get and / or 
retrieve element at index.


* `def upsert(self, data, parameters=None, many_to_many_clear: bool = True):` - method 
to upsert a single object. Supporting M2M relations. Based on 
`self.unique_identifier` & `self.unique_identifiers`.


* `def bulk_upsert(self, data, parameters=None, many_to_many_clear: bool = True)` - method
to bulk upsert multiple objects. Supporting M2M relations. Based on 
`self.unique_identifier` & `self.unique_identifiers`.


* `def bulk_delete(self, data)` - method to bulk delete multiple objects.


* `def bulk_get_or_create(self, data):` - method to bulk get or create multiple objects.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)