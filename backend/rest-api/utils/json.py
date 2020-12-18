import inspect
import types
import json
import datetime
from utils.parses import parse_datetime_to_date_time_str
from enum import Enum


class EnumConversibleToJson(str, Enum):
    def __str__(self):
        return str(self.value)


class ComplexObjectToJsonEntityMixin():
    def _is_instance_of_a_class(self, obj):
        if not hasattr(obj, '__dict__'):
            return False
        if inspect.isroutine(obj):
            return False
        else:
            return True

    def to_dict(self, ignore_type = None):
        obj_dict = {}
        class_dictionary = self.__dict__
        attrs = self.__dict__.keys()
        attrs_filtered = self._filter_attrs_to_convert_to_dict(attrs)
        type_of_object_converted = self.__class__
        
        for attr in attrs_filtered:
            obj_to_convert = class_dictionary.get(attr)

            if isinstance(obj_to_convert, list):
                obj_dict[attr] = self._convert_list_to_dict(
                    obj_dict, attr, obj_to_convert, type_of_object_converted)

            elif isinstance(obj_to_convert, Enum):
                obj_dict[attr] = str(obj_to_convert)

            elif isinstance(obj_to_convert, datetime.datetime):
                obj_dict[attr] = parse_datetime_to_date_time_str(obj_to_convert)
            
            elif ignore_type is not None:
                if not isinstance(obj_to_convert, ignore_type):
                    obj_dict[attr] = self._convert_to_dict(obj_to_convert, obj_dict, attr, ignore_type)

            else:
                obj_dict[attr] = self._convert_to_dict(obj_to_convert, obj_dict, attr)

        return obj_dict

    def _filter_attrs_to_convert_to_dict(self, attrs):
        attrs = sorted(attrs, key=lambda i: (i))
        return [attr for attr in attrs if attr != '_sa_instance_state']

    def _convert_list_to_dict(self, obj_dict, attr, obj_to_convert, type_to_not_convert):
        list_converted = []
        
        for item in obj_to_convert:
            if not isinstance(item, type_to_not_convert):
                list_converted.append(self._convert_to_dict(
                    item, obj_dict, attr, type_to_not_convert))

        return list_converted

    def _convert_to_dict(self, obj_to_convert, obj_dict, attr, ignore_type = None):
        if isinstance(obj_to_convert, ComplexObjectToJsonEntityMixin):
            return obj_to_convert.to_dict(ignore_type)

        elif self._is_instance_of_a_class(obj_to_convert):
            return obj_to_convert.__dict__

        else:
            return obj_to_convert
