from dataclasses import dataclass


@dataclass
class wallet:
    wallet_name: str
    wallet_address: str
    contract_address: str
    token_symbol: str
    trigger: float
    balance: float
    stake: bool
    user_id: int
