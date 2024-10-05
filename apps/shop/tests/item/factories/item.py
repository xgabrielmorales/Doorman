from factory import Faker, django, fuzzy

from shop.item.models import Item


class ItemFactory(django.DjangoModelFactory):
    class Meta:
        model = Item

    name = Faker("sentence", nb_words=2)
    description = Faker("sentence", nb_words=6)
    gross_cost = fuzzy.FuzzyDecimal(
        low=0.00,
        high=99999.99,
        precision=2,
    )
    tax_applicable = fuzzy.FuzzyDecimal(
        low=0,
        high=1,
        precision=2,
    )

    reference = Faker("ean")
    active = True
