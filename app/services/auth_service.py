# -*- coding: utf-8 -*-
import requests
from typing import Optional, Dict, Any
from config import config


class AuthService:
    """Serviço para comunicação com o Auth Service"""

    def __init__(self):
        self.base_url = config.AUTH_SERVICE_URL
        self.timeout = config.AUTH_SERVICE_TIMEOUT

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


# Instância global do serviço
auth_service = AuthService()
