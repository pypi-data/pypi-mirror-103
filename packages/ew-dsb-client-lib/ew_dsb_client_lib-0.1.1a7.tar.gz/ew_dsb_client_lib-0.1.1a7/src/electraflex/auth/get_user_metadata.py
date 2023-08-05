#!/usr/bin/env python3

import asyncio
import logging
import logging.config
import os

from ew_dsb_client_lib.auth.entities.user_entity import User
from ew_dsb_client_lib.auth.entities.user_jwt_entity import UserJwt
from ew_dsb_client_lib.dsb_client_lib import DSBClient
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

async def get_user_metadata():
    # Query
    logger.debug('Get User Metadata')
    try:
        user:User = await dsbClient.auth.get_user()
        logger.debug(user.to_json())
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
    user_DID:str = os.getenv('BAMBOO_ENERGY_DID')
    private_key:str = os.getenv('BAMBOO_ENERGY_PRIVATE_KEY')
    # Sign In User
    identity_token:str = create_identity(user_DID, private_key)
    
    user_jwt:UserJwt = await sign_in_user(identity_token)
    dsbClient.update(bearer_token=user_jwt.token)

    await get_user_metadata()

asyncio.run(main())
