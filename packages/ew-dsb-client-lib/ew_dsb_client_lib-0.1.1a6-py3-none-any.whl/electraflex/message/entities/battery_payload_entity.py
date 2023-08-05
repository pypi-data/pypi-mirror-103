#!/usr/bin/env python3

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

@dataclass(frozen=True)
class BatteryPayload(DataClassJsonMixin):
    asset_did: str
    timestamp: int
    online: bool
    measured_power: int
    state_of_charge: int