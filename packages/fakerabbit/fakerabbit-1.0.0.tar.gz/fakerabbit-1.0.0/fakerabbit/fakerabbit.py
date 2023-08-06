import datetime
import random
import string
import typing
from typing import List

from sqlalchemy import Integer, String, DateTime, LargeBinary, inspect, Boolean, Column, Numeric
from sqlalchemy.ext.declarative import DeclarativeMeta

T = typing.TypeVar("T")


class FakeRabbit:
    """A simple lib to make fake objects using SQLAlchemy"""

    def __init__(self, base_model_class: DeclarativeMeta, db_session):
        self.base_model_class = base_model_class
        self.db_session = db_session

    # Factory
    def make(self, cls, unities: int = 1, recursive_mode=False, **kwargs):

        attr_names = self.get_model_class_attribute_names(cls)

        def make_obj():
            obj = cls(**kwargs)

            for column in attr_names:

                column = column.columns[0]

                if column.key in kwargs.keys():
                    continue

                if column.primary_key:
                    continue

                if column.foreign_keys:

                    if not recursive_mode:
                        continue

                    foreign_cls = self.get_foreign_key_class_by_column(column)

                    if not isinstance(obj, foreign_cls):
                        foreign_obj = self.make(foreign_cls)

                        foreign_primary_key = inspect(foreign_obj).identity[0]
                        setattr(obj, column.key, foreign_primary_key)
                else:

                    # Getting a fake value by class type, ex: Integer = 3
                    fake_value = self.alchemy_type_generator(column.type.__class__)
                    setattr(obj, column.key, fake_value)

            self.db_session.add(obj)
            self.db_session.commit()

            return obj

        if unities > 1:
            return [make_obj() for _ in range(unities)]

        return make_obj()

    ##########################
    # SQLAlchemy extra methods
    ##########################
    @staticmethod
    def get_all_model_classes(base_model_class: DeclarativeMeta,
                              ) -> List[DeclarativeMeta]:

        # Get SQLAlchemy Class Registry
        # List of all model classes from SQLAlchemy
        model_classes = [mapper.class_
                         for mapper in base_model_class._sa_registry.mappers]

        return model_classes

    @staticmethod
    def get_model_class_attribute_names(cls: T):

        inst = inspect(cls)
        attr_names = [c_attr for c_attr in inst.mapper.column_attrs]

        return attr_names

    def get_foreign_key_class_by_column(self, column: Column) -> typing.Optional[DeclarativeMeta]:
        model_classes = self.get_all_model_classes(self.base_model_class)

        table = list(column.foreign_keys)[0].column.table
        # classes = [c for c in model_classes if c.__table__ == table]
        classes = filter(lambda c: c.__table__ == table, model_classes)

        for cls in classes:
            return cls

    #################
    # Fake generators
    #################
    @staticmethod
    def random_int():
        return random.randint(1, 9999)

    @staticmethod
    def random_str(length=10):
        fake_string = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        return fake_string

    @staticmethod
    def random_datetime():
        return datetime.datetime.now()

    @staticmethod
    def random_largebinary():
        return bytes(2020)

    @staticmethod
    def random_boolean():
        return random.choice([True, False])

    @staticmethod
    def random_numeric():
        return random.randint(1, 9999)

    def alchemy_type_generator(self, class_type: T):

        alchemy_types = {
            Integer: self.random_int,
            String: self.random_str,
            DateTime: self.random_datetime,
            LargeBinary: self.random_largebinary,
            Boolean: self.random_boolean,
            Numeric: self.random_numeric
        }

        alchemy_type = alchemy_types.get(class_type)

        if alchemy_type:
            fake_value = alchemy_type()
        else:
            fake_value = None

        return fake_value
