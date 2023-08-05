#!/usr/bin/env python3

from typing import Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport
from ew_dsb_client_lib.gql.gql_service import GQLService
from ew_dsb_client_lib.auth.auth_service import AuthService
from ew_dsb_client_lib.channel.channel_service import ChannelService
from ew_dsb_client_lib.message.message_service import MessageService

class DSBClient:
    __gql_client:GQLService
    auth: AuthService
    channel: ChannelService
    message: MessageService

    def __init__(self, **kwargs):
        self.__gql_client = GQLService(**kwargs)

        self.auth = AuthService(self.__gql_client)
        self.channel = ChannelService(self.__gql_client)
        self.message = MessageService(self.__gql_client)

    def update(self, **kwargs):
        self.__gql_client.update(**kwargs)

        self.auth = AuthService(self.__gql_client)
        self.channel = ChannelService(self.__gql_client)
        self.message = MessageService(self.__gql_client)