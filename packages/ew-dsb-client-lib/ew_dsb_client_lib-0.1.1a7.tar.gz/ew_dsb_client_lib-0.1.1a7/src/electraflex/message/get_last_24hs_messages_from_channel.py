#!/usr/bin/env python3

import asyncio
import logging
import logging.config
import os
from typing import List

import pendulum
from ew_dsb_client_lib.auth.entities.user_jwt_entity import UserJwt
from ew_dsb_client_lib.dsb_client_lib import DSBClient
from electraflex.message.entities.battery_payload_entity import \
    BatteryPayload
from electraflex.message.schemas.battery_schema import \
    BATTERY_MESSAGE_SCHEMA
from ew_dsb_client_lib.message.dtos.operation_message_dto import \
    FindAllMessagesDto
from ew_dsb_client_lib.message.entities.message_entity import Message
from jsonschema import validate
from py_dotenv import read_dotenv

# Setup logger
log_file_path = os.path.join(os.path.abspath('./'), 'logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('dsb_service')

# Read dotenv
dotenv_path = os.path.join(os.path.abspath('./'), '.env')
read_dotenv(dotenv_path)

# Create a DSB Client instance
dsbClient:DSBClient = DSBClient()

async def get_last_24hs_messages_from_channel():
    fqcn = 'cegasabattery.channels.electraflex.apps.energyweb.iam.ewc'
    now = pendulum.now()
    yesterday = now.subtract(hours=24)
    # FindAllMessagesDto
    find_all_messages_dto = FindAllMessagesDto(
        fqcn=fqcn,
        take=5,
        skip=0,
        startDate=yesterday.int_timestamp,
        endDate=now.int_timestamp
    )
    # Query
    logger.debug('Last 24hs messages from channel - '+ fqcn)
    try:
        last_24hs_messages:List[Message] = await dsbClient.message.find_all(find_all_messages_dto)
        for message in last_24hs_messages:
            json_payload:str = message.payload
            payload:BatteryPayload = BatteryPayload.from_json(json_payload)
            # Validate message schema
            validate(instance=payload.to_dict(), schema=BATTERY_MESSAGE_SCHEMA)
            # Verify message sigature
            public_key:str = await dsbClient.channel.find_public_key(fqcn)
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
    user_DID:str = os.getenv('BAMBOO_ENERGY_DID')
    private_key:str = os.getenv('BAMBOO_ENERGY_PRIVATE_KEY')
    identity_token:str = create_identity(user_DID, private_key)
    
    user_jwt:UserJwt = await sign_in_user(identity_token)
    dsbClient.update(bearer_token=user_jwt.token)
    
    # Get last 24hs messages
    await get_last_24hs_messages_from_channel()

asyncio.run(main())
