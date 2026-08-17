"""
Demo 4 — Tudo junto como suíte pytest.

Execute:  deepeval test run demo_04_pytest.py

Cada função de teste vira um item da suíte — a mesma mecânica dos testes
automatizados do mês 2.
"""

from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from juiz import obter_juiz

JUIZ = obter_juiz()

CATALOGO = [
    "Protetor Solar Mineral FPS 45 — Bioraiz — pele sensível — R$ 82,00.",
    "Hidratante Facial Ultra — Vellure — pele seca — R$ 79,90 — "
    "ingredientes: ácido hialurônico, ceramidas, manteiga de karité.",
]


def test_relevancia_recomendacao():
    caso = LLMTestCase(
        input="Qual hidratante você indica para pele seca?",
        actual_output=(
            "Para pele seca, indico o Hidratante Facial Ultra da Vellure, "
            "com ácido hialurônico e ceramidas, por R$ 79,90."
        ),
    )
    assert_test(caso, [AnswerRelevancyMetric(threshold=0.7, model=JUIZ)])


def test_fidelidade_ao_catalogo():
    caso = LLMTestCase(
        input="Quanto custa o Protetor Solar Mineral FPS 45?",
        actual_output="O Protetor Solar Mineral FPS 45 da Bioraiz custa R$ 82,00.",
        retrieval_context=CATALOGO,
    )
    assert_test(caso, [FaithfulnessMetric(threshold=0.8, model=JUIZ)])


# Descomente para mostrar uma FALHA ao vivo (preço inventado):
# def test_fidelidade_falhando():
#     caso = LLMTestCase(
#         input="Quanto custa o Protetor Solar Mineral FPS 45?",
#         actual_output="Está em promoção por R$ 9,90, aproveite!",
#         retrieval_context=CATALOGO,
#     )
#     assert_test(caso, [FaithfulnessMetric(threshold=0.8, model=JUIZ)])
