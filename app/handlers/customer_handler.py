from fastapi import APIRouter, Request, status

from app.logic.customer_dao import CustomerDao
from app.schemas.customer_dto import CustomerFullResponseDto

router = APIRouter(
    tags=["customer"],
    prefix="/customer"
)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Получение списка заказчиков",
    description="Получение списка заказчиков",
    response_model=list[CustomerFullResponseDto]
)
async def find_all(
        request: Request
):
    async with request.app.state.db.get_master_session() as session:
        customer_dao = CustomerDao(session=session, options=CustomerDao.list_options)
        return await customer_dao.find_all()
