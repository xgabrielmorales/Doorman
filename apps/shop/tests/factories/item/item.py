from factory import Faker, django

from shop.item.models import Item


class ItemFactory(django.DjangoModelFactory):
    class Meta:
        model = Item

    name = Faker("sentence", nb_words=2)
    description = Faker("sentence", nb_words=6)
    gross_cost = Faker("numerify", text="%%%%%%.%%")
    tax_applicable = Faker("numerify", text="0.%%")
    reference = Faker("ean")
    active = True
