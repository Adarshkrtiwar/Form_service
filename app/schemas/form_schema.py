from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Union
from enum import Enum

class FieldType(str, Enum):
    TEXT = "text"
    EMAIL = "email"
    NUMBER = "number"
    DATE = "date"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    SELECT = "select"
    FILE = "file"
    COMPUTED = "computed"

class FieldValidation(BaseModel):
    required: bool = True
    pattern: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None

class FormField(BaseModel):
    id: str
    type: FieldType
    label: str
    description: Optional[str] = None
    visible_if: Optional[str] = None
    validation: Optional[FieldValidation] = None
    options: Optional[List[Dict[str, str]]] = None
    computation: Optional[str] = None

class FormCard(BaseModel):
    id: str
    title: str
    fields: List[FormField]

class FormSchema(BaseModel):
    id: str
    title: str
    version: int = 1
    cards: List[FormCard]

class SchemaListResponse(BaseModel):
    schemas: List[Dict[str, str]]