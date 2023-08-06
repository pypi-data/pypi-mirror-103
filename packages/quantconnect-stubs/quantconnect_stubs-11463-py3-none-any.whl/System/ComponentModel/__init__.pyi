import abc
import typing

import System
import System.Collections
import System.ComponentModel

System_ComponentModel__EventContainer_Callable = typing.TypeVar("System_ComponentModel__EventContainer_Callable")
System_ComponentModel__EventContainer_ReturnType = typing.TypeVar("System_ComponentModel__EventContainer_ReturnType")


class EditorBrowsableState(System.Enum):
    """This class has no documentation."""

    Always = 0

    Never = 1

    Advanced = 2


class EditorBrowsableAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def State(self) -> int:
        """This property contains the int value of a member of the System.ComponentModel.EditorBrowsableState enum."""
        ...

    @typing.overload
    def __init__(self, state: System.ComponentModel.EditorBrowsableState) -> None:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class DefaultValueAttribute(System.Attribute):
    """Specifies the default value for a property."""

    @property
    def Value(self) -> System.Object:
        """Gets the default value of the property this attribute is bound to."""
        ...

    @typing.overload
    def __init__(self, type: typing.Type, value: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class, converting the specified value to the specified type, and using the U.S. English
        culture as the translation context.
        """
        ...

    @typing.overload
    def __init__(self, value: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a Unicode character.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using an 8-bit unsigned integer.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a 16-bit signed integer.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a 32-bit signed integer.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a 64-bit signed integer.
        """
        ...

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a single-precision floating point number.
        """
        ...

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a double-precision floating point number.
        """
        ...

    @typing.overload
    def __init__(self, value: bool) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a bool value.
        """
        ...

    @typing.overload
    def __init__(self, value: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a string.
        """
        ...

    @typing.overload
    def __init__(self, value: typing.Any) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a sbyte value.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a ushort value.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a uint value.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a ulong value.
        """
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def SetValue(self, value: typing.Any) -> None:
        """This method is protected."""
        ...


class TypeConverterAttribute(System.Attribute):
    """
    Specifies what type to use as a converter for the object this attribute is
    bound to. This class cannot be inherited.
    """

    Default: System.ComponentModel.TypeConverterAttribute = ...
    """
    Specifies the type to use as a converter for the object this attribute is
    bound to. This static field is read-only.
    """

    @property
    def ConverterTypeName(self) -> str:
        """
        Gets the fully qualified type name of the System.Type to use as a
        converter for the object this attribute is bound to.
        """
        ...

    @typing.overload
    def __init__(self) -> None:
        """
        Initializes a new instance of the System.ComponentModel.TypeConverterAttribute
        class with the default type converter, which is an empty string ("").
        """
        ...

    @typing.overload
    def __init__(self, type: typing.Type) -> None:
        """
        Initializes a new instance of the System.ComponentModel.TypeConverterAttribute
        class, using the specified type as the data converter for the object this attribute
        is bound to.
        """
        ...

    @typing.overload
    def __init__(self, typeName: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.TypeConverterAttribute
        class, using the specified type name as the data converter for the object this attribute
        is bound to.
        """
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class PropertyChangingEventArgs(System.EventArgs):
    """Provides data for the PropertyChanging event."""

    @property
    def PropertyName(self) -> str:
        """Indicates the name of the property that is changing."""
        ...

    def __init__(self, propertyName: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.PropertyChangingEventArgs
        class.
        """
        ...


class DataErrorsChangedEventArgs(System.EventArgs):
    """Provides data for the ErrorsChanged event."""

    @property
    def PropertyName(self) -> str:
        """Indicates the name of the property whose errors changed."""
        ...

    def __init__(self, propertyName: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DataErrorsChangedEventArgs
        class.
        """
        ...


class INotifyDataErrorInfo(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def HasErrors(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def ErrorsChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.ComponentModel.DataErrorsChangedEventArgs], None], None]:
        ...

    @ErrorsChanged.setter
    @abc.abstractmethod
    def ErrorsChanged(self, value: _EventContainer[typing.Callable[[System.Object, System.ComponentModel.DataErrorsChangedEventArgs], None], None]):
        ...

    def GetErrors(self, propertyName: str) -> System.Collections.IEnumerable:
        ...


class PropertyChangedEventArgs(System.EventArgs):
    """Provides data for the PropertyChanged event."""

    @property
    def PropertyName(self) -> str:
        """Indicates the name of the property that changed."""
        ...

    def __init__(self, propertyName: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.PropertyChangedEventArgs
        class.
        """
        ...


class INotifyPropertyChanged(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def PropertyChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.ComponentModel.PropertyChangedEventArgs], None], None]:
        ...

    @PropertyChanged.setter
    @abc.abstractmethod
    def PropertyChanged(self, value: _EventContainer[typing.Callable[[System.Object, System.ComponentModel.PropertyChangedEventArgs], None], None]):
        ...


class INotifyPropertyChanging(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def PropertyChanging(self) -> _EventContainer[typing.Callable[[System.Object, System.ComponentModel.PropertyChangingEventArgs], None], None]:
        ...

    @PropertyChanging.setter
    @abc.abstractmethod
    def PropertyChanging(self, value: _EventContainer[typing.Callable[[System.Object, System.ComponentModel.PropertyChangingEventArgs], None], None]):
        ...


class TypeDescriptionProviderAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def TypeName(self) -> str:
        """
        The TypeName property returns the assembly qualified type name
        for the type description provider.
        """
        ...

    @typing.overload
    def __init__(self, typeName: str) -> None:
        """Creates a new TypeDescriptionProviderAttribute object."""
        ...

    @typing.overload
    def __init__(self, type: typing.Type) -> None:
        """Creates a new TypeDescriptionProviderAttribute object."""
        ...


class _EventContainer(typing.Generic[System_ComponentModel__EventContainer_Callable, System_ComponentModel__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_ComponentModel__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_ComponentModel__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_ComponentModel__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


