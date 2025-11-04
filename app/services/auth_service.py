# -*- coding: utf-8 -*-
import requests
from typing import Optional, Dict, Any
from config import AUTH_SERVICE_URL, AUTH_SERVICE_TIMEOUT


class AuthService:
    """Serviço para comunicação com o Auth Service"""

    def __init__(self):
        self.base_url = AUTH_SERVICE_URL
        self.timeout = AUTH_SERVICE_TIMEOUT

    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Realiza login via auth-service

        Args:
            email: Email do usuário
            password: Senha do usuário

        Returns:
            Dict com tokens e dados do usuário ou None em caso de erro
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"email": email, "password": password},
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com auth-service: {e}")
            return None

    def validate_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Valida um access token via auth-service

        Args:
            access_token: Token JWT a ser validado

        Returns:
            Dict com dados do usuário ou None se token inválido
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/token/validate",
                json={"access_token": access_token},
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com auth-service: {e}")
            return None

    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Busca informações do usuário via auth-service

        Args:
            access_token: Access token do usuário

        Returns:
            Dict com dados do usuário ou None em caso de erro
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com auth-service: {e}")
            return None

    def register_user(self, user_data: Dict[str, Any], password: str) -> Optional[Dict[str, Any]]:
        """
        Registra um novo usuário no auth-service com UUID

        Args:
            user_data: Dados do usuário (deve conter sid_uuid, name, email)
            password: Senha do usuário

        Returns:
            Dict com resposta do auth-service ou None em caso de erro
        """
        try:
            payload = {
                "uuid": user_data.get('sid_uuid'),  # Mapeia sid_uuid para uuid
                "name": user_data.get('name'),
                "email": user_data.get('email'),
                "password": password,
                "phone": user_data.get('phone'),
                "avatar": user_data.get('avatar')
            }

            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json=payload,
                timeout=self.timeout
            )

            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Erro ao registrar usuário no auth-service: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com auth-service: {e}")
            return None

    def change_password(self, user_uuid: str, new_password: str) -> Optional[Dict[str, Any]]:
        """
        Altera a senha de um usuário no auth-service

        Args:
            user_uuid: UUID do usuário (sid_uuid)
            new_password: Nova senha do usuário

        Returns:
            Dict com resposta do auth-service ou None em caso de erro
        """
        try:
            payload = {
                "uuid": user_uuid,
                "password": new_password
            }

            response = requests.put(
                f"{self.base_url}/api/auth/change-password",
                json=payload,
                timeout=self.timeout
            )

            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Erro ao alterar senha no auth-service: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com auth-service: {e}")
            return None


# Instância global do serviço
auth_service = AuthService()
