#!/usr/bin/python3
"""Class Declaration of FileStorage"""
from ast import literal_eval
import json


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return  dictionary objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set objects obj with key <obj_class_name>.id"""
        obj_class_name = obj.__class__.__name__
        new_var = "{}.{}"
        FileStorage.__objects[new_var.format(obj_class_name, obj.id)] = obj

    def save(self):
        """Serialization of  objects to the JSON file file_path."""
        obj_dict = FileStorage.__objects
        objdict = {obj: obj_dict[obj].to_dict() for obj in obj_dict.keys()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialization of JSON file file_path to objects, if it exists"""
        try:
            with open(FileStorage.__file_path, encoding="utf-8") as f:
                objdict = json.load(f)
                for ob in objdict.values():
                    class_name = ob["__class__"]
                    del ob["__class__"]
                    self.new(literal_eval(class_name)(**ob))
        except FileNotFoundError:
            return
