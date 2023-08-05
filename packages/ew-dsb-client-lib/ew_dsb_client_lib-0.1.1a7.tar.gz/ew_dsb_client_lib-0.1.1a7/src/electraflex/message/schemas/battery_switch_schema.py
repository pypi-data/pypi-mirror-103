BATTERY_SWITCH_MESSAGE_SCHEMA: dict = {
    "type": "object",
    "anyOf": [
        { "required": ["asset_did"] },
        { "required": ["timestamp"] },
        { "required": ["start_stop"] },
    ],
    "properties": {
        "asset_did": {
            "type": "string"
        },
        "timestamp": {
            "type": "integer"
        },
        "start_stop": {
            "type": "boolean"
        },
    },
}