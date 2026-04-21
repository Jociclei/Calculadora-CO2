"""
CO2 Calculator - Calculadora de Emissões de Carbono
====================================================
Calcula a pegada de carbono pessoal e empresarial com base em
atividades cotidianas e gera relatório detalhado.
"""

import sys
from datetime import datetime


# ══════════════════════════════════════════════════════════════════════════════
# FATORES DE EMISSÃO (kg CO₂ por unidade)
# Fontes: IPCC, EPA, SEEG Brasil
# ══════════════════════════════════════════════════════════════════════════════

FATORES = {
    # Transporte (kg CO₂ por km)
    "carro_gasolina":      0.21,   # carro médio a gasolina
    "carro_etanol":        0.05,   # etanol (menor emissão líquida)
    "carro_eletrico":      0.07,   # elétrico (mix energético Brasil)
    "moto":                0.11,   # motocicleta média
    "onibus":              0.089,  # ônibus urbano (por passageiro/km)
    "metro_trem":          0.004,  # metrô/trem elétrico
    "aviao_nacional":      0.158,  # voo doméstico (por passageiro/km)
    "aviao_internacional": 0.195,  # voo internacional (por passageiro/km)

    # Energia (kg CO₂ por kWh)
    "eletricidade_brasil": 0.075,  # fator médio SIN (2023)
    "gas_natural_kwh":     0.202,  # gás natural residencial

    # Alimentação (kg CO₂ por kg de alimento)
    "carne_bovina":        27.0,
    "carne_suina":          7.6,
    "frango":               6.9,
    "peixe":                6.1,
    "ovos":                 4.5,
    "laticinios":           3.2,
    "leguminosas":          0.9,   # feijão, lentilha, grão-de-bico
    "vegetais":             0.4,
    "frutas":               0.5,

    # Resíduos (kg CO₂ por kg de resíduo)
    "lixo_aterro":          0.5,
    "lixo_reciclado":       0.02,

    # Compensação (kg CO₂ absorvido por árvore/ano)
    "arvore_plantada":     22.0,   # média árvore tropical adulta/ano
}


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE CÁLCULO
# ══════════════════════════════════════════════════════════════════════════════

def calcular_transporte(dados: dict) -> dict:
    """Calcula emissões de transporte em kg CO₂."""
    resultados = {}
    total = 0.0

    mapeamento = {
        "carro_gasolina":      ("Carro (gasolina)",      "km/mês"),
        "carro_etanol":        ("Carro (etanol)",        "km/mês"),
        "carro_eletrico":      ("Carro (elétrico)",      "km/mês"),
        "moto":                ("Moto",                  "km/mês"),
        "onibus":              ("Ônibus",                "km/mês"),
        "metro_trem":          ("Metrô/Trem",            "km/mês"),
        "aviao_nacional":      ("Avião (nacional)",      "km/ano"),
        "aviao_internacional": ("Avião (internacional)", "km/ano"),
    }

    for chave, (label, unidade) in mapeamento.items():
        valor = dados.get(chave, 0)
        if valor > 0:
            # Aviões: km/ano → converter para mensal
            fator_tempo = 1/12 if "aviao" in chave else 1
            emissao = valor * FATORES[chave] * (1 if "aviao" not in chave else 1/12)
            emissao_mensal = valor * FATORES[chave] * fator_tempo
            resultados[label] = {
                "valor": valor,
                "unidade": unidade,
                "emissao_mensal_kg": round(emissao_mensal, 3),
            }
            total += emissao_mensal

    return {"itens": resultados, "total_mensal_kg": round(total, 3)}


def calcular_energia(dados: dict) -> dict:
    """Calcula emissões de energia em kg CO₂."""
    resultados = {}
    total = 0.0

    kwh_eletrico = dados.get("eletricidade_kwh", 0)
    if kwh_eletrico > 0:
        emissao = kwh_eletrico * FATORES["eletricidade_brasil"]
        resultados["Eletricidade"] = {
            "valor": kwh_eletrico,
            "unidade": "kWh/mês",
            "emissao_mensal_kg": round(emissao, 3),
        }
        total += emissao

    m3_gas = dados.get("gas_m3", 0)
    if m3_gas > 0:
        # 1 m³ gás natural ≈ 10.55 kWh
        kwh_gas = m3_gas * 10.55
        emissao = kwh_gas * FATORES["gas_natural_kwh"]
        resultados["Gás Natural"] = {
            "valor": m3_gas,
            "unidade": "m³/mês",
            "emissao_mensal_kg": round(emissao, 3),
        }
        total += emissao

    return {"itens": resultados, "total_mensal_kg": round(total, 3)}


def calcular_alimentacao(dados: dict) -> dict:
    """Calcula emissões de alimentação em kg CO₂."""
    resultados = {}
    total = 0.0

    mapeamento = {
        "carne_bovina":  "Carne bovina",
        "carne_suina":   "Carne suína",
        "frango":        "Frango",
        "peixe":         "Peixe/frutos do mar",
        "ovos":          "Ovos",
        "laticinios":    "Laticínios",
        "leguminosas":   "Leguminosas",
        "vegetais":      "Vegetais",
        "frutas":        "Frutas",
    }

    for chave, label in mapeamento.items():
        valor = dados.get(chave, 0)
        if valor > 0:
            emissao = valor * FATORES[chave]
            resultados[label] = {
                "valor": valor,
                "unidade": "kg/mês",
                "emissao_mensal_kg": round(emissao, 3),
            }
            total += emissao

    return {"itens": resultados, "total_mensal_kg": round(total, 3)}


def calcular_residuos(dados: dict) -> dict:
    """Calcula emissões de resíduos em kg CO₂."""
    resultados = {}
    total = 0.0

    lixo_total   = dados.get("lixo_total_kg", 0)
    perc_recicla = dados.get("percentual_reciclagem", 0) / 100

    if lixo_total > 0:
        lixo_aterro   = lixo_total * (1 - perc_recicla)
        lixo_reciclado = lixo_total * perc_recicla

        emissao_aterro    = lixo_aterro   * FATORES["lixo_aterro"]
        emissao_reciclado = lixo_reciclado * FATORES["lixo_reciclado"]

        resultados["Lixo (aterro)"]   = {"valor": round(lixo_aterro, 2),    "unidade": "kg/mês", "emissao_mensal_kg": round(emissao_aterro, 3)}
        resultados["Lixo (reciclado)"] = {"valor": round(lixo_reciclado, 2), "unidade": "kg/mês", "emissao_mensal_kg": round(emissao_reciclado, 3)}
        total += emissao_aterro + emissao_reciclado

    return {"itens": resultados, "total_mensal_kg": round(total, 3)}


def calcular_compensacao(arvores: int) -> dict:
    """Calcula a compensação de CO₂ por árvores plantadas."""
    absorcao_anual  = arvores * FATORES["arvore_plantada"]
    absorcao_mensal = absorcao_anual / 12
    return {
        "arvores": arvores,
        "absorcao_mensal_kg": round(absorcao_mensal, 3),
        "absorcao_anual_kg":  round(absorcao_anual, 3),
    }


def calcular_pegada_total(transporte, energia, alimentacao, residuos, compensacao=None) -> dict:
    """Consolida todas as emissões e calcula o saldo."""
    total_mensal = (
        transporte["total_mensal_kg"] +
        energia["total_mensal_kg"] +
        alimentacao["total_mensal_kg"] +
        residuos["total_mensal_kg"]
    )
    total_anual = total_mensal * 12
    comp_mensal = compensacao["absorcao_mensal_kg"] if compensacao else 0
    saldo_mensal = total_mensal - comp_mensal

    # Classificação
    if saldo_mensal <= 100:
        nivel = "🟢 Baixo"
    elif saldo_mensal <= 300:
        nivel = "🟡 Médio"
    elif saldo_mensal <= 600:
        nivel = "🟠 Alto"
    else:
        nivel = "🔴 Crítico"

    return {
        "total_mensal_kg":     round(total_mensal, 2),
        "total_anual_kg":      round(total_anual, 2),
        "total_anual_toneladas": round(total_anual / 1000, 3),
        "compensacao_mensal_kg": round(comp_mensal, 2),
        "saldo_mensal_kg":     round(saldo_mensal, 2),
        "nivel":               nivel,
        "media_brasileira_anual_t": 2.1,  # toneladas CO₂/pessoa/ano (SEEG 2023)
        "meta_paris_anual_t":       2.0,  # meta Acordo de Paris 2050
    }


# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIO
# ══════════════════════════════════════════════════════════════════════════════

def gerar_relatorio(nome: str, transporte: dict, energia: dict,
                    alimentacao: dict, residuos: dict,
                    pegada: dict, compensacao: dict = None) -> str:
    """Gera um relatório textual formatado."""
    sep  = "═" * 60
    sep2 = "─" * 60
    linhas = []

    linhas.append(sep)
    linhas.append("  🌍  RELATÓRIO DE PEGADA DE CARBONO")
    linhas.append(sep)
    linhas.append(f"  Pessoa/Empresa : {nome}")
    linhas.append(f"  Gerado em      : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    linhas.append(sep)

    def bloco(titulo, categoria):
        linhas.append(f"\n📌 {titulo}")
        linhas.append(sep2)
        if not categoria["itens"]:
            linhas.append("  Nenhum dado informado.")
        else:
            for item, info in categoria["itens"].items():
                linhas.append(
                    f"  {item:<30} {info['valor']:>8.2f} {info['unidade']:<12}"
                    f"  →  {info['emissao_mensal_kg']:>8.3f} kg CO₂/mês"
                )
        linhas.append(f"  {'SUBTOTAL':<50} {categoria['total_mensal_kg']:>8.3f} kg CO₂/mês")

    bloco("TRANSPORTE",   transporte)
    bloco("ENERGIA",      energia)
    bloco("ALIMENTAÇÃO",  alimentacao)
    bloco("RESÍDUOS",     residuos)

    linhas.append(f"\n{'═'*60}")
    linhas.append("  📊  RESUMO CONSOLIDADO")
    linhas.append(sep2)
    linhas.append(f"  Total mensal              : {pegada['total_mensal_kg']:>10.2f} kg CO₂")
    linhas.append(f"  Total anual               : {pegada['total_anual_kg']:>10.2f} kg CO₂")
    linhas.append(f"  Total anual               : {pegada['total_anual_toneladas']:>10.3f} t CO₂")

    if compensacao:
        linhas.append(sep2)
        linhas.append(f"  🌱 Árvores plantadas       : {compensacao['arvores']:>10} árvores")
        linhas.append(f"  Absorção mensal           : {compensacao['absorcao_mensal_kg']:>10.2f} kg CO₂")
        linhas.append(f"  SALDO (emissão - absorção): {pegada['saldo_mensal_kg']:>10.2f} kg CO₂/mês")

    linhas.append(sep2)
    linhas.append(f"  Nível de emissão          :  {pegada['nivel']}")
    linhas.append(f"  Média brasileira (anual)  : {pegada['media_brasileira_anual_t']:>10.1f} t CO₂")
    linhas.append(f"  Meta Acordo de Paris      : {pegada['meta_paris_anual_t']:>10.1f} t CO₂")

    diff = pegada["total_anual_toneladas"] - pegada["meta_paris_anual_t"]
    if diff > 0:
        linhas.append(f"  ⚠  Você emite {diff:.3f} t acima da meta de Paris.")
    else:
        linhas.append(f"  ✅ Você está {abs(diff):.3f} t abaixo da meta de Paris!")

    linhas.append(sep)
    return "\n".join(linhas)


# ══════════════════════════════════════════════════════════════════════════════
# ENTRADA INTERATIVA
# ══════════════════════════════════════════════════════════════════════════════

def perguntar(prompt: str, padrao: float = 0.0) -> float:
    """Lê um número do usuário com valor padrão."""
    try:
        entrada = input(f"  {prompt} [{padrao}]: ").strip()
        return float(entrada) if entrada else padrao
    except ValueError:
        print("  ⚠  Valor inválido, usando 0.")
        return 0.0


def menu_interativo():
    print("\n" + "═"*60)
    print("  🌱  CALCULADORA DE PEGADA DE CARBONO CO₂")
    print("═"*60)
    nome = input("  Seu nome ou empresa: ").strip() or "Usuário"

    print("\n── TRANSPORTE (valores mensais, exceto aviões que são anuais) ─")
    transporte_dados = {
        "carro_gasolina":      perguntar("Carro gasolina       (km/mês)"),
        "carro_etanol":        perguntar("Carro etanol         (km/mês)"),
        "carro_eletrico":      perguntar("Carro elétrico       (km/mês)"),
        "moto":                perguntar("Moto                 (km/mês)"),
        "onibus":              perguntar("Ônibus               (km/mês)"),
        "metro_trem":          perguntar("Metrô/Trem           (km/mês)"),
        "aviao_nacional":      perguntar("Avião nacional       (km/ano)"),
        "aviao_internacional": perguntar("Avião internacional  (km/ano)"),
    }

    print("\n── ENERGIA ────────────────────────────────────────────────────")
    energia_dados = {
        "eletricidade_kwh": perguntar("Eletricidade         (kWh/mês)"),
        "gas_m3":           perguntar("Gás natural          (m³/mês)"),
    }

    print("\n── ALIMENTAÇÃO (kg consumidos por mês) ────────────────────────")
    alim_dados = {
        "carne_bovina": perguntar("Carne bovina         (kg/mês)"),
        "carne_suina":  perguntar("Carne suína          (kg/mês)"),
        "frango":       perguntar("Frango               (kg/mês)"),
        "peixe":        perguntar("Peixe/frutos do mar  (kg/mês)"),
        "ovos":         perguntar("Ovos                 (kg/mês)"),
        "laticinios":   perguntar("Laticínios           (kg/mês)"),
        "leguminosas":  perguntar("Leguminosas          (kg/mês)"),
        "vegetais":     perguntar("Vegetais             (kg/mês)"),
        "frutas":       perguntar("Frutas               (kg/mês)"),
    }

    print("\n── RESÍDUOS ───────────────────────────────────────────────────")
    res_dados = {
        "lixo_total_kg":          perguntar("Total de lixo        (kg/mês)"),
        "percentual_reciclagem":  perguntar("% reciclado          (0-100) "),
    }

    print("\n── COMPENSAÇÃO ────────────────────────────────────────────────")
    arvores = int(perguntar("Árvores já plantadas (quantidade)"))

    # Cálculos
    transporte  = calcular_transporte(transporte_dados)
    energia     = calcular_energia(energia_dados)
    alimentacao = calcular_alimentacao(alim_dados)
    residuos    = calcular_residuos(res_dados)
    compensacao = calcular_compensacao(arvores) if arvores > 0 else None
    pegada      = calcular_pegada_total(transporte, energia, alimentacao, residuos, compensacao)

    relatorio = gerar_relatorio(nome, transporte, energia, alimentacao, residuos, pegada, compensacao)
    print("\n" + relatorio)

    # Salvar relatório
    salvar = input("\n  Salvar relatório em arquivo? (s/N): ").strip().lower()
    if salvar == "s":
        nome_arquivo = f"relatorio_co2_{nome.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(relatorio)
        print(f"  ✅ Relatório salvo em: {nome_arquivo}")


# ══════════════════════════════════════════════════════════════════════════════
# MODO CLI (STDIN/STDOUT para scripts e testes)
# ══════════════════════════════════════════════════════════════════════════════

def modo_cli():
    """
    Uso: python calculadora_co2.py --cli
    Lê JSON de transporte/energia/alimentação/resíduos do stdin e imprime resultado.
    """
    import json
    dados = json.loads(sys.stdin.read())
    nome        = dados.get("nome", "Usuário")
    transporte  = calcular_transporte(dados.get("transporte", {}))
    energia     = calcular_energia(dados.get("energia", {}))
    alimentacao = calcular_alimentacao(dados.get("alimentacao", {}))
    residuos    = calcular_residuos(dados.get("residuos", {}))
    arvores     = dados.get("arvores", 0)
    compensacao = calcular_compensacao(arvores) if arvores > 0 else None
    pegada      = calcular_pegada_total(transporte, energia, alimentacao, residuos, compensacao)
    relatorio   = gerar_relatorio(nome, transporte, energia, alimentacao, residuos, pegada, compensacao)
    print(relatorio)


if __name__ == "__main__":
    if "--cli" in sys.argv:
        modo_cli()
    else:
        menu_interativo()
