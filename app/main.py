import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import uvicorn
from fastapi import FastAPI

from app.utils.base import bind_routes, bind_events
from app.handlers import routes
from app.settings import settings


def make_app(settings) -> FastAPI:
    app = FastAPI(
        title="Service desk",
        description="",
        docs_url="/api/v1/service_desk/swagger"
    )

    bind_events(app=app, db_url=settings.database_url)
    bind_routes(app=app, routes=routes)
    return app


if __name__ == "__main__":
    uvicorn.run(
        make_app(settings=settings)
    )
