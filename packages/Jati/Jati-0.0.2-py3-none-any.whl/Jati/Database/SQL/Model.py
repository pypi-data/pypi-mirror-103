import datetime

class ListOfModels():
    def __init__(self, models = []):
        self.models = models
    def append(self, model):
        self.models.append(model)
    def __len__(self):
        if type(self.models) in [list, dict]:
            return len(self.models)
        return 0
    def __setitem__(self, i, val):
        self.models[i] = val
    def __getitem__(self, table):
        return self.models[table]

class ModelsAsObject(object):
    def __init__(self, obj_class, key, models = [], parent = None, on = {}):
        self.__attributtes = {}
        self.__obj_class = obj_class
        self.__key = key
        self.__parent = parent
        self.__on = on
        for m in models:
            self.__attributtes[getattr(m, key)] = m
    def __getitem__(self, name):
        if not name in self.__attributtes:
            args = {self.__key: name}
            for key in self.__on.keys():
                if self.__parent is not None:
                    args[self.__on[key]] = getattr(self.__parent, key)
            self.__attributtes[name] = self.__obj_class.create(**args)
        return self.__attributtes[name]
    def save(self):
        for key in self.__attributtes.keys():
            self.__attributtes[key].save()

class ModelIterator:
    def __init__(self, model_class, query):
        self.model_class = model_class
        self.query = query
        self.result = None
        self.i = -1

    def limit(self, num, offset = 0):
        self.query = self.query.select(
            asDictionary = True,
            limit = (offset, num),
            isExecute = False
        )
        return self

    def page(self, num, limit = 20):
        offset = limit*(num-1)
        self.query = self.query.select(
            asDictionary = True,
            limit = (offset, limit),
            isExecute = False
        )
        return self

    def __iter__(self):
        self.result = self.query.getResult()
        return self

    def __next__(self):
        if self.result:
            data = self.result.__next__()
            if data:
                return self.model_class.createFromDict(data, False)
        raise StopIteration

class Model(object):
    DB = None
    TABLE = None
    PRIMARY_KEY = 'id'
    WHERE = {}
    Databases = {}
    Log = None

    def __init__(self, *arg, **kw):
        self.__id = None
        self.__updated__attr = {}
        self.__attributtes = self._attributtes()
        self.__relations = {}
        self.__generate__attrs()

        for key in kw.keys():
            setattr(self, key, kw[key])

    @classmethod
    def create(this_class, *arg, **kw):
        model = this_class(*arg, **kw)
        return model

    @classmethod
    def createFromDict(this_class, args, is_new = True):
        model = this_class(**args)
        if not is_new:
            model.__updated__attr = {}
            if this_class.PRIMARY_KEY in args.keys():
                model.__id = args[this_class.PRIMARY_KEY]
        return model

    @classmethod
    def one(this_class, *arg, **args):
        db = this_class.Databases[this_class.DB]
        _where = []
        for key in args.keys():
            _where.append((key, args[key], ))
        for key in this_class.WHERE.keys():
            _where.append((key, this_class.WHERE[key], ))
        results = db[this_class.TABLE].select(
            where=_where, 
            limit=1
        )
        model = None
        if results:
            for r in results:
                model = this_class.createFromDict(r, False)
        return model

    @classmethod
    def all(this_class):
        db = this_class.Databases[this_class.DB]
        _where = []
        for key in this_class.WHERE.keys():
            _where.append((key, this_class.WHERE[key], ))
        query = db[this_class.TABLE].select(
            where = _where,
            isExecute = False
        )
        return ModelIterator(this_class, query)
        
    @classmethod
    def search(this_class, *arg, **args):
        db = this_class.Databases[this_class.DB]
        _where = []
        for key in args.keys():
            _where.append((key, args[key], ))
        for key in this_class.WHERE.keys():
            _where.append((key, this_class.WHERE[key], ))
        query = db[this_class.TABLE].select(
            where = _where,
            isExecute = False
        )
        return ModelIterator(this_class, query)
    
    def _attributtes(self):
        return {}

    def __setattr__(self, name, value):
        if name in self.WHERE:
            value = self.WHERE[name]
        if (hasattr(self, "_Model__attributtes") 
         and name in self.__attributtes 
         and "datatype" in self.__attributtes[name]
        ):
            datatype = self.__attributtes[name]["datatype"]
            new_value = None
            if value is None:
                new_value = value
            elif datatype == 'int':
                new_value = int(value)
            elif datatype == 'float':
                new_value = float(value)
            elif datatype == 'str':
                new_value = str(value)
            elif datatype == 'date':
                if type(value) is str:
                    tmp_val = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                elif type(value) is int:
                    tmp_val = datetime.date.fromtimestamp(value)
                elif type(value) is datetime.date:
                    tmp_val = value
                else:
                    tmp_val = None
                new_value = tmp_val
            elif datatype == 'list':
                new_value = value
            elif datatype == 'dict':
                new_value = value
            elif datatype == 'relation_has_one':
                new_value = value
            elif datatype == 'relation_has_many':
                new_value = value
            if datatype not in ['relation_has_one', 'relation_has_many', 'relation_as_object']:
                self.__updated__attr[name] = new_value
            return object.__setattr__(self, name, new_value)
        return object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        if (name != '_Model__attributtes'
         and hasattr(self, "_Model__attributtes") 
         and name in self.__attributtes 
         and "datatype" in self.__attributtes[name]
        ):
            datatype = self.__attributtes[name]["datatype"]
            if datatype == 'relation_has_one':
                if object.__getattribute__(self, name) == None:
                    _on = self.__attributtes[name]["on"]
                    _class_model = self.__attributtes[name]["class_model"]
                    _where = {}
                    for key in _on.keys():
                        _where[_on[key]] = self.__getattribute__(key)
                    model = _class_model.one(**_where)
                    object.__setattr__(self, name, model)
            elif datatype == 'relation_has_many':
                if object.__getattribute__(self, name) == None:
                    _on = self.__attributtes[name]["on"]
                    _class_model = self.__attributtes[name]["class_model"]
                    _where = {}
                    for key in _on.keys():
                        _where[key] = self.__getattribute__(_on[key])
                    models = _class_model.search(**_where)
                    object.__setattr__(self, name, models)
            elif datatype == 'relation_as_object':
                if object.__getattribute__(self, name) == None:
                    _on = self.__attributtes[name]["on"]
                    _key = self.__attributtes[name]["key"]
                    _class_model = self.__attributtes[name]["class_model"]
                    _where = {}
                    for key in _on.keys():
                        _where[_on[key]] = self.__id
                    models = _class_model.search(**_where)
                    object.__setattr__(self, name, ModelsAsObject(_class_model, _key, models, 
                            parent=self, 
                            on=_on
                        )
                    )
        return object.__getattribute__(self, name)

    def __generate__attrs(self):
        _attrs = self.__attributtes
        if self.PRIMARY_KEY in _attrs.keys():
            _attrs[self.PRIMARY_KEY]['primary'] = True
        for _key in _attrs.keys():
            if _attrs[_key]["datatype"] == 'relation':
                self.__relations[_key] = {
                    "class_model":_attrs[_key]["class_model"],
                    "data": []
                }
            setattr(self, _key, _attrs[_key]["default"] if "default" in _attrs[_key] else None)
            
    def save(self):
        db = self.Databases[self.DB][self.TABLE]
        if not self.__updated__attr: return False
        if self.__id is None:
            result = db.insert(self.__updated__attr)
            if result is not None:
                self.__id = result.lastid
                self.__setattr__(self.PRIMARY_KEY, self.__id)
                return (result.error is None)
        else:
            result = db.update(self.__updated__attr,
                where=[(self.PRIMARY_KEY, self.__id)]
            )
            return (result.error is None)
    
    def delete(self):
        db = self.Databases[self.DB][self.TABLE]
        if self.__id is not None:
            result = db.delete(where=[(self.PRIMARY_KEY, self.__id)])
            if result is not None:
                return True

    @staticmethod
    def _integer(default = 0):
        return {
            "datatype" : "int",
            "default": int(default)
        }

    @staticmethod
    def _float(default = 0.0):
        return {
            "datatype" : "float",
            "default": float(default)
        }

    @staticmethod
    def _string(default = None):
        return {
            "datatype" : "str",
            "default": str(default) if default else None
        }

    @staticmethod
    def _date(default = None):
        return {
            "datatype" : "date",
            "default": default
        }

    @staticmethod
    def _time(default = None):
        return {
            "datatype" : "time",
            "default": default
        }

    @staticmethod
    def _datetime(default = None):
        return {
            "datatype" : "datetime",
            "default": default
        }

    @staticmethod
    def _array(default = []):
        return {
            "datatype" : "list",
            "default": default
        }

    @staticmethod
    def _object(default = {}):
        return {
            "datatype" : "dict",
            "default": default
        }

    @staticmethod
    def _hasOne(class_model, on = {}):
        return {
            "datatype" : "relation_has_one",
            "class_model" : class_model,
            "on" : on,
            "default": None
        }
    
    @staticmethod
    def _hasMany(class_model, on = {}):
        return {
            "datatype" : "relation_has_many",
            "class_model" : class_model,
            "on" : on,
            "default": None
        }
    
    @staticmethod
    def _hasObject(class_model, on = {}, key="key"):
        return {
            "datatype" : "relation_as_object",
            "class_model" : class_model,
            "on" : on,
            "key" : key,
            "default": None
        }
    