import os
import sys

import ruamel.yaml
import yaml
from ruamel.yaml.comments import CommentedMap


class ConfigurationBase:
    def __init__(self, fields):
        """Configuration base class.

        Parameters
        ----------
        data : dict-like
            A dictionary of configuration data.
        """
        self._fields = dict()
        for name, unbound_field in fields:
            # options = dict(name=name, prefix=prefix, translations=translations)
            # field = meta.bind_field(self, unbound_field, options)
            self._fields[name] = unbound_field.bind(self, name)
            # self._fields[name] = unbound_field

        self._errors = None

    @property
    def data(self):
        return dict((name, f.data) for name, f in self._fields.items())

    @property
    def errors(self):
        if self._errors is None:
            self._errors = dict(
                (name, f.errors) for name, f in self._fields.items() if f.errors
            )
        return self._errors

    def validate(self):
        """Validate each value of the form"""
        for field in self._fields:
            field.validate(self)

    def process(self, data):
        for name, field in self._fields.items():
            if name in data:
                field.process(data, data[name])

    def keys(self):
        return self._fields.keys()

    def items(self):
        return self._fields.items()

    def __iter__(self):
        """Iterate form fields in creation order."""
        return iter(self._fields.values())

    def __contains__(self, name):
        """Returns `True` if the named field is a member of this form."""
        return name in self._fields

    def __getitem__(self, name):
        """Dict-style access to this form's fields."""
        return self._fields[name]

    def __setitem__(self, name, value):
        """Bind a field to this form. """
        self._fields[name] = value.bind(form=self, name=name, prefix=self._prefix)

    def __delitem__(self, name):
        """Remove a field from this form. """
        del self._fields[name]

    @staticmethod
    def _yaml_representer(dumper, data, flow_style=False):
        assert isinstance(dumper, ruamel.yaml.RoundTripDumper)
        return dumper.represent_dict(data._convert_to_yaml_struct())

    def _convert_to_yaml_struct(self, indent=32):
        x = CommentedMap()
        for name, field in self._fields.items():
            x[name] = field.data
            lines = field.long_description().splitlines()
            if lines:
                first, extra = lines[0], lines[1:]

                description = os.linesep.join(
                    [first] + [" " * indent + "# " + line for line in extra]
                )
                x.yaml_add_eol_comment(description, name, indent)

        return x

    def to_yaml(self):
        return ruamel.yaml.round_trip_dump(self)
        ruamel.yaml.round_trip_dump(self, sys.stdout)


class ConfigurationMeta(type):
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        cls._unbound_fields = None
        ruamel.yaml.RoundTripDumper.add_representer(
            cls, ConfigurationBase._yaml_representer
        )

    def __call__(cls, *args, **kwds):

        if cls._unbound_fields is None:
            fields = []
            for name in dir(cls):
                if not name.startswith("_"):
                    unbound_field = getattr(cls, name)
                    if hasattr(unbound_field, "_configuration_field"):
                        fields.append((name, unbound_field))
            fields.sort(key=lambda x: (x[1].creation_counter, x[0]))
            cls._unbound_fields = fields

        return type.__call__(cls, *args, **kwds)
        # return super(ConfigurationMeta, cls).__call__(*args, **kwds)


class Configuration(ConfigurationBase, metaclass=ConfigurationMeta):
    def __init__(self, data=None):
        if data is None:
            data = {}

        super(Configuration, self).__init__(self._unbound_fields)

        for name, field in self._fields.items():
            # Set all the fields to attributes so that they obscure the class
            # attributes with the same names.
            setattr(self, name, field)

        self.process(data)

    @classmethod
    def from_path(cls, path_to_file, fmt="yaml", loader=None):
        try:
            loader = getattr(cls, f"from_{fmt}")
        except AttributeError:
            raise ValueError(f"unknown configuration file format ({format})")
        else:
            return cls(data=loader(path_to_file))
            # return loader(cls, path_to_file)

    @classmethod
    def from_yaml(cls, filepath):
        with open(filepath, "r") as fp:
            params = yaml.safe_load(fp)
        return cls(data=params)
