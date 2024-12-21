from fastapi import APIRouter, Request, status

from app.logic.operator_dao import OperatorDao
from app.schemas.operator_dto import OperatorFullResponseDto, OperatorOneResponseDto

router = APIRouter(
    tags=["operator"],
    prefix="/operator"
)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Получение списка операторов",
    description="Получение списка операторов",
    response_model=list[OperatorFullResponseDto]
)
async def find_all(
        request: Request
):
    async with request.app.state.db.get_master_session() as session:
        operator_dao = OperatorDao(session=session, options=OperatorDao.list_options)
        return await operator_dao.find_all()


@router.get(
    "/{operator_id}",
    status_code=status.HTTP_200_OK,
    summary="Получение оператора по id",
    description="Получение оператора по id",
    response_model=OperatorOneResponseDto
)
async def find_one(
        request: Request,
        operator_id: int
):
    async with request.app.state.db.get_master_session() as session:
        operator_dao = OperatorDao(session=session, options=OperatorDao.options)
        return await operator_dao.find_one(model_id=operator_id)
