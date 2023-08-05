#!/usr/bin/env python3

import os
import logging
import logging.config
import asyncio
from py_dotenv import read_dotenv
from jsonschema import validate
from ew_dsb_client_lib.dsb_client_lib import DSBClient
from ew_dsb_client_lib.auth.entities.user_jwt_entity import UserJwt
from ew_dsb_client_lib.message.dtos.operation_message_dto import ReceiveMessageDto
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

async def receive_a_message():
    # CEGASA Battery DID
    CEGASA_DID:str = 'did:ethr:0xf17f52151EbEF6C7334FAD080c5704D77216b732'
    recipientDID:str = '{}.channels.electraflex.apps.energyweb.iam.ewc'.format(CEGASA_DID)
    # ReceiveMessageDto    
    receive_message_dto = ReceiveMessageDto(
        recipientDID,
    )
    # Subscription
    try:
        async for message in dsbClient.message.receive(receive_message_dto):
            json_payload:str = message.payload
            payload:BatterySwitchPayload = BatterySwitchPayload.from_json(json_payload)
            # Validate message schema
            validate(instance=payload.to_dict(), schema=BATTERY_SWITCH_MESSAGE_SCHEMA)
            # Verify message sigature
            public_key:str = os.getenv('BAMBOO_ENERGY_PUBLIC_KEY')
            dsbClient.crypto.verify_signature(json_payload, public_key)
            logger.debug(json_payload)
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
    user_DID:str = os.getenv('CEGASA_DID')
    private_key:str = os.getenv('CEGASA_PRIVATE_KEY')
    identity_token:str = create_identity(user_DID, private_key)
    
    user_jwt:UserJwt = await sign_in_user(identity_token)
    dsbClient.update(bearer_token=user_jwt.token)
    
    # Receive a direct message
    await receive_a_message()

asyncio.run(main())