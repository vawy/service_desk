from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import LoaderOption
from sqlalchemy.sql.selectable import Select

from starlette import status

from metadata import Base


class BaseDao:
    def __init__(
            self,
            session: AsyncSession,
            model: Base,
            options: list[LoaderOption] | None = None,
    ):
        self.session = session
        self.model = model
        self.options = options or []

    async def find_all(self, query=None):
        if query is None:
            query = self._build_default_query()

        if self.options:
            query = query.options(*self.options)

        result = await self.session.scalars(query)
        result = result.all()
        return result


    async def find_one(
            self,
            model_id=None,
            query=None,
            raise_exception=True
    ):
        if query is None:
            query = self._build_default_query()

        if model_id is not None:
            query = query.where(self.model.id == model_id)

        if self.options:
            query = query.options(*self.options)

        model = await self.session.scalar(query)

        if not model:
            if raise_exception:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Model {self.model.__name__} with ID={model_id} was not found",
                )
            return None

        return model



    def _build_default_query(self) -> Select:
        return select(self.model)