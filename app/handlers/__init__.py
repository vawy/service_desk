from app.handlers.ticket_handler import router as ticket_router
from app.handlers.message_handler import router as message_router
from app.handlers.operator_handler import router as operator_router
from app.handlers.customer_handler import router as customer_router

routes = [
    ticket_router,
    message_router,
    operator_router,
    customer_router
]

__all__ = [
    "routes",
]