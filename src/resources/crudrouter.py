from typing import List
from .baserouter import BaseRouter


class CrudRouter(BaseRouter):
    def __init__(
            self,
            request_schema,
            response_schema,
            model,
            **kwargs
            ):
        super().__init__()
        self.request_schema = request_schema
        self.response_schema = response_schema
        self.model = model
        self.single_response_schema =\
            kwargs["single_response_schema"] if "single_response_schema" in kwargs else response_schema
        self.update_schema = \
            kwargs["update_schema"] if "update_schema" in kwargs else request_schema

    def load_routes(self):
        request_schema = self.request_schema
        response_schema = self.response_schema
        model = self.model
        single_response_schema = self.single_response_schema
        update_schema = self.update_schema

        @self.get("/", response_model=List[response_schema])
        async def fetch_all():
            return await response_schema.from_queryset(model.all())

        @self.get("/{item_id}", response_model=single_response_schema)
        async def fetch_one(item_id: str):
            return await single_response_schema\
                .from_queryset_single(model.get(id=item_id))

        @self.post("/", status_code=201, response_model=response_schema)
        async def create(item: request_schema):
            new_item = await model.create_one(item)
            return await response_schema.from_tortoise_orm(new_item)

        @self.put("/{item_id}", response_model=response_schema)
        async def update(item_id: str, item: update_schema):
            updated_item = await model.update_one(item_id, item)
            return await response_schema.from_queryset_single(updated_item)

        @self.delete("/{item_id}")
        async def delete(item_id: str):
            await model.delete_one(item_id)
            return {"message": "Item deleted successfully"}

