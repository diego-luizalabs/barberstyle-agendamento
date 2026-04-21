"""
airtable_integration.py
========================
Script de integração com a API do Airtable para o projeto BarberStyle.
Disciplina: Padrões Web para No Code e Low Code – UniFECAF

Funcionalidades:
    - Listar agendamentos cadastrados via formulário no site Webflow
    - Filtrar agendamentos por data
    - Criar novo agendamento via linha de comando
    - Exportar agendamentos para CSV
"""

import os
import json
import csv
import requests
from datetime import datetime
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# Carrega variáveis de ambiente do arquivo .env
# ─────────────────────────────────────────────
load_dotenv()

AIRTABLE_API_KEY  = os.getenv("AIRTABLE_API_KEY",  "sua_chave_aqui")
AIRTABLE_BASE_ID  = os.getenv("AIRTABLE_BASE_ID",  "appXXXXXXXXXXXXXX")
AIRTABLE_TABLE    = os.getenv("AIRTABLE_TABLE_NAME", "Agendamentos")

BASE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type":  "application/json",
}

# ─────────────────────────────────────────────
# Dados de exemplo (usados quando a API não está
# configurada, para fins de demonstração)
# ─────────────────────────────────────────────
MOCK_DATA = [
    {
        "id": "rec001",
        "fields": {
            "Nome":     "Carlos Souza",
            "Telefone": "(11) 99123-4567",
            "Servico":  "Corte + Barba",
            "Data":     "2025-06-10",
            "Hora":     "10:00",
            "Status":   "Confirmado",
        },
    },
    {
        "id": "rec002",
        "fields": {
            "Nome":     "Rafael Lima",
            "Telefone": "(11) 98765-4321",
            "Servico":  "Corte Degradê",
            "Data":     "2025-06-10",
            "Hora":     "11:30",
            "Status":   "Pendente",
        },
    },
    {
        "id": "rec003",
        "fields": {
            "Nome":     "Lucas Pereira",
            "Telefone": "(11) 91234-5678",
            "Servico":  "Barba Completa",
            "Data":     "2025-06-11",
            "Hora":     "09:00",
            "Status":   "Confirmado",
        },
    },
    {
        "id": "rec004",
        "fields": {
            "Nome":     "Fernanda Martins",
            "Telefone": "(11) 97654-3210",
            "Servico":  "Corte Feminino",
            "Data":     "2025-06-12",
            "Hora":     "14:00",
            "Status":   "Cancelado",
        },
    },
]


# ══════════════════════════════════════════════
#  FUNÇÕES DE API
# ══════════════════════════════════════════════

def listar_agendamentos(filtro_data: str = None) -> list:
    """
    Busca todos os agendamentos na base do Airtable.
    Se filtro_data for informado (formato YYYY-MM-DD), filtra por data.

    Em modo demonstração (sem chave real), retorna dados mockados.
    """
    # Modo demonstração
    if AIRTABLE_API_KEY == "sua_chave_aqui":
        print("⚠️  Modo demonstração: usando dados fictícios (configure o .env para usar a API real)\n")
        dados = MOCK_DATA
        if filtro_data:
            dados = [r for r in dados if r["fields"].get("Data") == filtro_data]
        return dados

    # Modo real
    params = {}
    if filtro_data:
        params["filterByFormula"] = f"{{Data}}='{filtro_data}'"

    try:
        resposta = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
        resposta.raise_for_status()
        return resposta.json().get("records", [])
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP: {e.response.status_code} – {e.response.text}")
        return []
    except requests.exceptions.ConnectionError:
        print("❌ Sem conexão com a internet. Verificar rede.")
        return []


def criar_agendamento(nome: str, telefone: str, servico: str, data: str, hora: str) -> dict | None:
    """
    Cria um novo registro de agendamento na base do Airtable.
    Retorna o registro criado ou None em caso de erro.
    """
    if AIRTABLE_API_KEY == "sua_chave_aqui":
        print("⚠️  Modo demonstração: agendamento NÃO foi enviado à API.\n")
        registro = {
            "id": f"rec{len(MOCK_DATA)+1:03d}",
            "fields": {
                "Nome":     nome,
                "Telefone": telefone,
                "Servico":  servico,
                "Data":     data,
                "Hora":     hora,
                "Status":   "Pendente",
            },
        }
        MOCK_DATA.append(registro)
        return registro

    payload = {
        "fields": {
            "Nome":     nome,
            "Telefone": telefone,
            "Servico":  servico,
            "Data":     data,
            "Hora":     hora,
            "Status":   "Pendente",
        }
    }

    try:
        resposta = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=10)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro ao criar agendamento: {e.response.status_code} – {e.response.text}")
        return None


def exportar_csv(agendamentos: list, caminho: str = "agendamentos.csv") -> None:
    """
    Exporta lista de agendamentos para um arquivo CSV.
    """
    if not agendamentos:
        print("Nenhum agendamento para exportar.")
        return

    campos = ["id", "Nome", "Telefone", "Servico", "Data", "Hora", "Status"]

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for registro in agendamentos:
            linha = {"id": registro["id"]}
            linha.update(registro["fields"])
            writer.writerow(linha)

    print(f"✅ Exportado para '{caminho}' ({len(agendamentos)} registros).")


# ══════════════════════════════════════════════
#  FUNÇÕES DE APRESENTAÇÃO
# ══════════════════════════════════════════════

STATUS_EMOJI = {
    "Confirmado": "✅",
    "Pendente":   "⏳",
    "Cancelado":  "❌",
}

def imprimir_agendamentos(agendamentos: list) -> None:
    """Exibe os agendamentos de forma legível no terminal."""
    if not agendamentos:
        print("Nenhum agendamento encontrado.")
        return

    print(f"\n{'─'*60}")
    print(f"{'📅 AGENDAMENTOS – BARBEARIA ESTILO CERTO':^60}")
    print(f"{'─'*60}")

    for reg in agendamentos:
        f = reg["fields"]
        emoji = STATUS_EMOJI.get(f.get("Status", ""), "❓")
        print(
            f"\n  {emoji} {f.get('Nome', 'N/A')}"
            f"\n     Serviço : {f.get('Servico', 'N/A')}"
            f"\n     Data/Hr : {f.get('Data', 'N/A')} às {f.get('Hora', 'N/A')}"
            f"\n     Tel.    : {f.get('Telefone', 'N/A')}"
            f"\n     Status  : {f.get('Status', 'N/A')}"
        )

    print(f"\n{'─'*60}")
    print(f"  Total: {len(agendamentos)} agendamento(s) encontrado(s).")
    print(f"{'─'*60}\n")


# ══════════════════════════════════════════════
#  MENU INTERATIVO
# ══════════════════════════════════════════════

def menu() -> None:
    print("\n╔══════════════════════════════════════╗")
    print("║   BarberStyle – Gestão de Agenda     ║")
    print("╠══════════════════════════════════════╣")
    print("║  1. Listar todos os agendamentos     ║")
    print("║  2. Filtrar por data                 ║")
    print("║  3. Criar novo agendamento           ║")
    print("║  4. Exportar para CSV                ║")
    print("║  0. Sair                             ║")
    print("╚══════════════════════════════════════╝")


def main() -> None:
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            agendamentos = listar_agendamentos()
            imprimir_agendamentos(agendamentos)

        elif opcao == "2":
            data_str = input("Informe a data (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(data_str, "%Y-%m-%d")
            except ValueError:
                print("❌ Formato inválido. Use YYYY-MM-DD.")
                continue
            agendamentos = listar_agendamentos(filtro_data=data_str)
            imprimir_agendamentos(agendamentos)

        elif opcao == "3":
            print("\n── Novo Agendamento ──")
            nome     = input("Nome do cliente : ").strip()
            telefone = input("Telefone        : ").strip()
            print("Serviços disponíveis: Corte, Barba, Corte + Barba, Corte Degradê, Barba Completa, Corte Feminino")
            servico  = input("Serviço         : ").strip()
            data     = input("Data (YYYY-MM-DD): ").strip()
            hora     = input("Hora (HH:MM)    : ").strip()

            registro = criar_agendamento(nome, telefone, servico, data, hora)
            if registro:
                print(f"\n✅ Agendamento criado com ID: {registro['id']}")

        elif opcao == "4":
            agendamentos = listar_agendamentos()
            exportar_csv(agendamentos)

        elif opcao == "0":
            print("👋 Encerrando. Até mais!")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")


# ── Ponto de entrada ──────────────────────────
if __name__ == "__main__":
    main()
