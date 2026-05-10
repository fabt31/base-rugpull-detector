import httpx
import asyncio
from dataclasses import dataclass, field
from typing import Optional

BASE_RPC = "https://mainnet.base.org"

DANGEROUS_SELECTORS = {
    "0x40c10f19": "mint(address,uint256)",
    "0x42842e0e": "safeTransferFrom (possible blacklist)",
    "0x8456cb59": "pause()",
    "0x3f4ba83a": "unpause()",
    "0xf2fde38b": "transferOwnership(address)",
    "0xdd62ed3e": "allowance check",
}

@dataclass
class TokenRisk:
    address: str
    name: str = "Unknown"
    symbol: str = "?"
    score: int = 100
    risks: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    def add_risk(self, msg: str, points: int = 20):
        self.risks.append(msg); self.score = max(0, self.score - points)

    def add_warning(self, msg: str, points: int = 10):
        self.warnings.append(msg); self.score = max(0, self.score - points)

    def label(self) -> str:
        if self.score >= 80: return "✅ LOW RISK"
        if self.score >= 50: return "⚠️  MEDIUM RISK"
        return "❌ HIGH RISK"

async def call_rpc(client, method: str, params: list) -> dict:
    r = await client.post(BASE_RPC, json={"jsonrpc":"2.0","method":method,"params":params,"id":1},
                          headers={"Content-Type":"application/json"}, timeout=10)
    return r.json()

async def scan_token(address: str) -> TokenRisk:
    risk = TokenRisk(address=address)
    async with httpx.AsyncClient() as client:
        # Get bytecode
        code_resp = await call_rpc(client, "eth_getCode", [address, "latest"])
        bytecode = code_resp.get("result", "0x")
        if bytecode == "0x" or len(bytecode) < 10:
            risk.add_risk("No contract code found", 100); return risk

        # Check for dangerous selectors
        for selector, name in DANGEROUS_SELECTORS.items():
            if selector[2:] in bytecode:
                risk.add_warning(f"Has function: {name}")

        # Check owner
        owner_data = "0x8da5cb5b"  # owner()
        owner_resp = await call_rpc(client, "eth_call", [{"to": address, "data": owner_data}, "latest"])
        owner = owner_resp.get("result", "0x")
        if owner and owner != "0x" + "0"*64:
            risk.add_warning("Contract has owner (not renounced)")

    return risk

async def main():
    import sys
    token = sys.argv[1] if len(sys.argv) > 1 else "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    print(f"Scanning {token}...")
    risk = await scan_token(token)
    print(f"\nSafety Score: {risk.score}/100 {risk.label()}")
    for r in risk.risks: print(f"  ❌ {r}")
    for w in risk.warnings: print(f"  ⚠️  {w}")

if __name__ == "__main__":
    asyncio.run(main())