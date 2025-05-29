import asyncio

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.anyio
async def test_async(client_async: AsyncClient) -> None:
    results = await asyncio.gather(*[client_async.get("/posts") for _ in range(2)])
    for response in results:
        assert response.status_code == status.HTTP_200_OK
