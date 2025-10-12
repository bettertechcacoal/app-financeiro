# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com clientes municipais de Rondônia
"""
import sys
import os

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.client import Client
from app.models.city import City


def seed_clients():
    """Popula o banco com clientes municipais de Rondônia"""

    db = SessionLocal()

    try:
        # Buscar cidades do banco de dados para obter os IDs
        cities = db.query(City).all()
        cities_dict = {city.name: city.id for city in cities}

        print(f"[INFO] {len(cities_dict)} cidades carregadas do banco de dados\n")
        # Definir clientes municipais
        clients_data = [
            # Alta Floresta d'Oeste
            {
                'name': 'Prefeitura Municipal de Alta Floresta d\'Oeste',
                'email': 'contato@prefeituraftaflorestarondonia.com.br',
                'phone': '(69) 3641-1234',
                'document': '04.394.824/0001-19',
                'city': 'Alta Floresta d\'Oeste',
                'state': 'RO',
                'address': 'Av. Principal, Centro',
                'zipcode': '76954-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Alta Floresta d\'Oeste',
                'email': 'contato@camaraaltafloresta.ro.gov.br',
                'phone': '(69) 3641-1235',
                'document': '04.394.825/0001-98',
                'city': 'Alta Floresta d\'Oeste',
                'state': 'RO',
                'address': 'Rua das Flores, Centro',
                'zipcode': '76954-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'SAAE - Alta Floresta d\'Oeste',
                'email': 'saae@altafloresta.ro.gov.br',
                'phone': '(69) 3641-1236',
                'document': '04.394.826/0001-77',
                'city': 'Alta Floresta d\'Oeste',
                'state': 'RO',
                'address': 'Av. das Águas, Centro',
                'zipcode': '76954-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Cacoal
            {
                'name': 'Prefeitura Municipal de Cacoal',
                'email': 'gabinete@cacoal.ro.gov.br',
                'phone': '(69) 3441-1234',
                'document': '04.092.714/0001-28',
                'city': 'Cacoal',
                'state': 'RO',
                'address': 'Av. Porto Velho, Centro',
                'zipcode': '76963-900',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Cacoal',
                'email': 'contato@camaracacoal.ro.gov.br',
                'phone': '(69) 3441-1235',
                'document': '04.092.715/0001-07',
                'city': 'Cacoal',
                'state': 'RO',
                'address': 'Rua dos Vereadores, Centro',
                'zipcode': '76963-900',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Castanheiras
            {
                'name': 'Prefeitura Municipal de Castanheiras',
                'email': 'prefeitura@castanheiras.ro.gov.br',
                'phone': '(69) 3535-1234',
                'document': '63.762.493/0001-92',
                'city': 'Castanheiras',
                'state': 'RO',
                'address': 'Av. Governador Jorge Teixeira, Centro',
                'zipcode': '76.976-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Castanheiras',
                'email': 'camara@castanheiras.ro.gov.br',
                'phone': '(69) 3535-1235',
                'document': '63.762.494/0001-71',
                'city': 'Castanheiras',
                'state': 'RO',
                'address': 'Rua Legislativa, Centro',
                'zipcode': '76.976-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Instituto de Previdência de Castanheiras',
                'email': 'previdencia@castanheiras.ro.gov.br',
                'phone': '(69) 3535-1236',
                'document': '63.762.495/0001-50',
                'city': 'Castanheiras',
                'state': 'RO',
                'address': 'Av. das Castanheiras, Centro',
                'zipcode': '76.976-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Ministro Andreazza
            {
                'name': 'Prefeitura Municipal de Ministro Andreazza',
                'email': 'prefeitura@ministroanreazza.ro.gov.br',
                'phone': '(69) 3530-1234',
                'document': '63.762.850/0001-44',
                'city': 'Ministro Andreazza',
                'state': 'RO',
                'address': 'Av. Tancredo Neves, Centro',
                'zipcode': '76919-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Ministro Andreazza',
                'email': 'camara@ministroanreazza.ro.gov.br',
                'phone': '(69) 3530-1235',
                'document': '63.762.851/0001-23',
                'city': 'Ministro Andreazza',
                'state': 'RO',
                'address': 'Rua dos Vereadores, Centro',
                'zipcode': '76919-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Nova Brasilândia d'Oeste
            {
                'name': 'Prefeitura Municipal de Nova Brasilândia d\'Oeste',
                'email': 'prefeitura@novabrasilandia.ro.gov.br',
                'phone': '(69) 3418-1234',
                'document': '63.761.903/0001-66',
                'city': 'Nova Brasilandia d\'Oeste',
                'state': 'RO',
                'address': 'Av. Presidente Médici, Centro',
                'zipcode': '76958-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Nova Brasilândia d\'Oeste',
                'email': 'camara@novabrasilandia.ro.gov.br',
                'phone': '(69) 3418-1235',
                'document': '63.761.904/0001-45',
                'city': 'Nova Brasilandia d\'Oeste',
                'state': 'RO',
                'address': 'Rua do Legislativo, Centro',
                'zipcode': '76958-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'SAAE - Nova Brasilândia d\'Oeste',
                'email': 'saae@novabrasilandia.ro.gov.br',
                'phone': '(69) 3418-1236',
                'document': '63.761.905/0001-24',
                'city': 'Nova Brasilandia d\'Oeste',
                'state': 'RO',
                'address': 'Av. Saneamento, Centro',
                'zipcode': '76958-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Rio Crespo
            {
                'name': 'Prefeitura Municipal de Rio Crespo',
                'email': 'prefeitura@riocrespo.ro.gov.br',
                'phone': '(69) 3538-1234',
                'document': '63.763.081/0001-14',
                'city': 'Rio Crespo',
                'state': 'RO',
                'address': 'Av. Brasil, Centro',
                'zipcode': '76.927-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Rio Crespo',
                'email': 'camara@riocrespo.ro.gov.br',
                'phone': '(69) 3538-1235',
                'document': '63.763.082/0001-03',
                'city': 'Rio Crespo',
                'state': 'RO',
                'address': 'Rua Parlamentar, Centro',
                'zipcode': '76.927-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Rolim de Moura
            {
                'name': 'Prefeitura Municipal de Rolim de Moura',
                'email': 'gabinete@rolim.ro.gov.br',
                'phone': '(69) 3442-1234',
                'document': '04.394.577/0001-05',
                'city': 'Rolim de Moura',
                'state': 'RO',
                'address': 'Av. 25 de Agosto, Centro',
                'zipcode': '76940-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Rolim de Moura',
                'email': 'contato@camararolim.ro.gov.br',
                'phone': '(69) 3442-1235',
                'document': '04.394.578/0001-94',
                'city': 'Rolim de Moura',
                'state': 'RO',
                'address': 'Rua dos Vereadores, Centro',
                'zipcode': '76940-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Instituto de Previdência de Rolim de Moura',
                'email': 'previdencia@rolim.ro.gov.br',
                'phone': '(69) 3442-1236',
                'document': '04.394.579/0001-73',
                'city': 'Rolim de Moura',
                'state': 'RO',
                'address': 'Av. Previdência, Centro',
                'zipcode': '76940-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # São Felipe d'Oeste
            {
                'name': 'Prefeitura Municipal de São Felipe d\'Oeste',
                'email': 'prefeitura@saofelipe.ro.gov.br',
                'phone': '(69) 3625-1234',
                'document': '15.990.326/0001-90',
                'city': 'Sao Felipe d\'Oeste',
                'state': 'RO',
                'address': 'Av. São Paulo, Centro',
                'zipcode': '76.977-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de São Felipe d\'Oeste',
                'email': 'camara@saofelipe.ro.gov.br',
                'phone': '(69) 3625-1235',
                'document': '15.990.327/0001-79',
                'city': 'Sao Felipe d\'Oeste',
                'state': 'RO',
                'address': 'Rua do Poder Legislativo, Centro',
                'zipcode': '76.977-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # São Miguel do Guaporé
            {
                'name': 'Prefeitura Municipal de São Miguel do Guaporé',
                'email': 'prefeitura@saomiguel.ro.gov.br',
                'phone': '(69) 3616-1234',
                'document': '63.761.786/0001-50',
                'city': 'Sao Miguel do Guapore',
                'state': 'RO',
                'address': 'Av. Principal, Centro',
                'zipcode': '76932-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de São Miguel do Guaporé',
                'email': 'camara@saomiguel.ro.gov.br',
                'phone': '(69) 3616-1235',
                'document': '63.761.787/0001-39',
                'city': 'Sao Miguel do Guapore',
                'state': 'RO',
                'address': 'Rua Legislativa, Centro',
                'zipcode': '76932-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Seringueiras
            {
                'name': 'Prefeitura Municipal de Seringueiras',
                'email': 'prefeitura@seringueiras.ro.gov.br',
                'phone': '(69) 3545-1234',
                'document': '15.990.409/0001-27',
                'city': 'Seringueiras',
                'state': 'RO',
                'address': 'Av. Getúlio Vargas, Centro',
                'zipcode': '76.934-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Seringueiras',
                'email': 'camara@seringueiras.ro.gov.br',
                'phone': '(69) 3545-1235',
                'document': '15.990.410/0001-95',
                'city': 'Seringueiras',
                'state': 'RO',
                'address': 'Rua dos Vereadores, Centro',
                'zipcode': '76.934-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Fundo de Previdência de Seringueiras',
                'email': 'previdencia@seringueiras.ro.gov.br',
                'phone': '(69) 3545-1236',
                'document': '15.990.411/0001-74',
                'city': 'Seringueiras',
                'state': 'RO',
                'address': 'Av. Previdenciária, Centro',
                'zipcode': '76.934-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Urupá
            {
                'name': 'Prefeitura Municipal de Urupá',
                'email': 'prefeitura@urupa.ro.gov.br',
                'phone': '(69) 3414-1234',
                'document': '15.990.450/0001-06',
                'city': 'Urupa',
                'state': 'RO',
                'address': 'Av. Marechal Rondon, Centro',
                'zipcode': '76.929-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Urupá',
                'email': 'camara@urupa.ro.gov.br',
                'phone': '(69) 3414-1235',
                'document': '15.990.451/0001-95',
                'city': 'Urupa',
                'state': 'RO',
                'address': 'Rua Câmara, Centro',
                'zipcode': '76.929-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Vale do Anari
            {
                'name': 'Prefeitura Municipal de Vale do Anari',
                'email': 'prefeitura@valedoanari.ro.gov.br',
                'phone': '(69) 3534-1234',
                'document': '15.990.472/0001-56',
                'city': 'Vale do Anari',
                'state': 'RO',
                'address': 'Av. dos Pioneiros, Centro',
                'zipcode': '76.867-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Vale do Anari',
                'email': 'camara@valedoanari.ro.gov.br',
                'phone': '(69) 3534-1235',
                'document': '15.990.473/0001-35',
                'city': 'Vale do Anari',
                'state': 'RO',
                'address': 'Rua Legislativo, Centro',
                'zipcode': '76.867-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },

            # Vilhena
            {
                'name': 'Prefeitura Municipal de Vilhena',
                'email': 'gabinete@vilhena.ro.gov.br',
                'phone': '(69) 3321-1234',
                'document': '04.092.714/0001-43',
                'city': 'Vilhena',
                'state': 'RO',
                'address': 'Av. Capitão Castro, Centro',
                'zipcode': '76980-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Câmara Municipal de Vilhena',
                'email': 'contato@camaravilhena.ro.gov.br',
                'phone': '(69) 3321-1235',
                'document': '04.092.715/0001-22',
                'city': 'Vilhena',
                'state': 'RO',
                'address': 'Rua Alagoas, Centro',
                'zipcode': '76980-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'SAAE - Vilhena',
                'email': 'saae@vilhena.ro.gov.br',
                'phone': '(69) 3321-1236',
                'document': '04.092.716/0001-01',
                'city': 'Vilhena',
                'state': 'RO',
                'address': 'Av. Saneamento, Jardim América',
                'zipcode': '76980-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
            {
                'name': 'Instituto de Previdência de Vilhena',
                'email': 'previdencia@vilhena.ro.gov.br',
                'phone': '(69) 3321-1237',
                'document': '04.092.717/0001-90',
                'city': 'Vilhena',
                'state': 'RO',
                'address': 'Rua Pernambuco, Centro',
                'zipcode': '76980-000',
                'billing_cycle_type': 'mensal',
                'billing_day': 10
            },
        ]

        created_count = 0
        existing_count = 0
        updated_count = 0

        for client_data in clients_data:
            # Verifica se o cliente ja existe pelo CNPJ
            existing_client = db.query(Client).filter_by(document=client_data['document']).first()

            # Buscar o ID da cidade
            city_id = cities_dict.get(client_data['city'])
            if not city_id:
                print(f"  [AVISO] Cidade não encontrada: {client_data['city']} - Cliente: {client_data['name']}")
                continue

            if not existing_client:
                # Criar novo cliente
                client = Client(
                    name=client_data['name'],
                    email=client_data['email'],
                    phone=client_data['phone'],
                    document=client_data['document'],
                    city_id=city_id,
                    state=client_data['state'],
                    address=client_data['address'],
                    zipcode=client_data['zipcode'],
                    billing_cycle_type=client_data.get('billing_cycle_type'),
                    billing_day=client_data.get('billing_day'),
                    billing_cycle=client_data.get('billing_cycle'),
                    fixed_start_day=client_data.get('fixed_start_day')
                )
                db.add(client)
                created_count += 1
                print(f"  [OK] Cliente criado: {client_data['name']}")
            else:
                # Atualizar cliente existente
                existing_client.name = client_data['name']
                existing_client.email = client_data['email']
                existing_client.phone = client_data['phone']
                existing_client.city_id = city_id
                existing_client.state = client_data['state']
                existing_client.address = client_data['address']
                existing_client.zipcode = client_data['zipcode']
                existing_client.billing_cycle_type = client_data.get('billing_cycle_type')
                existing_client.billing_day = client_data.get('billing_day')
                existing_client.billing_cycle = client_data.get('billing_cycle')
                existing_client.fixed_start_day = client_data.get('fixed_start_day')
                updated_count += 1
                print(f"  [OK] Cliente atualizado: {client_data['name']}")

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Clientes criados: {created_count}")
        print(f"Clientes atualizados: {updated_count}")
        print(f"Total de clientes processados: {len(clients_data)}")
        print(f"{'='*60}\n")

        # Mostrar resumo por cidade
        print("Resumo por Cidade:")
        print("  - Alta Floresta d'Oeste: 3 clientes (Prefeitura, Câmara, SAAE)")
        print("  - Cacoal: 2 clientes (Prefeitura, Câmara)")
        print("  - Castanheiras: 3 clientes (Prefeitura, Câmara, Instituto Previdência)")
        print("  - Ministro Andreazza: 2 clientes (Prefeitura, Câmara)")
        print("  - Nova Brasilândia d'Oeste: 3 clientes (Prefeitura, Câmara, SAAE)")
        print("  - Rio Crespo: 2 clientes (Prefeitura, Câmara)")
        print("  - Rolim de Moura: 3 clientes (Prefeitura, Câmara, Instituto Previdência)")
        print("  - São Felipe d'Oeste: 2 clientes (Prefeitura, Câmara)")
        print("  - São Miguel do Guaporé: 2 clientes (Prefeitura, Câmara)")
        print("  - Seringueiras: 3 clientes (Prefeitura, Câmara, Fundo Previdência)")
        print("  - Urupá: 2 clientes (Prefeitura, Câmara)")
        print("  - Vale do Anari: 2 clientes (Prefeitura, Câmara)")
        print("  - Vilhena: 4 clientes (Prefeitura, Câmara, SAAE, Instituto Previdência)")
        print()

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar seeder: {str(e)}\n")
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEEDER: Clientes Municipais de Rondônia")
    print("="*60 + "\n")
    seed_clients()
