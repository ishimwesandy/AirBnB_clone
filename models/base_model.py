#!/usr/bin/python3
"""Class Declaration of BaseModel."""

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """Class attribute Declaration of the BaseModel on HBnB project."""

    def __init__(self, *args, **kwargs):
        """Variable Initialize a new BaseModel.

        Args:
            *args (any): Unused
            **kwargs (dict): Key pairs of attributes.
        """
        dtformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for ky, va in kwargs.items():
                if ky == "created_at" or ky == "updated_at":
                    self.__dict__[ky] = datetime.strptime(va, dtformat)
                else:
                    self.__dict__[ky] = va
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at attribute  with now  date"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance."""
        returned_dict = self.__dict__.copy()
        returned_dict["created_at"] = self.created_at.isoformat()
        returned_dict["updated_at"] = self.updated_at.isoformat()
        returned_dict["__class__"] = self.__class__.__name__
        return returned_dict

    def __str__(self):
        """Return the str representation of the BaseModel instances."""
        class_name = self.__class__.__name__
        new_var = "[{}] ({}) {}"
        return new_var.format(class_name, self.id, self.__dict__)
