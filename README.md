# base-rugpull-detector

> Token Safety & Rug Pull Detector for Base L2

Before trading any token on Base, scan it for rug pull risks, honeypot patterns, suspicious ownership, and malicious contract code. Get a safety score in seconds.

## Risk Checks
| Check | Description |
|-------|-------------|
| Honeypot | Can tokens be sold? |
| Ownership | Is ownership renounced? |
| Mint function | Can supply be inflated? |
| Blacklist | Can wallets be blacklisted? |
| Trading pause | Can trading be paused? |
| Liquidity lock | Is LP locked? |
| Proxy | Is contract upgradeable? |
| Max tx | Unreasonably low max tx? |

## Installation
```bash
git clone https://github.com/fabt31/base-rugpull-detector
cd base-rugpull-detector
pip install -r requirements.txt
```

## Usage
```bash
# Scan a token
python scan.py --token 0xTokenAddress

# Scan and output JSON
python scan.py --token 0xTokenAddress --json

# Batch scan from file
python scan.py --file tokens.txt
```

## Example Output
```
Token: 0x1234...abcd (SCAM)
Safety Score: 23/100 ⚠️ HIGH RISK

❌ Honeypot detected — cannot sell
❌ Owner can pause trading
⚠️  Max transaction: 0.1% of supply
✅ Ownership renounced
✅ Liquidity locked (Unicrypt)
```

## License
MIT