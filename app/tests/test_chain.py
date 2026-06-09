from app.chain.runnable import Runnable
import pandas as pd
from app.chain.steps import PromptBuilder, LLMRunner, LLMRunnerOutput, ResponseParser
from app.data.summary import QueryInput

class AddOne(Runnable[int, int]):
    def run(self, input: int) -> int:
        return input + 1

class Double(Runnable[int, int]):
    def run(self, input: int) -> int:
        return input * 2

# Runnable & Runnable
def test_runnable_or_runnable():
    chain = AddOne() | Double()
    assert chain.run(3) == 8  #(3+1)*2

# Runable & vanlig funktion
def test_runnable_or_function():
    chain = AddOne() | (lambda x: x * 2)
    assert chain.run(3) == 8  #(3+1)*2

# vanlig funktion & Runnable
def test_function_or_runnable():
    chain = (lambda x: x + 1) | Double()
    assert chain.run(3) == 8  #(3+1)*2

#Testar bygga prompt med fråga och data 
def test_prompt_builder():
    df = pd.DataFrame({
        "card_name": ["Luffy", "Zoro"],
        "card_color": ["Red", "Green"],
        "card_type": ["Character", "Character"],
        "market_price": [100.0, 50.0]
    })
    builder = PromptBuilder()
    result = builder.run(QueryInput(question="Vilket kort är dyrast?", df=df))
    assert "Vilket kort är dyrast?" in result.prompt
    assert "Luffy" in result.prompt

#Returnerar svar och frågan
def test_response_parser():
    parser = ResponseParser()
    result = parser.run(LLMRunnerOutput(
        raw_answer="  Luffy kostar 100 kr.  ",
        question="Hur mycket kostar Luffy?"
    ))
    assert result.answer == "Luffy kostar 100 kr."
    assert result.question == "Hur mycket kostar Luffy?"

def test_full_chain_mocked(monkeypatch):
    df = pd.DataFrame({
        "card_name": ["Luffy"],
        "card_color": ["Red"],
        "card_type": ["Character"],
        "market_price": [100.0]
    })

    def fake_run(self, input):
        return LLMRunnerOutput(
            raw_answer="Luffy kostar 100 kr.",
            question=input.question
        )

    monkeypatch.setattr(LLMRunner, "run", fake_run)

    chain = PromptBuilder() | LLMRunner() | ResponseParser()
    result = chain.run(QueryInput(question="Hur mycket kostar Luffy?", df=df))
    assert result.answer == "Luffy kostar 100 kr."