from src.utils.enums import Status
from slugify import slugify
from tortoise import fields, models


class BaseModel(models.Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)

    """ Database methods """
    @classmethod
    async def create_one(cls, item):
        return await cls.create(**item.dict())

    @classmethod
    async def find_by(cls, *args, **kwargs):
        if args is not None:
            return await cls.filter(**kwargs).prefetch_related(*args).all()
        return await cls.filter(**kwargs).all()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        return await cls.get_or_none(**kwargs)

    @classmethod
    async def find_one(cls, *args, **kwargs):
        if args is not None:
            return await cls.filter(**kwargs).prefetch_related(*args).first()
        return await cls.filter(**kwargs).first()

    @classmethod
    async def update_one(cls, _id: str, item):
        await cls.filter(id=_id).update(**item.dict(exclude_unset=True))
        return cls.get(id=_id)

    @classmethod
    async def delete_one(cls, _id: str) -> int:
        deleted_count = await cls.filter(id=_id).delete()
        return deleted_count

    class Meta:
        __abstract__ = True


class ModelWithStatus(BaseModel):
    status = fields.CharEnumField(Status, default=Status.ACTIVE)

    class Meta:
        __abstract__ = True


class SluggableModel(ModelWithStatus):
    slug = fields.CharField(max_length=70)

    """ Database methods """
    @classmethod
    async def create_one(cls, item):
        return await cls.create(**item.dict(), slug=cls.make_slug(item.name))

    @classmethod
    async def update_one(cls, _id: str, item):
        await cls.filter(id=_id).update(
            **item.dict(exclude_unset=True),
            slug=cls.make_slug(item.name)
        )
        return cls.get(id=_id)

    """ Utility methods """
    @classmethod
    def make_slug(cls, title: str):
        return slugify(title)

    class Meta:
        __abstract__ = True
