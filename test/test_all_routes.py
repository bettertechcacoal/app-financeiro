# -*- coding: utf-8 -*-
"""
Script para testar todas as rotas do sistema
"""
import requests
import sys

# Criar sessão
session = requests.Session()
BASE_URL = "http://localhost:5000"

print("="*60)
print("TESTE DE TODAS AS ROTAS DO SISTEMA")
print("="*60)

# 1. Login
print("\n[1] Testando Login...")
login_response = session.post(
    f"{BASE_URL}/login",
    data={"email": "demo@demo.com", "password": "demo123"},
    allow_redirects=False,
    timeout=5
)

if login_response.status_code == 302 and 'dashboard' in login_response.headers.get('Location', ''):
    print("[OK] Login bem-sucedido")
else:
    print(f"[ERRO] Login falhou - Status: {login_response.status_code}")
    sys.exit(1)

# Rotas para testar
routes = [
    ("/admin/dashboard", "Dashboard"),
    ("/admin/clients", "Lista de Clientes"),
    ("/admin/clients/new", "Novo Cliente"),
    ("/admin/tickets", "Lista de Tickets"),
    ("/admin/integrations", "Integracoes"),
    ("/admin/integrations/movidesk", "Opcoes Movidesk"),
    ("/admin/travels", "Lista de Viagens"),
    ("/admin/travels/new", "Nova Viagem"),
    ("/admin/profile", "Perfil"),
]

# Testar cada rota
print("\n" + "="*60)
print("TESTANDO ROTAS PROTEGIDAS")
print("="*60)

failed_routes = []
for route, name in routes:
    try:
        response = session.get(f"{BASE_URL}{route}", timeout=5)
        if response.status_code == 200:
            print(f"[OK] {name:30} - {route}")
        else:
            print(f"[ERRO] {name:30} - Status {response.status_code}")
            failed_routes.append((route, name, response.status_code))
    except Exception as e:
        print(f"[ERRO] {name:30} - Erro: {str(e)}")
        failed_routes.append((route, name, str(e)))

# Testar APIs
print("\n" + "="*60)
print("TESTANDO APIs")
print("="*60)

apis = [
    ("/admin/api/organizations", "API Organizacoes"),
    ("/admin/api/clients", "API Clientes"),
    ("/admin/api/clients/unlinked", "API Clientes Nao Vinculados"),
]

for route, name in apis:
    try:
        response = session.get(f"{BASE_URL}{route}", timeout=5)
        if response.status_code == 200:
            print(f"[OK] {name:30} - {route}")
        else:
            print(f"[ERRO] {name:30} - Status {response.status_code}")
            failed_routes.append((route, name, response.status_code))
    except Exception as e:
        print(f"[ERRO] {name:30} - Erro: {str(e)}")
        failed_routes.append((route, name, str(e)))

# Resumo
print("\n" + "="*60)
print("RESUMO DOS TESTES")
print("="*60)
print(f"Total de rotas testadas: {len(routes) + len(apis)}")
print(f"Rotas com sucesso: {len(routes) + len(apis) - len(failed_routes)}")
print(f"Rotas com falha: {len(failed_routes)}")

if failed_routes:
    print("\n[FALHAS DETECTADAS]")
    for route, name, error in failed_routes:
        print(f"  - {name}: {route}")
        print(f"    Erro: {error}")
else:
    print("\n[SUCESSO] Todas as rotas estao funcionando!")

print("\n" + "="*60)
