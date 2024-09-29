from rest_framework import serializers
from rest_framework.fields import Field


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(
    *,
    name: str,
    fields: dict[str, Field],
    data=None,
    **kwargs,
):
    serializer_class = create_serializer_class(
        name=name,
        fields=fields,
    )

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
