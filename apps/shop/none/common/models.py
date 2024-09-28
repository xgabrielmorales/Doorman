from django.db import models


class BaseModel(models.Model):
    """Base model.

    Base model from which all project models will inherit. It includes the
    common attributes for all models:

    - created_at (datetime): describes the creation date/time of the object.
    - updated_at (datetime): describes the object's modification date/time.
    - active (bool): describes whether the object is active or not.

    Also, an object in db should not be deleted so the `delete()` method instead
    of implementing a physical delete, implements a logical delete using the
    active field.
    """

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
