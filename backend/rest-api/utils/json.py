import inspect
import types
import json

class ComplexObjectToJsonEntityMixin():
    def is_instance(self, obj):
        if not hasattr(obj, '__dict__'):
            return False
        if inspect.isroutine(obj):
            return False
        else:
            return True

    def to_dict(self):
        class_dictionary = self.__dict__
        attrs = self.__dict__.keys()
        obj_dict = {}
        attrs_filtered = [
            attr for attr in attrs if attr != '_sa_instance_state']

        for attr in attrs_filtered:
            obj_to_convert = class_dictionary.get(attr)

            if isinstance(obj_to_convert, ComplexObjectToJsonEntityMixin):
                obj_dict[attr] = obj_to_convert.to_dict()
            elif self.is_instance(obj_to_convert):
                obj_dict[attr] = obj_to_convert.__dict__
            else:
                obj_dict[attr] = obj_to_convert

        return obj_dict
