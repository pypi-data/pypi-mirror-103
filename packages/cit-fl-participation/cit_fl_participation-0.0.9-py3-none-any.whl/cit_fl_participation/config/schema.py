from collections import namedtuple
import ipaddress
from typing import Any, Mapping, NamedTuple, Type, TypeVar
import urllib.error
import urllib.parse

import idna
from schema import And, Optional, Or, Schema, SchemaError, Use
import toml

def error(key: str, description: str) -> str:
    """Return an error message for the given configuration item and
    description of the expected value type.

    Args:

        key (str): key of the configuration item
        description (str): description of the expected type of value
            for this configuration item
    """
    return f"Invalid `{key}`: value must be {description}"

def url(key: str, expected_value: str = "a valid URL") -> Schema:
    """Return a URL validator for the given configuration item.

    Args:

        key: key of the configuration item
        expected_value: description of the expected type of
            value for this configuration item

    """

    def is_valid_url(value: str) -> bool:
        try:
            parsed = urllib.parse.urlparse(value)
        except (ValueError, urllib.error.URLError):
            return False
        # A URL is considered valid if it has at least a scheme and a
        # network location.
        return all([parsed.scheme, parsed.netloc])

    return And(str, is_valid_url, error=error(key, expected_value))

STORAGE_SCHEMA = Schema(
    {
        "endpoint": And(str, url, error=error("storage.endpoint", "a valid URL")),
        "bucket": Use(str, error=error("storage.bucket", "an S3 bucket name")),
        "secret_access_key": Use(
            str, error=error("storage.secret_access_key", "a valid utf-8 string")
        ),
        "access_key_id": Use(
            str, error=error("storage.access_key_id", "a valid utf-8 string")
        ),
    }
)

def create_class_from_schema(class_name: str, schema: Schema) -> Any:

    """Create a class named `class_name` from the given `schema`, where
    the attributes of the new class are the schema's keys.

    Args:

        class_name: name of the class to create
        schema: schema from which to create the class

    Returns:

        A new class where attributes are the given schema's keys
    """
    # pylint: disable=protected-access
    keys = schema._schema.keys()
    attributes = list(
        map(lambda key: key._schema if isinstance(key, Schema) else key, keys)  # type: ignore
    )
    return namedtuple(class_name, attributes)

StorageConfig = create_class_from_schema("StorageConfig", STORAGE_SCHEMA)
StorageConfig.__doc__ = (
    "Storage related configuration: storage endpoints and credentials, etc."
)
