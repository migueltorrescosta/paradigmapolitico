from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).parents[1]
CSV = pd.read_csv(ROOT / "paradigma_politico.csv", index_col="Pergunta")
QUESTIONS = CSV.index.tolist()
SHORT = CSV.index[CSV["Curto"] == 1].tolist()


@pytest.fixture
def app(monkeypatch):
    monkeypatch.chdir(ROOT)
    return AppTest.from_file(str(ROOT / "Home.py"), default_timeout=30).run()


def click(at, label_start):
    next(b for b in at.button if b.label.startswith(label_start)).click().run()


def answer(at, n):
    """Answers n questions with "Concordo totalmente" and returns them in the order asked."""
    asked = []
    for _ in range(n):
        asked.append(at.subheader[0].value)
        click(at, "Concordo totalmente")
    return asked


def assert_results(at):
    assert not at.exception
    assert at.success[0].value == "Teste concluído!"


def test_short_then_full_asks_every_question_once(app):
    click(app, "Iniciar Teste Curto")
    asked = answer(app, len(SHORT))
    assert asked == SHORT
    click(app, "Continuar Teste")
    asked += answer(app, len(QUESTIONS) - len(SHORT))
    assert sorted(asked) == sorted(QUESTIONS)
    assert len(asked) == len(set(asked))
    assert_results(app)


def test_short_only(app):
    click(app, "Iniciar Teste Curto")
    assert answer(app, len(SHORT)) == SHORT
    click(app, "Ver Resultados")
    assert_results(app)


def test_full_only(app):
    click(app, "Iniciar Teste Completo")
    asked = answer(app, len(QUESTIONS))
    assert sorted(asked) == sorted(QUESTIONS)
    assert len(asked) == len(set(asked))
    assert_results(app)
