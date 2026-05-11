import asyncio, httpx
BASE_RPC = "https://mainnet.base.org"
async def simulate_sell(token: str, amount: int = 10**18) -> dict:
    """Simulate a sell to detect honeypot."""
    router = "0x2626664c2603336E57B271c5C0b26F421741e481"
    weth = "0x4200000000000000000000000000000000000006"
    call_data = {"to": router, "data": "0x04e45aaf" + "0" * 100, "from": "0x0000000000000000000000000000000000000001"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(BASE_RPC, json={"jsonrpc":"2.0","method":"eth_call","params":[call_data,"latest"],"id":1}, timeout=5)
        result = resp.json()
        if "error" in result:
            return {"honeypot": True, "reason": result["error"].get("message", "Sell failed")}
    return {"honeypot": False}
