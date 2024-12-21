from fastapi import APIRouter, Request, status

from app.schemas.ticket_dto import TicketSearchDto, ManyTicketResponseDto, OneTicketResponseDto
from app.schemas.message_dto import MessageResponseDto
from app.schemas.base_responses import BasicResultResponseDto
from app.logic.ticket_dao import TicketDao

router = APIRouter(
    tags=["ticket"],
    prefix="/ticket"
)


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Получение списка обращений",
    description="""
    Получение списка тикетов. В body можно указать список названий статусов для фильтрации по этому полю
    + указать сортировать по created_at или нет
    """,
    response_model=list[ManyTicketResponseDto]
)
async def find_all(
        request: Request,
        body: TicketSearchDto
):
    """Получить обращения с фильтрами/сортировками."""
    async with request.app.state.db.get_master_session() as session:
        ticket_dao = TicketDao(session=session, options=TicketDao.list_options)
        return await ticket_dao.find_tickets(body=body)


@router.post(
    "/set/{ticket_id}",
    status_code=status.HTTP_200_OK,
    summary="Назначить обращение на оператора",
    description="Назначить обращение на оператора. Меняется статус на in_progress",
    response_model=BasicResultResponseDto
)
async def set_ticket(
        request: Request,
        ticket_id: int,
        operator_id: int
):
    """Назначить обращение на оператора."""
    async with request.app.state.db.get_master_session() as session:
        ticket_dao = TicketDao(session=session)
        await ticket_dao.set_ticket(ticket_id=ticket_id, operator_id=operator_id)
    return BasicResultResponseDto()


@router.get(
    "/{ticket_id}",
    status_code=status.HTTP_200_OK,
    summary="Получение обращения по id",
    description="Получение обращения по id вместе с его сообщениями",
    response_model=OneTicketResponseDto
)
async def find_all(
        request: Request,
        ticket_id: int
):
    """Получить обращение с его сообщениями."""
    async with request.app.state.db.get_master_session() as session:
        ticket_dao = TicketDao(session=session, options=TicketDao.options)
        return await ticket_dao.find_one(model_id=ticket_id)


@router.delete(
    "/close/{ticket_id}",
    status_code=status.HTTP_200_OK,
    summary="Закрыть обращение",
    description="Меняется статус обращения на closed + в рамках данного тикета отправляется автоответ о решении проблемы",
    response_model=MessageResponseDto
)
async def close_ticket(
        request: Request,
        ticket_id: int
):
    """Закрыть обращение. Ищем обращение и меняем статус + отправляем сообщение заказчику, что проблема решена."""
    async with request.app.state.db.get_master_session() as session:
        ticket_dao = TicketDao(session=session)
        return await ticket_dao.close_ticket(ticket_id=ticket_id)
