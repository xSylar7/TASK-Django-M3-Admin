from typing import Optional

import pytest
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.db.models.fields import NOT_PROVIDED, Field

from . import models


def get_field(name: str, model: Optional[type[Model]] = None) -> Field:
    if model is None:
        model = models.Pokemon
    return getattr(model, name).field


@pytest.mark.models
@pytest.mark.parametrize("field_name", ["name", "name_fr", "name_jp", "name_ar"])
def test_name_length(field_name: str) -> None:
    field = get_field(field_name)
    assert field.max_length == 30


@pytest.mark.models
@pytest.mark.parametrize("field_name", ["name_fr", "name_jp", "name_ar"])
def test_localizations(field_name: str) -> None:
    field = get_field(field_name)
    assert field.default == ""


@pytest.mark.models
@pytest.mark.parametrize(
    "field_name", ["name", "type", "hp", "created_at", "modified_at"]
)
def test_no_default(field_name: str) -> None:
    field = get_field(field_name)
    assert field.default == NOT_PROVIDED


@pytest.mark.models
@pytest.mark.parametrize("choice", ["WA", "GR", "GH", "ST", "FA"])
def test_valid_choices(choice: str) -> None:
    type_field = get_field("type")
    type_field.validate(choice, None)


@pytest.mark.models
@pytest.mark.parametrize("choice", ["foo", "bar", "spam", "p", "py"])
def test_invalid_choices(choice: str) -> None:
    type_field = get_field("type")
    with pytest.raises(ValidationError):
        type_field.validate(choice, None)


@pytest.mark.models
def test_created_at() -> None:
    field = get_field("created_at")
    assert field.auto_now_add == True


@pytest.mark.models
def test_modified_at() -> None:
    field = get_field("modified_at")
    assert field.auto_now == True
