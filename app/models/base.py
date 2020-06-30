from sqlalchemy.ext.declarative import declarative_base


def base_repr(self):
    """
    Creates beautiful repr() strings for an object based on it's classname and __dict__
    Made specifically for objects that inherit from SQLAlchemy's declarative base, but will probably work for others too

    :param self: Object, instance of SQLAlchemy's declarative base
    :return: str: repr string, that looks like this: "<ClassName(attr1='value', attr2=321)>"
    """

    # Filter for only public attributes
    attrs = filter(lambda t: not t[0].startswith('_'), self.__dict__.items())
    # Exclude instances of the same base class to avoid circular recursion with one-to-many relationships
    attrs = filter(lambda t: not isinstance(t[1], self.__class__.__bases__), attrs)
    # Make a tuple of strings that look like this: attr_name='value'
    attr_strings = tuple(map(lambda t: f"{t[0]}={repr(t[1])}", attrs))
    # Combine the class name with the attributes to get
    # <ClassName(attr1='value', attr2=321)>
    return f'<{self.__class__.__name__}({", ".join(attr_strings)})>'


Base = declarative_base()
Base.__repr__ = base_repr
