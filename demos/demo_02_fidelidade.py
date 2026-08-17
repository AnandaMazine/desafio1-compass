"""
Demo 2 — Faithfulness: a resposta é fiel à fonte de verdade?

O retrieval_context é o trecho do catálogo. A métrica detecta quando o bot
inventa produto, preço ou ingrediente que não está na fonte.

Execute:  python demo_02_fidelidade.py
"""

from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from juiz import obter_juiz

JUIZ = obter_juiz()

PERGUNTA = "Quais protetores solares vocês têm para pele sensível?"

CATALOGO = [
    "Protetor Solar Mineral FPS 45 — Bioraiz — pele sensível — R$ 82,00 — "
    "ingredientes: óxido de zinco, dióxido de titânio, aloe vera.",
    "Protetor Solar Facial FPS 60 Toque Seco — Kaia — pele oleosa — R$ 69,90.",
]

RESPOSTAS = {
    "resposta fiel": (
        "Para pele sensível temos o Protetor Solar Mineral FPS 45 da Bioraiz, "
        "por R$ 82,00, com óxido de zinco e aloe vera na fórmula."
    ),
    "resposta inventada": (
        "Temos o Protetor Solar Mineral FPS 45 da Bioraiz por apenas R$ 19,90 "
        "e também o novíssimo Vellure Kids FPS 90, o queridinho das crianças!"
    ),
}

for nome, resposta in RESPOSTAS.items():
    caso = LLMTestCase(
        input=PERGUNTA,
        actual_output=resposta,
        retrieval_context=CATALOGO,
    )
    metrica = FaithfulnessMetric(threshold=0.8, model=JUIZ)
    metrica.measure(caso)
    status = "PASSOU" if metrica.is_successful() else "FALHOU"
    print(f"\n[{nome}] {status} — score: {metrica.score:.2f} (threshold 0.8)")
    print(f"Motivo do juiz: {metrica.reason}")
