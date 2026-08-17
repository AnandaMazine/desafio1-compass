"""
Demo 1 — Answer Relevancy: a resposta responde à pergunta?

Execute:  python demo_01_relevancia.py
"""

from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from juiz import obter_juiz

JUIZ = obter_juiz()

PERGUNTA = "Qual protetor solar você indica para pele oleosa?"

RESPOSTAS = {
    "resposta boa": (
        "Recomendo o Protetor Solar Facial FPS 60 Toque Seco da Kaia: "
        "ele foi feito para pele oleosa e custa R$ 69,90."
    ),
    "resposta ruim": (
        "Nossa loja abre de segunda a sábado! 😊 "
        "Aproveite para conhecer a nossa linha de batons."
    ),
}

for nome, resposta in RESPOSTAS.items():
    caso = LLMTestCase(input=PERGUNTA, actual_output=resposta)
    metrica = AnswerRelevancyMetric(threshold=0.7, model=JUIZ)
    metrica.measure(caso)
    status = "PASSOU" if metrica.is_successful() else "FALHOU"
    print(f"\n[{nome}] {status} — score: {metrica.score:.2f} (threshold 0.7)")
    print(f"Motivo do juiz: {metrica.reason}")
