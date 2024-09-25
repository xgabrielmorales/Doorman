from factory import Faker, django

from none.item.models import Item


class ItemFactory(django.DjangoModelFactory):
    class Meta:
        model = Item

    name = Faker("sentence", nb_words=2)
    description = Faker("sentence", nb_words=6)
    net_cost = Faker("numerify", text="%%%%%%.%%")
    tax_applicable = Faker("numerify", text="%%.%%")
    reference = Faker("ean")
    active = True
