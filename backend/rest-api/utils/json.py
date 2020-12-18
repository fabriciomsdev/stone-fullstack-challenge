import inspect
import types
import json


def my_decorator(func):
    def wrapper():
        func()
    return wrapper

class ComplexObjectToJsonEntityMixin():
    def is_instance(self, obj):
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

            elif ignore_type is not None:
                if not isinstance(obj_to_convert, ignore_type):
                    obj_dict[attr] = self._convert_to_dict(obj_to_convert, obj_dict, attr, ignore_type)

            else:
                obj_dict[attr] = self._convert_to_dict(obj_to_convert, obj_dict, attr)

        return obj_dict

    def _filter_attrs_to_convert_to_dict(self, attrs):
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

        elif self.is_instance(obj_to_convert):
            return obj_to_convert.__dict__
            
        else:
            return obj_to_convert
