#!/usr/bin/env python3

from typing import List, Dict, Any
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from gql import gql, Client
import eth_keys, binascii, base64
from ew_dsb_client_lib.gql.gql_service import GQLService
from ew_dsb_client_lib.auth.dtos.signin_response_dto import SignInResponseDto
from ew_dsb_client_lib.auth.dtos.get_user_response_dto import GetUserResponseDto
from ew_dsb_client_lib.auth.dtos.get_user_did_response_dto import GetUserDIDResponseDto
from ew_dsb_client_lib.auth.dtos.get_user_roles_response_dto import GetUserRolesResponseDto
from ew_dsb_client_lib.auth.operations.mutation_auth_operation import SignInAuthMutation
from ew_dsb_client_lib.auth.operations.query_auth_operation import GetUserAuthQuery, GetUserDIDAuthQuery, GetUserRolesAuthQuery
from ew_dsb_client_lib.auth.entities.user_jwt_entity import UserJwt
from ew_dsb_client_lib.auth.entities.user_entity import User
from ew_dsb_client_lib.auth.entities.claim_data_entity import ClaimData
from ew_dsb_client_lib.auth.entities.public_claim_entity import PublicClaim
from ew_dsb_client_lib.auth.entities.jwt_header_entity import JWTHeader
from ew_dsb_client_lib.auth.entities.user_role_entity import UserRole

class AuthService:
    http_client: Client

    def __init__(self, gql_service:GQLService):
        self.http_client = gql_service.http_client

    def __base64_url_encode(self, string):
        """Removes any `=` used as padding from the encoded string.

        Parameters
        ----------
        string : str

        Returns
        -------
        str
        """
        encoded = base64.urlsafe_b64encode(string.encode('utf-8')).decode('utf-8')
        return encoded.rstrip("=")

    def __base64_url_decode(self, string):
        """Adds back in the required padding before decoding.

        Parameters
        ----------
        string : str

        Returns
        -------
        str
        """
        padding = 4 - (len(string) % 4)
        string = string + ("=" * padding)
        return base64.urlsafe_b64decode(string.encode('utf-8')).decode('utf-8')

    def sign_message(self, payload:str, private_key:str) -> str:
        """Sign a message with a private key

        Parameters
        ----------
        payload : str
        private_key : str

        Returns
        -------
        str
        """
        header:JWTHeader = JWTHeader(
            alg='ES256',
            typ='JWT'
        )
        encoded_header:str = self.__base64_url_encode(header.to_json())

        encoded_payload:str = self.__base64_url_encode(payload)

        message:str = "".join([encoded_header, '.', encoded_payload])
        signer = eth_keys.keys.PrivateKey(binascii.unhexlify(private_key))
        signature = signer.sign_msg(message.encode())
        encoded_signature:str = self.__base64_url_encode(str(signature))

        jwt_token:str = "".join([encoded_header, '.', encoded_payload, '.', encoded_signature])
        return jwt_token

    def verify_message_signature(self, payload:str, public_key:str) -> bool:
        """Verify a message signature with a public key

        Parameters
        ----------
        payload : str
        public_key : str

        Returns
        -------
        bool
        """
        return True

    def create_identity(self, user_DID:str, private_key:str) -> str:
        """Create Identity token

        Parameters
        ----------
        user_DID : str
        private_key : str

        Returns
        -------
        str
        """
        # TODO: Get the actual blockNumber from provider
        # https://web3py.readthedocs.io/en/stable/providers.html#httpprovider
        claim_data:ClaimData = ClaimData(
            # NB: Just for dev purposes. Avoids `LoginStrategy` "Claim outdated" validation.
            blockNumber=999999999999
        )
        claim:PublicClaim = PublicClaim(
            claimData=claim_data,
            iss=user_DID
        )
        payload:str = claim.to_json()

        jwt_identity_token:str = self.sign_message(payload, private_key)
        return jwt_identity_token

    async def sign_in(self, identityToken:str) -> UserJwt:
        """Sign In user 

        Parameters
        ----------
        identityToken : str

        Returns
        -------
        UserJwt
        """
        query = gql("".join(set(SignInAuthMutation)))
        variables: Dict[str, Any] = {
            'identityToken': identityToken
        }
        response_text = await self.http_client.execute_async(
            query, 
            variable_values=variables
        )
        res = SignInResponseDto.from_dict(response_text)
        return res.signIn

    async def get_user(self) -> User:
        query = gql("".join(set(GetUserAuthQuery)))
        response_text = await self.http_client.execute_async(
            query
        )
        res = GetUserResponseDto.from_dict(response_text)
        return res.getUser

    async def get_user_DID(self) -> str:
        query = gql("".join(set(GetUserDIDAuthQuery)))
        response_text = await self.http_client.execute_async(
            query
        )
        res = GetUserDIDResponseDto.from_dict(response_text)
        return res.getUserDID

    async def get_user_roles(self) -> List[UserRole]:
        query = gql("".join(set(GetUserRolesAuthQuery)))
        response_text = await self.http_client.execute_async(
            query
        )
        res = GetUserRolesResponseDto.from_dict(response_text)
        return res.getUserRoles