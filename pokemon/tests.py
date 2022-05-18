from typing import Any, Optional

import pytest
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.db.models.fields import NOT_PROVIDED, Field

from . import admin, models


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


@pytest.mark.admin
@pytest.mark.parametrize("field", ["id", "name", "hp", "active"])
def test_list_display(field: str) -> None:
    list_display = getattr(admin.PokemonAdmin, "list_display", [])
    assert field in list_display


@pytest.mark.admin
def test_list_filter() -> None:
    list_filter = getattr(admin.PokemonAdmin, "list_filter", [])
    assert not isinstance(list_filter, str)
    assert "active" in list_filter


def get_options(spec: Optional[str]) -> Optional[dict[str, Any]]:
    fieldsets = admin.PokemonAdmin.fieldsets
    assert fieldsets is not None
    for cur_spec, options in fieldsets:
        if cur_spec == spec:
            return options

    return None


@pytest.mark.admin
def test_none_fieldsets() -> None:
    options = get_options(None)
    assert options is not None

    fields = sorted(options.get("fields", []))
    assert fields == ["active", "hp", "name", "type"]


@pytest.mark.admin
def test_collapsed_fieldsets() -> None:
    options = get_options("Localizations")
    assert options is not None, "No fieldset named Localizations found"

    fields = sorted(options.get("fields", []))
    assert fields == ["name_ar", "name_fr", "name_jp"]

    classes = options.get("classes", [])
    assert "collapse" in classes


@pytest.mark.bonus
def test_string_repr() -> None:
    name = "foo"
    assert str(models.Pokemon(name=name)) == name


@pytest.mark.bonus
@pytest.mark.parametrize("invalid_value", [15, 400])
def test_hp_validation(invalid_value: int) -> None:
    instance = models.Pokemon(
        name="Squirtle",
        type="WA",
        hp=invalid_value,
        name_fr="Squirtle",
        name_jp="Squirtle",
        name_ar="Squirtle",
    )
    with pytest.raises(ValidationError):
        instance.full_clean(exclude=["name", "type", "name_fr", "name_jp", "name_ar"])


@pytest.mark.models
@pytest.mark.parametrize("field_name", ["name_fr", "name_jp", "name_ar"])
def test_blank_fields(field_name: str) -> None:
    field = get_field(field_name)
    assert field.blank
