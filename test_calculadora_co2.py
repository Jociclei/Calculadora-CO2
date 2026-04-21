"""
Testes unitários — Calculadora de Pegada de Carbono CO₂
"""

import unittest
from calculadora_co2 import (
    calcular_transporte,
    calcular_energia,
    calcular_alimentacao,
    calcular_residuos,
    calcular_compensacao,
    calcular_pegada_total,
    FATORES,
)


class TestTransporte(unittest.TestCase):
    def test_carro_gasolina(self):
        resultado = calcular_transporte({"carro_gasolina": 100})
        esperado  = round(100 * FATORES["carro_gasolina"], 3)
        self.assertAlmostEqual(resultado["total_mensal_kg"], esperado)

    def test_aviao_converte_para_mensal(self):
        resultado = calcular_transporte({"aviao_nacional": 1200})
        esperado  = round(1200 * FATORES["aviao_nacional"] / 12, 3)
        self.assertAlmostEqual(resultado["total_mensal_kg"], esperado)

    def test_sem_dados_retorna_zero(self):
        self.assertEqual(calcular_transporte({})["total_mensal_kg"], 0.0)

    def test_multiplos_meios(self):
        dados = {"carro_gasolina": 200, "onibus": 50, "metro_trem": 100}
        resultado = calcular_transporte(dados)
        self.assertGreater(resultado["total_mensal_kg"], 0)
        self.assertEqual(len(resultado["itens"]), 3)


class TestEnergia(unittest.TestCase):
    def test_eletricidade(self):
        resultado = calcular_energia({"eletricidade_kwh": 200})
        esperado  = round(200 * FATORES["eletricidade_brasil"], 3)
        self.assertAlmostEqual(resultado["total_mensal_kg"], esperado)

    def test_gas_natural(self):
        resultado = calcular_energia({"gas_m3": 10})
        # 10 m³ * 10.55 kWh/m³ * fator
        esperado  = round(10 * 10.55 * FATORES["gas_natural_kwh"], 3)
        self.assertAlmostEqual(resultado["total_mensal_kg"], esperado)

    def test_sem_dados(self):
        self.assertEqual(calcular_energia({})["total_mensal_kg"], 0.0)


class TestAlimentacao(unittest.TestCase):
    def test_carne_bovina(self):
        resultado = calcular_alimentacao({"carne_bovina": 4})
        self.assertAlmostEqual(resultado["total_mensal_kg"], round(4 * FATORES["carne_bovina"], 3))

    def test_dieta_vegana_menor_emissao(self):
        carnivoro = calcular_alimentacao({"carne_bovina": 5, "frango": 3})
        vegano    = calcular_alimentacao({"leguminosas": 5, "vegetais": 3, "frutas": 2})
        self.assertGreater(carnivoro["total_mensal_kg"], vegano["total_mensal_kg"])

    def test_todos_alimentos(self):
        dados = {k: 1.0 for k in ["carne_bovina", "carne_suina", "frango", "peixe",
                                   "ovos", "laticinios", "leguminosas", "vegetais", "frutas"]}
        resultado = calcular_alimentacao(dados)
        self.assertEqual(len(resultado["itens"]), 9)


class TestResiduos(unittest.TestCase):
    def test_sem_reciclagem(self):
        resultado = calcular_residuos({"lixo_total_kg": 20, "percentual_reciclagem": 0})
        esperado  = round(20 * FATORES["lixo_aterro"], 3)
        self.assertAlmostEqual(resultado["total_mensal_kg"], esperado, places=2)

    def test_reciclagem_total(self):
        resultado = calcular_residuos({"lixo_total_kg": 20, "percentual_reciclagem": 100})
        esperado  = round(20 * FATORES["lixo_reciclado"], 3)
        self.assertAlmostEqual(resultado["total_mensal_kg"], esperado, places=2)

    def test_reciclagem_parcial(self):
        sem = calcular_residuos({"lixo_total_kg": 20, "percentual_reciclagem": 0})
        com = calcular_residuos({"lixo_total_kg": 20, "percentual_reciclagem": 50})
        self.assertGreater(sem["total_mensal_kg"], com["total_mensal_kg"])


class TestCompensacao(unittest.TestCase):
    def test_zero_arvores(self):
        resultado = calcular_compensacao(0)
        self.assertEqual(resultado["absorcao_mensal_kg"], 0.0)

    def test_arvores(self):
        resultado = calcular_compensacao(10)
        esperado  = round(10 * FATORES["arvore_plantada"] / 12, 3)
        self.assertAlmostEqual(resultado["absorcao_mensal_kg"], esperado)

    def test_absorcao_anual(self):
        resultado = calcular_compensacao(5)
        self.assertAlmostEqual(resultado["absorcao_anual_kg"],
                               resultado["absorcao_mensal_kg"] * 12, places=1)


class TestPegadaTotal(unittest.TestCase):
    def _pegada_basica(self):
        t = calcular_transporte({"carro_gasolina": 100})
        e = calcular_energia({"eletricidade_kwh": 200})
        a = calcular_alimentacao({"carne_bovina": 4})
        r = calcular_residuos({"lixo_total_kg": 10, "percentual_reciclagem": 20})
        return t, e, a, r

    def test_soma_correta(self):
        t, e, a, r = self._pegada_basica()
        pegada = calcular_pegada_total(t, e, a, r)
        esperado = round(t["total_mensal_kg"] + e["total_mensal_kg"] +
                         a["total_mensal_kg"] + r["total_mensal_kg"], 2)
        self.assertEqual(pegada["total_mensal_kg"], esperado)

    def test_anual_e_doze_vezes_mensal(self):
        t, e, a, r = self._pegada_basica()
        pegada = calcular_pegada_total(t, e, a, r)
        self.assertAlmostEqual(pegada["total_anual_kg"], pegada["total_mensal_kg"] * 12, places=1)

    def test_nivel_critico(self):
        t = calcular_transporte({"aviao_internacional": 50000})
        e = calcular_energia({"eletricidade_kwh": 0})
        a = calcular_alimentacao({})
        r = calcular_residuos({})
        pegada = calcular_pegada_total(t, e, a, r)
        self.assertIn("Crítico", pegada["nivel"])

    def test_compensacao_reduz_saldo(self):
        t, e, a, r = self._pegada_basica()
        sem_comp = calcular_pegada_total(t, e, a, r)
        comp     = calcular_compensacao(50)
        com_comp = calcular_pegada_total(t, e, a, r, comp)
        self.assertLess(com_comp["saldo_mensal_kg"], sem_comp["saldo_mensal_kg"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
