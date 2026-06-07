from pydantic import BaseModel
from transformers import pipeline as hf_pipeline
from app.chain.runnable import Runnable
from app.data.summary import summarize, QueryInput


class PromptBuilderOutput(BaseModel):
    prompt: str
    question: str


class LLMRunnerOutput(BaseModel):
    raw_answer: str
    question: str


class ResponseParserOutput(BaseModel):
    question: str
    answer: str
    model: str = "HuggingFaceTB/SmolLM2-135M-Instruct"


class PromptBuilder(Runnable[QueryInput, PromptBuilderOutput]):
    def run(self, input: QueryInput) -> PromptBuilderOutput:
        system = (
            "Du är en expert på One Piece Trading Card Game."
            "Svara kort på svenska."
            "Basera endast ditt svar på den data du får."
        )
        data = summarize(input.df)
        prompt = f"{system}\n\nData:\n{data}\n\nFråga: {input.question}"
        return PromptBuilderOutput(
            prompt=prompt,
            question=input.question
        )


class LLMRunner(Runnable[PromptBuilderOutput, LLMRunnerOutput]):
    def __init__(self):
        super().__init__()
        self.pipe = hf_pipeline(
            "text-generation",
            model="HuggingFaceTB/SmolLM2-135M-Instruct",
        )

    def run(self, input: PromptBuilderOutput) -> LLMRunnerOutput:
        messages = [{"role": "user", "content": input.prompt}]
        result = self.pipe(messages, max_new_tokens=200)
        raw = result[0]["generated_text"][-1]["content"]
        return LLMRunnerOutput(
            raw_answer=raw,
            question=input.question,
        )


class ResponseParser(Runnable[LLMRunnerOutput, ResponseParserOutput]):
    def run(self, input: LLMRunnerOutput) -> ResponseParserOutput:
        raw = input.raw_answer.strip()
        first_sentence = raw.split(".")[0] + "."
        return ResponseParserOutput(
            question=input.question,
            answer=first_sentence
        )