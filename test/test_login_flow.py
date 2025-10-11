"""
Script para testar o fluxo de login completo
"""
import requests
import json

# Teste 1: Auth Service
print("="*60)
print("TESTE 1: Autenticação no Auth-Service")
print("="*60)

auth_url = "http://localhost:8000/api/auth/login"
auth_data = {
    "email": "demo@demo.com",
    "password": "demo123"
}

try:
    response = requests.post(auth_url, json=auth_data, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("\n[OK] Autenticacao no auth-service OK!")
        access_token = response.json().get('access_token')
    else:
        print("\n[ERRO] Falha na autenticacao no auth-service")
        exit(1)

except Exception as e:
    print(f"\n[ERRO] Erro ao conectar no auth-service: {e}")
    exit(1)

# Teste 2: Login na aplicação
print("\n" + "="*60)
print("TESTE 2: Login na Aplicação Flask")
print("="*60)

session = requests.Session()
login_url = "http://localhost:5000/login"
login_data = {
    "email": "demo@demo.com",
    "password": "demo123"
}

try:
    response = session.post(login_url, data=login_data, allow_redirects=False, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Location: {response.headers.get('Location', 'N/A')}")
    print(f"Cookies: {dict(session.cookies)}")

    if response.status_code == 302:
        redirect_location = response.headers.get('Location', '')
        if 'dashboard' in redirect_location or '/admin' in redirect_location:
            print("\n[OK] Login na aplicacao OK! Redirecionando para dashboard")
        else:
            print(f"\n[ERRO] Redirecionamento inesperado: {redirect_location}")
    else:
        print(f"\n[ERRO] Status code inesperado: {response.status_code}")

except Exception as e:
    print(f"\n[ERRO] Erro ao fazer login na aplicacao: {e}")
    exit(1)

# Teste 3: Acessar Dashboard
print("\n" + "="*60)
print("TESTE 3: Acessar Dashboard")
print("="*60)

try:
    dashboard_url = "http://localhost:5000/admin/dashboard"
    response = session.get(dashboard_url, timeout=5)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("\n[OK] Dashboard acessado com sucesso!")
        print(f"Tamanho da resposta: {len(response.text)} bytes")
    else:
        print(f"\n[ERRO] Falha ao acessar dashboard: {response.status_code}")

except Exception as e:
    print(f"\n[ERRO] Erro ao acessar dashboard: {e}")

print("\n" + "="*60)
print("TESTES CONCLUÍDOS")
print("="*60)
