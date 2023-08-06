import os
import pathlib
import textwrap

from .errors import ValidationError
from .validators import IsInstance


class UnboundField:
    _configuration_field = True
    creation_counter = 0

    def __init__(self, field_class, *args, **kwargs):
        UnboundField.creation_counter += 1
        self.field_class = field_class
        self.args = args
        self.kwargs = kwargs
        self.creation_counter = UnboundField.creation_counter
        # validators = kwargs.get("validators")
        # if validators:
        #     self.field_class.check_validators(validators)

    def bind(self, configuration, name, **kwargs):
        field = self.field_class(
            *self.args,
            **dict(self.kwargs, _configuration=configuration, _name=name, **kwargs)
        )
        return field

    def __repr__(self):
        return "<UnboundField(%s, %r, %r)>" % (
            self.field_class.__name__,
            self.args,
            self.kwargs,
        )


class Field:
    _configuration_field = True
    _validators = ()

    def __new__(cls, *args, **kwargs):
        if "_configuration" in kwargs and "_name" in kwargs:
            return super(Field, cls).__new__(cls)
        else:
            return UnboundField(cls, *args, **kwargs)

    def __init__(
        self,
        label,
        validators=(),
        description=None,
        units=None,
        default=None,
        _configuration=None,
        _name=None,
    ):
        self._label = label
        self._default = default
        # self._validators = validators or ()
        self._validators = self._validators + tuple(validators)
        self._description = description
        self._units = units
        self._data = None
        self.process({}, self.default)

        self._configuration = None
        self._errors = []

    @property
    def description(self):
        return self._description

    def long_description(self):
        brief, extended = "", ""
        if self.units:
            brief = "[{units}] ".format(units=self.units)

        lines = self.description.rstrip().splitlines()
        if lines:
            brief, extended = brief + lines[0], lines[1:]

            extended = textwrap.dedent(os.linesep.join(extended))

        return os.linesep.join([brief] + extended.splitlines())

    @property
    def default(self):
        return self._default

    @property
    def units(self):
        return self._units

    @property
    def data(self):
        return self._data

    def process(self, config, value=None):
        if value is None:
            value = self.default

        self.validate(config, value)
        self._data = value

    def validate(self, config, value):
        self._errors = []
        for validate in self._validators:
            try:
                validate(config, value)
            except ValidationError as error:
                self._errors.append(error)
        if self._errors:
            raise ValidationError(", ".join([e.message for e in self._errors]))

    def __repr__(self):
        return "%s(%r, description=%r, units=%r, default=%r)" % (
            self.__class__.__name__,
            self._label,
            self.description,
            self.units,
            self.default,
            # self.data,
        )


class FloatField(Field):
    _validators = (IsInstance((float, int)),)

    @property
    def data(self):
        return float(self._data)


class IntegerField(Field):
    _validators = (IsInstance(int),)

    def process(self, config, value=None):
        if value is not None:
            try:
                as_int = int(value)
            except TypeError:
                pass
            else:
                if as_int == value:
                    value = as_int
        super().process(config, value=value)


class BooleanField(Field):
    _validators = (IsInstance(bool),)

    def process(self, config, value=None):
        if value is not None:
            try:
                as_bool = bool(value)
            except TypeError:
                pass
            else:
                if as_bool == value:
                    value = as_bool
        super().process(config, value=value)


class ArrayField(Field):
    _validators = (IsInstance((tuple, list)),)

    @property
    def data(self):
        return tuple(self._data)


class PathField(Field):
    _validators = IsInstance(str)

    @property
    def data(self):
        return pathlib.Path(self._data)


class ConfigurationField(Field):
    def __init__(
        self,
        label,
        configuration_class,
        validators=(),
        description=None,
        units=None,
        default=None,
        _configuration=None,
        _name=None,
    ):
        self._configuration_class = configuration_class
        super(ConfigurationField, self).__init__(
            label,
            validators=validators,
            description=description,
            units=units,
            default=default,
        )

    def process(self, config, value):
        if hasattr(value, "data"):
            rtn = self._configuration_class(value.data)
        else:
            rtn = self._configuration_class(value)
        self._data = rtn
        # self._data = value
