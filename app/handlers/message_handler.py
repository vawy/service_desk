from typing import Union

from fastapi import APIRouter, Request, status

from app.schemas.message_dto import SendMessageToOperatorDto, SendMessageToCustomerDto, MessageResponseDto
from app.schemas.base_responses import BasicResultResponseDto
from app.logic.message_dao import MessageDao

router = APIRouter(
    tags=["message"],
    prefix="/message"
)

@router.post(
    "/send_to_operator",
    status_code=status.HTTP_200_OK,
    summary="Отправить сообщение оператору",
    description="""
    Отправить сообщение оператору. в body указывается customer_id(какой клиент отправляет сообщение). Если у данного
    клиента есть открытый тикет, то сообщение отправляется туда, если нет, то создается новый тикет, в который
    отправляется сообщение от клиента и автоответ от системы
    """,
    response_model=Union[MessageResponseDto, BasicResultResponseDto]
)
async def send_to_operator(
        request: Request,
        customer_id: int,
        body: SendMessageToOperatorDto
):
    """
    Отправка сообщения оператору.
    Если нет открытого тикета, то создается новый + отправляется автоответ
    Если есть открытый тикет, то сообщение отправляется в него.
    """
    async with request.app.state.db.get_master_session() as session:
        message_dao = MessageDao(session=session)
        return await message_dao.send_to_operator(body=body, customer_id=customer_id)


@router.post(
    "/send_to_customer",
    status_code=status.HTTP_200_OK,
    summary="Отправить сообщение заказчику в тикет",
    description="""
    Отправить сообщение заказчику в тикет. В body указывается ticket_id. Если данный тикет закрыт или у него нет 
    прикрепленного оператора, то отдаст ошибку, если все норм, то отправит сообщение в тикет
    """,
    response_model=BasicResultResponseDto
)
async def send_to_customer(
        request: Request,
        body: SendMessageToCustomerDto
):
    """
    Отправка сообщения заказчику в тикет.
    """
    async with request.app.state.db.get_master_session() as session:
        message_dao = MessageDao(session=session)
        await message_dao.send_to_customer(body=body)
    return BasicResultResponseDto()
