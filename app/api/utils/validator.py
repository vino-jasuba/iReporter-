import re
from marshmallow import ValidationError


def required(value):
    """Validate that field under validation does not contain null value."""

    if isinstance(value, str):
        if not value.strip(' '):
            raise ValidationError('The parameter cannot be null')

        return value
    elif value:
        return value


def email(value):
    """Validate field matches email format."""

    if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)", value):
        raise ValidationError('The parameter must be a valid email')

    return value


def geopoint(value):
    """Validate field contains lat and lng coordinates."""

    if list(value) != ['lat', 'lng']:
        raise ValidationError(
            'Location not properly formatted. Expecting lat and lng')

    if not isinstance(value['lat'], float) or not isinstance(value['lng'], float):
        raise ValidationError('Expecting float value')

    if value['lat'] > 90 or value['lat'] < -90:
        raise ValidationError("Value range exceeded for field lat")

    if value['lng'] > 90 or value['lng'] < -180:
        raise ValidationError("Value range exceeded for field lng")

    return value


def strong_password(password):
    """Validate field contains strong password"""

    message = "Password field should be at least 8 characters long." \
    " Have at least 1 uppercase, 1 lowercase and 1 digit"

    if len(password) < 8:
        raise ValidationError(message)

    scores = {}

    for letter in password:
        if letter.islower():
            scores['has_lower'] = 1

        if letter.isupper():
            scores['has_upper'] = 1

        if letter.isdigit():
            scores['has_digit'] = 1

    if sum(scores.values()) < 3:
        raise ValidationError(message)