"""
Functions and schemas relating to specification 214, for level 0 FITS files.

This submodule generates a hybrid spec 122 / spec 214 schema for level 0 files
ingested by the data center.
"""
from typing import Dict, Optional

from dkist_fits_specifications import spec122, spec214
from dkist_fits_specifications.utils import (raw_schema_type_hint,
                                             schema_type_hint,)

__all__ = ['load_level0_spec214']


def rename_only_spec214(schema: raw_schema_type_hint) -> schema_type_hint:
    """
    Parse a 214 schema and filter out all keys which do not have a type of rename.
    """
    new_schema = {}
    for key, key_schema in schema[1].items():
        if 'rename' in key_schema:
            new_schema[key] = key_schema

    return spec214.preprocess_schema((schema[0], new_schema))


def load_level0_spec214(glob: Optional[str] = None) -> Dict[str, schema_type_hint]:
    """
    Return the loaded schemas for Level 0 214 files.

    This schema is a superset of the 122 schemas, with all 214 key schemas
    added if the 214 key is a rename of a 122 key.
    """

    spec_122_schemas = spec122.load_spec122(glob)
    raw_214_schemas = spec214.load_raw_spec214(glob)
    spec_122_214_map = {}

    for name_214, schema_214 in raw_214_schemas.items():
        name_122 = schema_214[0]['spec214']['section_122']
        if name_122 is not None:
            spec_122_214_map[name_122] = name_214

    level0_schemas = {}
    for name_122, schema_122 in spec_122_schemas.items():
        rename_214 = rename_only_spec214(raw_214_schemas[spec_122_214_map[name_122]])
        level0_schemas[name_122] = {**schema_122, **rename_214}

    return level0_schemas
