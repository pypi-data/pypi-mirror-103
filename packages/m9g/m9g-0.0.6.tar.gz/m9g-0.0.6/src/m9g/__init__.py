# ~ coding: future_fstrings ~

from __future__ import absolute_import, unicode_literals

__version__ = "0.0.6"

from future.utils import with_metaclass, iteritems
from future.builtins import filter

import sys
import json
import pickle

from .exceptions import ValidationError
from .fields import *  # noqa


def _new_class_with_kwargs(cls, **kwargs):
    obj = cls.__new__(cls)
    for attr, attr_value in iteritems(kwargs):
        setattr(obj, attr, attr_value)
    return obj


def _get_parents_fields(parents):
    fields = {}

    for parent in parents:
        if hasattr(parent, "_fields"):
            parent_fields = dict(parent._fields)
            fields.update(parent_fields)

    return fields


class MetaModel(type):
    _models_registry = {}

    def _add_to_model_registry(cls):
        model_module, model_name = cls.module_and_classname()
        cls._models_registry[(model_module, model_name)] = cls

    def __init__(cls, class_name, parents, attrs):
        m_parents = filter(lambda p: isinstance(p, MetaModel), parents)

        if len(list(m_parents)) > 1:
            raise ValidationError(f"{cls.__name__} must only have one MetaModel parent")

        fields = _get_parents_fields(parents)

        fields_declared_as_pk = []

        for attr_k, attr_v in iteritems(attrs):
            if isinstance(attr_v, Field):  # noqa: F405
                fields[attr_k] = attr_v
                delattr(cls, attr_k)
                if attr_v.pk:
                    fields_declared_as_pk.append(attr_k)
        cls._fields = fields

        declared_pk = getattr(cls, "primary_key_fields", None)

        if declared_pk and not set(declared_pk).issubset(cls._fields):
            raise ValidationError(f"{declared_pk} is not part of declared fields")

        if len(fields_declared_as_pk) > 1:
            raise ValidationError(
                f"Multiple fields declared as primary key, got: {len(fields_declared_as_pk)}"
            )

        if len(fields_declared_as_pk) and declared_pk:
            raise ValidationError("Both fields declared as primary key and defined primary_key attr")

        field_pk = None
        if len(fields_declared_as_pk) == 1:
            field_pk = fields_declared_as_pk.pop()

        if not declared_pk:
            cls.primary_key_fields = field_pk and tuple([field_pk])

        cls._add_to_model_registry()

    @classmethod
    def get_all_models(cls):
        return cls._models_registry

    @classmethod
    def get_model(cls, module, name):
        return cls._models_registry[(module, name)]


class Model(with_metaclass(MetaModel)):
    polymorphic_base = False

    def __init__(self, **kwargs):
        received_fields = set()
        for k, v in kwargs.items():
            if k not in self._fields:
                raise ValidationError(f"'{k}' is not part of declared fields")
            setattr(self, k, v)
            received_fields.add(k)

        # seteamos a default los campos que no nos definieron
        for missing_field in set(self._fields).difference(received_fields):
            default_missing_field = self._fields[missing_field].get_default()
            if default_missing_field is missing or (
                    default_missing_field is None and not self._fields[missing_field].allow_none
            ):
                raise ValidationError(f"'{missing_field}' is missing or None and it's required")
            setattr(self, missing_field, default_missing_field)

    @classmethod
    def module_and_classname(cls):
        model_module = getattr(cls, "model_module", None)
        if model_module is None:
            class_module = sys.modules.get(cls.__module__, None)
            if class_module and hasattr(class_module, "m9g_module"):
                model_module = class_module.m9g_module
            else:
                model_module = cls.__module__
        model_name = getattr(cls, "model_name", cls.__name__)
        return model_module, model_name

    @classmethod
    def modelfullname(cls):
        model_module, model_name = cls.module_and_classname()
        return f"{model_module}.{model_name}"

    def __getattr__(self, attr_name):
        if attr_name not in self._fields.keys():
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{attr_name}'")
        if self._ref_status == "lazy":
            obj = self.manager.findByPrimaryKey(self.pk)
            self._full_obj = obj
            self._ref_status = "loaded"
            return getattr(obj, attr_name)
        elif self._ref_status == "loaded":
            return getattr(self._full_obj, attr_name)

    def __setattr__(self, attr_name, attr_value):
        if attr_name not in self._fields:
            return super().__setattr__(attr_name, attr_value)
        if getattr(self, "_ref_status", None) == "loaded":
            return self._full_obj.__setattr__(attr_name, attr_value)
        elif getattr(self, "_ref_status", None) == "lazy":
            obj = self.manager.findByPrimaryKey(self.pk)
            self._full_obj = obj
            self._ref_status = "loaded"
            return self._full_obj.__setattr__(attr_name, attr_value)

        attr_value = self._fields[attr_name].adapt(attr_value)
        self._fields[attr_name].validate(attr_value)
        super().__setattr__(attr_name, attr_value)

    def _resolve_pk_values(self):
        """ Obtiene los valores de las claves primarias """
        return [getattr(self, attr_name) for attr_name in self.primary_key_fields if self.primary_key_fields]

    def _serialize(self, format):
        """ Serialización completa, con todos los atributos """

        data = {}
        format = self._model_format_to_field_format(format)
        for k, v in iteritems(self._fields):
            value = getattr(self, k)
            data[k] = v.serialize(format, value)

        if self.polymorphic_base:
            data["__modelclass__"] = self.modelfullname()

        return data

    @classmethod
    def _model_format_to_field_format(cls, format):
        if format == "jsondict":
            return "json"
        return format

    @classmethod
    def _deserialize(cls, data, format):
        modelclass = data.pop("__modelclass__", None)
        if modelclass:
            model_module, model_class = modelclass.rsplit(".", 1)
            subclass = MetaModel.get_model(model_module, model_class)
            return subclass._deserialize(data, format)

        return _new_class_with_kwargs(cls, **cls._deserialize_fields(data, format))

    def _in_place_deserialize(self, data, format):
        new_fields = self._deserialize_fields(data, format)
        for k, v in new_fields.items():
            setattr(self, k, v)

    @classmethod
    def _deserialize_fields(cls, data, format):
        """Full deserialization - expects all the fields"""
        kwattrs = {}
        format = cls._model_format_to_field_format(format)
        for attr_name, serialized_attr_value in iteritems(data):
            if attr_name not in cls._fields.keys():
                # TODO: ver qué pasa si nos "sobran" atributos en data - WARNING o ERROR?
                pass

            associated_field = cls._fields[attr_name]
            attr_value = associated_field.deserialize(format, serialized_attr_value)
            kwattrs[attr_name] = attr_value

        return kwattrs

    @property
    def pk(self):
        pk_values = self._resolve_pk_values()
        if len(pk_values) == 1:
            return pk_values[0]
        return tuple(pk_values)

    def available_fields(self):
        """ Returns dictionary with <field_type>: <field_value> for fields available in the
            gross or thin ref """
        return dict((field_name, field_value) for field_name, field_value in self.__dict__.items()
                    if field_name in self._fields)

    @classmethod
    def field_from_key(cls, field_key):
        return cls._fields[field_key]

    @classmethod
    def get_manager(cls):
        return cls.manager

    def serialize(self, format="json"):
        serialize_method = getattr(self, f"serialize_{format}")
        return serialize_method()

    def serialize_json(self):
        """Serializes as JSON string"""
        return json.dumps(self.serialize_jsondict())

    def serialize_jsondict(self):
        """Serializes as JSON-serializable python dictionary"""
        return self._serialize("jsondict")

    def serialize_pickle(self):
        serialized_data = self._serialize("pickle")
        return pickle.dumps(serialized_data)

    def serialize_pydict(self):
        return self._serialize("pydict")

    @classmethod
    def deserialize(cls, str_obj, format="json"):
        deserialize_method = getattr(cls, f"deserialize_{format}")
        return deserialize_method(str_obj)

    def in_place_deserialize(self, str_obj, format="json"):
        deserialize_method = getattr(self, f"in_place_deserialize_{format}")
        return deserialize_method(str_obj)

    def in_place_deserialize_json(self, str_obj):
        data = json.loads(str_obj)
        return self.in_place_deserialize_jsondict(data)

    def in_place_deserialize_jsondict(self, obj):
        return self._in_place_deserialize(obj, "jsondict")

    def in_place_deserialize_pickle(self, str_obj):
        data = pickle.loads(str_obj)
        return self._in_place_deserialize(data, "pickle")

    def in_place_deserialize_pydict(self, pydict):
        return self._in_place_deserialize(pydict, "pydict")

    @classmethod
    def deserialize_json(cls, str_obj):
        data = json.loads(str_obj)
        return cls.deserialize_jsondict(data)

    @classmethod
    def deserialize_jsondict(cls, obj):
        return cls._deserialize(obj, "jsondict")

    @classmethod
    def deserialize_pickle(cls, str_obj):
        data = pickle.loads(str_obj)
        return cls._deserialize(data, "pickle")

    @classmethod
    def deserialize_pydict(cls, pydict):
        return cls._deserialize(pydict, "pydict")

    @classmethod
    def fromdb(cls, **kwargs):
        if set(kwargs) != set(cls._fields):
            raise ValidationError("Faltan")

        obj = _new_class_with_kwargs(cls, **kwargs)
        # TODO: marca de readonly?
        return obj

    @classmethod
    def thinRef(cls, **kwargs):
        if set(kwargs) != set(cls.primary_key_fields):
            raise ValidationError(f"{cls.__name__}.thinRef must receive only primary key fields")

        obj = _new_class_with_kwargs(cls, **kwargs)
        obj._ref_status = "lazy"
        return obj

    @classmethod
    def grossRef(cls, **kwargs):
        received_fields = set(kwargs)
        if not received_fields.issuperset(set(cls.primary_key_fields)):
            raise ValidationError(f"{cls.__name__}.grossRef must receive at least primary keys")
        if not set(cls._fields).issuperset(received_fields):
            unknown_fields = received_fields - set(cls._fields)
            raise ValidationError(f"{cls.__name__}.grossRef received unknown_fields: {unknown_fields}")

        obj = _new_class_with_kwargs(cls, **kwargs)
        obj._ref_status = "lazy"
        return obj

    def is_lazy(self):
        return hasattr(self, "_ref_status") and self._ref_status == "lazy"
