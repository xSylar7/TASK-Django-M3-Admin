# Task

For the models task below take advantage of the [model field reference](https://docs.djangoproject.com/en/4.0/ref/models/fields/), and for the admin task use the [admin site reference](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/) to guide you.

## Setup

1. Fork and clone [this repository](https://github.com/JoinCODED/TASK-Django-M3-Admin).
2. Create a `virtual environment`, and activate it.

## Models

1. Install the requirements using `pip install -r dev-requirements.txt`.
2. Create a `Pokemon` model with the following attributes:

   - `name`: `CharField` with a maximum of 30 characters.
   - `type`: `CharField` with choices. Make sure to use [`TextChoices`](https://docs.djangoproject.com/en/4.0/ref/models/fields/#enumeration-types) and call the class `PokemonType`. The choices will be as follows:
     - `WATER = 'WA'`
     - `GRASS = 'GR'`
     - `GHOST = 'GH'`
     - `STEEL = 'ST'`
     - `FAIRY = 'FA'`
   - `hp`: `PositiveIntegerField`.
   - `active`: `BooleanField` that defaults to `True`.
   - `name_fr`: `CharField` with a maximum of 30 characters and defaults to an empty `string`.
   - `name_ar`: `CharField` with a maximum of 30 characters and defaults to an empty `string`.
   - `name_jp`: `CharField` with a maximum of 30 characters and defaults to an empty `string`.
   - `created_at`: `DateTimeField` that automatically sets the field when the model is **created**.
   - `modified_at`: `DateTimeField` that automatically sets the field when the model is **updated**.

3. Make migrations and migrate your changes.
4. Run `pytest -m models` and pass all tests.
5. Push your code.

## Admin Site

1. Import your `Pokemon` model.
2. Create a `PokemonAdmin` class and attach your `Pokemon` model to it.
3. Customize your `PokemonAdmin`:
   - The list page only displays the `id`, `name`, `hp`, and `active`.
   - The list page is filterable by `active` status.
   - The list page has both `id` and `name` columns clickable and take you to the form page.
   - The form page has the `name_fr`, `name_ar`, and `name_jp` in different section below, with the title as `Localizations` and collapsible (hint: look for something called `fieldsets`).
4. Run `pytest -m admin` and pass all tests.
5. Push your code.

## Bonus

1. Add a string representation for the `Pokemon` model.
2. Add validation for `hp` to be between `50` and `350`.
3. Run `pytest` and pass all tests.
