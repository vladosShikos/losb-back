from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExpectedCredentials:
    email: str
    password: str


@dataclass
class AuthToken:
    access: str
    refresh: str
