BATTERY_MESSAGE_SCHEMA: dict = {
    "type": "object",
    "anyOf": [
        { "required": ["asset_did"] },
        { "required": ["timestamp"] },
        { "required": ["online"] },
        { "required": ["measured_power"] },
        { "required": ["state_of_charge"] },
    ],
    "properties": {
        "asset_did": {
            "type": "string"
        },
        "timestamp": {
            "type": "integer"
        },
        "online": {
            "type": "boolean"
        },
        "measured_power": {
            "type": "number"
        },
        "state_of_charge": {
            "type": "number"
        },
    },
}