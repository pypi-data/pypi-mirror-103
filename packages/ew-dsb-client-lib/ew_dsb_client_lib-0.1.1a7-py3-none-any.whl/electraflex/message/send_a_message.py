#!/usr/bin/env python3

import os
import logging
import logging.config
import asyncio
import pendulum
from py_dotenv import read_dotenv
from jsonschema import validate
from ew_dsb_client_lib.dsb_client_lib import DSBClient
from ew_dsb_client_lib.auth.entities.user_jwt_entity import UserJwt
from ew_dsb_client_lib.message.dtos.operation_message_dto import SendMessageDto
from electraflex.message.schemas.battery_switch_schema import BATTERY_SWITCH_MESSAGE_SCHEMA
from electraflex.message.entities.battery_switch_payload_entity import BatterySwitchPayload

# Setup logger
log_file_path = os.path.join(os.path.abspath('./'), 'logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('dsb_service')

# Read dotenv
dotenv_path = os.path.join(os.path.abspath('./'), '.env')
read_dotenv(dotenv_path)

# Create a DSB Client instance
dsbClient:DSBClient = DSBClient()

async def send_a_message():
    # CEGASA Battery DID
    CEGASA_DID:str = 'did:ethr:0xf17f52151EbEF6C7334FAD080c5704D77216b732'
    recipientDID:str = '{}.channels.electraflex.apps.energyweb.iam.ewc'.format(CEGASA_DID)
    timestamp:int = pendulum.now().int_timestamp
    payload:BatterySwitchPayload = BatterySwitchPayload(
        asset_did=CEGASA_DID,
        timestamp=timestamp,
        start_stop=True,
    )
    json_payload = payload.to_json()

    try:
        # Validate message schema
        validate(instance=payload.to_dict(), schema=BATTERY_SWITCH_MESSAGE_SCHEMA)
        # Sign message    
        private_key:str = os.getenv('BAMBOO_ENERGY_PRIVATE_KEY')
        signature:str = dsbClient.crypto.sign(json_payload, private_key)
        # Send Message
        send_message_dto = SendMessageDto(
            recipientDID,
            json_payload,
            signature
        )
        sent:bool = await dsbClient.message.send(send_message_dto)
        logger.debug('Message sent to - '+ recipientDID + ' - ' + str(sent))
    except Exception as error:
        logger.error(error)

async def sign_in_user(identity_token:str) -> UserJwt:
    logger.debug('Sign In User')
    try:
        userJwt:UserJwt = await dsbClient.auth.sign_in(identity_token)
        # logger.debug(vars(userJwt))
        return userJwt
    except Exception as error:
        logger.error(error)

def create_identity( user_DID:str, private_key:str) -> str:
    logger.debug('Create an Identity Token')
    try:
        identity_token:str = dsbClient.auth.create_identity(user_DID, private_key)
        # logger.debug(vars(userJwt))
        return identity_token
    except Exception as error:
        logger.error(error)

async def main():
    # Sign In User
    user_DID:str = os.getenv('BAMBOO_ENERGY_DID')
    private_key:str = os.getenv('BAMBOO_ENERGY_PRIVATE_KEY')
    identity_token:str = create_identity(user_DID, private_key)
    
    user_jwt:UserJwt = await sign_in_user(identity_token)
    dsbClient.update(bearer_token=user_jwt.token)
    
    # Send a direct message
    await send_a_message()

asyncio.run(main())