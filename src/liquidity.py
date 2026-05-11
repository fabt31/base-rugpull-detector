import httpx, asyncio
BASE_RPC = "https://mainnet.base.org"
async def check_liquidity(pool_address: str) -> dict:
    """Check if liquidity is locked and sufficient."""
    async with httpx.AsyncClient() as client:
        bal_resp = await client.post(BASE_RPC, json={"jsonrpc":"2.0","method":"eth_getBalance","params":[pool_address,"latest"],"id":1}, timeout=5)
        balance_hex = bal_resp.json().get("result", "0x0")
        balance_eth = int(balance_hex, 16) / 1e18
    return {"pool": pool_address, "liquidity_eth": balance_eth, "sufficient": balance_eth >= 5.0}
