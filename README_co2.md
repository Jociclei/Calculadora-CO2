# 🌍 CO2 Calculator — Calculadora de Pegada de Carbono

> Calcule, entenda e reduza suas emissões de CO₂ com Python puro.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Testes](https://img.shields.io/badge/Testes-20%20passed-brightgreen)](#-testes)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green)](LICENSE)

---

## 📋 Sobre o Projeto

A **CO2 Calculator** é uma ferramenta educacional e prática que permite calcular a **pegada de carbono** de pessoas ou empresas com base em quatro categorias principais de emissão:

| Categoria | O que calcula |
|-----------|--------------|
| 🚗 Transporte | Carro, moto, ônibus, metrô, avião |
| ⚡ Energia | Eletricidade e gás natural |
| 🥩 Alimentação | 9 grupos alimentares |
| 🗑️ Resíduos | Lixo com impacto da reciclagem |

O sistema também calcula a **compensação de CO₂** por árvores plantadas e compara o resultado com a **meta do Acordo de Paris** e a **média brasileira**.

---

## 🏗️ Arquitetura

```
co2-calculator/
│
├── calculadora_co2.py      # Módulo principal
│   ├── FATORES             # Dicionário de fatores de emissão
│   ├── calcular_transporte()
│   ├── calcular_energia()
│   ├── calcular_alimentacao()
│   ├── calcular_residuos()
│   ├── calcular_compensacao()
│   ├── calcular_pegada_total()
│   ├── gerar_relatorio()
│   ├── menu_interativo()   # Modo padrão (terminal)
│   └── modo_cli()          # Modo JSON via stdin
│
├── test_calculadora_co2.py # 20 testes unitários
├── exemplo_entrada.json    # Exemplo de entrada para modo CLI
└── README.md
```

---

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa necessária

```bash
git clone https://github.com/seu-usuario/co2-calculator.git
cd co2-calculator
```

### Modo Interativo (menu no terminal)

```bash
python calculadora_co2.py
```

O programa guia você pelas perguntas passo a passo e exibe o relatório ao final, com opção de salvar em arquivo `.txt`.

### Modo CLI (automação via JSON)

Ideal para scripts, pipelines e integrações:

```bash
cat exemplo_entrada.json | python calculadora_co2.py --cli
```

Ou com dados inline:

```bash
echo '{"nome":"Ana","transporte":{"carro_gasolina":200},"energia":{"eletricidade_kwh":150},"alimentacao":{"carne_bovina":3},"residuos":{"lixo_total_kg":15,"percentual_reciclagem":40},"arvores":5}' \
  | python calculadora_co2.py --cli
```

**Estrutura do JSON de entrada:**

```json
{
  "nome": "João Silva",
  "transporte": {
    "carro_gasolina": 300,
    "carro_etanol": 0,
    "carro_eletrico": 0,
    "moto": 0,
    "onibus": 50,
    "metro_trem": 0,
    "aviao_nacional": 2000,
    "aviao_internacional": 0
  },
  "energia": {
    "eletricidade_kwh": 250,
    "gas_m3": 5
  },
  "alimentacao": {
    "carne_bovina": 4,
    "frango": 3,
    "ovos": 1.5,
    "laticinios": 5,
    "leguminosas": 2,
    "vegetais": 3,
    "frutas": 2
  },
  "residuos": {
    "lixo_total_kg": 20,
    "percentual_reciclagem": 30
  },
  "arvores": 10
}
```

---

## 📊 Exemplo de Saída

```
════════════════════════════════════════════════════════════
  🌍  RELATÓRIO DE PEGADA DE CARBONO
════════════════════════════════════════════════════════════
  Pessoa/Empresa : João Silva
  Gerado em      : 15/06/2024 14:32
════════════════════════════════════════════════════════════

📌 TRANSPORTE
────────────────────────────────────────────────────────────
  Carro (gasolina)               300.00 km/mês        →    63.000 kg CO₂/mês
  Avião (nacional)              2000.00 km/ano        →    26.333 kg CO₂/mês
  SUBTOTAL                                                  89.333 kg CO₂/mês

📌 ENERGIA
────────────────────────────────────────────────────────────
  Eletricidade                   250.00 kWh/mês       →    18.750 kg CO₂/mês
  Gás Natural                      5.00 m³/mês        →    10.655 kg CO₂/mês
  SUBTOTAL                                                  29.405 kg CO₂/mês

...

════════════════════════════════════════════════════════════
  📊  RESUMO CONSOLIDADO
────────────────────────────────────────────────────────────
  Total mensal              :     254.32 kg CO₂
  Total anual               :    3051.84 kg CO₂
  Total anual               :       3.052 t CO₂
────────────────────────────────────────────────────────────
  🌱 Árvores plantadas       :         10 árvores
  Absorção mensal           :      18.33 kg CO₂
  SALDO (emissão - absorção):     235.99 kg CO₂/mês
────────────────────────────────────────────────────────────
  Nível de emissão          :  🟡 Médio
  Média brasileira (anual)  :        2.1 t CO₂
  Meta Acordo de Paris      :        2.0 t CO₂
  ⚠  Você emite 1.052 t acima da meta de Paris.
════════════════════════════════════════════════════════════
```

---

## 🧮 Fatores de Emissão

Os fatores foram baseados em fontes reconhecidas internacionalmente:

| Fonte | Uso |
|-------|-----|
| [IPCC AR6 (2022)](https://www.ipcc.ch/report/ar6/wg3/) | Alimentação, aviação |
| [EPA (EUA)](https://www.epa.gov/ghgemissions) | Transporte terrestre |
| [SEEG Brasil (2023)](https://seeg.eco.br/) | Eletricidade (fator SIN), média brasileira |
| [GHG Protocol](https://ghgprotocol.org/) | Gás natural, resíduos |

---

## 🧪 Testes

O projeto inclui **20 testes unitários** cobrindo todos os módulos de cálculo:

```bash
python test_calculadora_co2.py
```

```
Ran 20 tests in 0.002s
OK
```

**Cobertura dos testes:**
- ✅ Transporte (4 testes) — carro, avião com conversão anual→mensal, múltiplos meios
- ✅ Energia (3 testes) — eletricidade, gás natural, entrada vazia
- ✅ Alimentação (3 testes) — carne bovina, comparativo vegano vs carnívoro, todos os grupos
- ✅ Resíduos (3 testes) — sem reciclagem, reciclagem total, parcial
- ✅ Compensação (3 testes) — zero árvores, cálculo mensal, relação anual
- ✅ Pegada Total (4 testes) — soma, conversão anual, nível crítico, efeito da compensação

---

## 🌱 Níveis de Emissão

| Nível | Saldo mensal | Orientação |
|-------|-------------|-----------|
| 🟢 Baixo | ≤ 100 kg CO₂ | Parabéns! Continue assim. |
| 🟡 Médio | 101 – 300 kg CO₂ | Algumas mudanças podem ajudar. |
| 🟠 Alto | 301 – 600 kg CO₂ | Recomendada revisão de hábitos. |
| 🔴 Crítico | > 600 kg CO₂ | Ação urgente necessária. |

> **Meta do Acordo de Paris:** 2,0 t CO₂/pessoa/ano até 2050  
> **Média brasileira:** 2,1 t CO₂/pessoa/ano (SEEG 2023)

---

## 💡 Como Contribuir

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-categoria`
3. Adicione seus testes em `test_calculadora_co2.py`
4. Faça commit: `git commit -m "feat: adiciona cálculo de categoria X"`
5. Abra um Pull Request

**Ideias para contribuição:**
- Novos fatores de emissão (combustíveis industriais, pecuária)
- Suporte a múltiplos países (fatores de eletricidade locais)
- Exportação em CSV/PDF
- Interface web com Flask ou Streamlit

---

## 📄 Licença

MIT License — veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<p align="center">
  Feito com 💚 para um planeta mais sustentável
</p>
