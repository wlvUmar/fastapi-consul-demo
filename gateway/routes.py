from typing import Annotated

from fastapi import APIRouter, Depends

from .config import settings
from .infrastructure.discovery import ServiceResolver, get_resolver
from .schemas import ErrorResponse
from .service import fetch_info

router = APIRouter()

responses = {502: {"model": ErrorResponse}, 503: {"model": ErrorResponse}, 504: {"model": ErrorResponse}}


@router.get("/service-a/info", responses=responses)
async def service_a_info(resolver: Annotated[ServiceResolver, Depends(get_resolver)]) -> dict:
    return await fetch_info("service-a", resolver, settings.request_timeout)


@router.get("/service-b/info", responses=responses)
async def service_b_info(resolver: Annotated[ServiceResolver, Depends(get_resolver)]) -> dict:
    return await fetch_info("service-b", resolver, settings.request_timeout)


@router.get("/service-c/info", responses=responses)
async def service_c_info(resolver: Annotated[ServiceResolver, Depends(get_resolver)]) -> dict:
    return await fetch_info("service-c", resolver, settings.request_timeout)
