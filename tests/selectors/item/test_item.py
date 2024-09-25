import pytest

from none.item.selectors.item import item_detail, items_list
from tests.factories.item import ItemFactory


class TestItemDetail:
    @pytest.mark.django_db
    def test_item_detail(self):
        created_item = ItemFactory()
        fetched_item = item_detail(item_id=created_item.id)
        assert created_item.id is fetched_item.id

    @pytest.mark.django_db
    def test_fetch_inactive_item(self):
        created_item = ItemFactory(active=False)

        with pytest.raises(Exception):
            item_detail(item_id=created_item.id)


class TestItemList:
    @pytest.mark.django_db
    def test_list_items(self):
        created_item = ItemFactory.create_batch(size=3)
        fetched_item = items_list(query_params={})
        assert len(created_item) == fetched_item.count()

    @pytest.mark.django_db
    def test_list_inactive_items(self):
        ItemFactory.create_batch(size=3, active=False)
        fetched_item = items_list(query_params={})
        assert 0 == fetched_item.count()
