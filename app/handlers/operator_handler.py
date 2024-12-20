from fastapi import APIRouter, Request, status

from app.logic.operator_dao import OperatorDao
from app.schemas.operator_dto import OperatorFullResponseDto

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
