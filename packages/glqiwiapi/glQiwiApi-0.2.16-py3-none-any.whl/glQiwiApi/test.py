import asyncio

from glQiwiApi import QiwiWrapper
from glQiwiApi.core.web_hooks.config import Path

TOKEN = 'c3fcef01058fdf8c475897f2e587c0e8'
QIWI_SECRET = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IngzeGpycS0wMCIsInVzZXJfaWQiOiIzODA5ODUyNzIwNjQiLCJzZWNyZXQiOiIyODZmNjg4NTdhZmM4ZTQ3M2U3ZTJkMjEwMzQxYTQyMTliOTI4ZjQzYWJkYjAxMzlkOWNhZTQyM2QwYzg1OTA5In19'
wallet = QiwiWrapper(
    api_access_token=TOKEN,
    secret_p2p=QIWI_SECRET
)


async def main():
    async with wallet as w:
        await w.bind_webhook(
            url="http://188.227.85.92/web_hooks/qiwi/",
            delete_old=True,
            send_test_notification=True
        )

asyncio.run(main())
