from app.chain.runnable import Runnable, RunnableLambda, RunnableSequence


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