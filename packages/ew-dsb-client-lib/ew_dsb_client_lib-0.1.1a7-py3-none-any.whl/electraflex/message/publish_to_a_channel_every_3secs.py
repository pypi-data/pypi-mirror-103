#!/usr/bin/env python3

import asyncio
import logging
import logging.config
import os
import random

import pendulum
from electraflex.message.entities.battery_payload_entity import BatteryPayload
from electraflex.message.schemas.battery_schema import BATTERY_MESSAGE_SCHEMA
from ew_dsb_client_lib.auth.entities.user_jwt_entity import UserJwt
from ew_dsb_client_lib.dsb_client_lib import DSBClient
from ew_dsb_client_lib.message.dtos.operation_message_dto import \
    PublishMessageDto
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

async def publish_to_a_channel():
    # CEGASA Battery Fully Qualified Channel Name
    fqcn:str = 'cegasabattery.channels.electraflex.apps.energyweb.iam.ewc'
    CEGASA_DID:str = os.getenv('CEGASA_DID')
    timestamp:int = pendulum.now().int_timestamp
    measured_power:float = float("{0:.2f}".format(random.uniform(2.7, 3.5))) 
    state_of_charge:float = float("{0:.2f}".format(random.uniform(0.8, 0.95))) 

    payload:BatteryPayload = BatteryPayload(
        asset_did=CEGASA_DID,
        timestamp=timestamp,
        online=True,
        measured_power=measured_power,
        state_of_charge=state_of_charge,
    )
    json_payload = payload.to_json()
    
    try:
        # Validate message schema
        validate(instance=payload.to_dict(), schema=BATTERY_MESSAGE_SCHEMA)
        # Verify message sigature
        private_key:str = await dsbClient.channel.find_private_key(fqcn)
        signature:str = dsbClient.crypto.sign(json_payload, private_key)
        # Publish Message   
        publish_message_dto = PublishMessageDto(
            fqcn,
            json_payload,
            signature
        )
        published:bool = await dsbClient.message.publish(publish_message_dto)
        logger.debug('Message put in channel - '+ fqcn + ' - ' + str(published))
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
    user_DID:str = os.getenv('CEGASA_DID')
    private_key:str = os.getenv('CEGASA_PRIVATE_KEY')
    # Sign In User
    identity_token:str = create_identity(user_DID, private_key)
    
    user_jwt:UserJwt = await sign_in_user(identity_token)
    dsbClient.update(bearer_token=user_jwt.token)
    
    while(True):
        # Publish message to channel
        await publish_to_a_channel()
        await asyncio.sleep(delay=3)

asyncio.run(main())
