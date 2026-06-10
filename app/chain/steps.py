from pydantic import BaseModel
from transformers import pipeline as hf_pipeline
from app.chain.runnable import Runnable
from app.config import settings
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
    model: str = settings.model_id


class PromptBuilder(Runnable[QueryInput, PromptBuilderOutput]):
    def run(self, input: QueryInput) -> PromptBuilderOutput:
        system = (
            "Du är en expert på One Piece Trading Card Game. "
            "Svara direkt och koncist på frågan. "
            "Använd endast den data som ges. "
            "Svara på engelska."
        )
        data = summarize(input.df)
        prompt = (
            f"{system}\n\n"
            f"Data:\n{data}\n\n"
            f"Fråga: {input.question}\n"
            f"Svar:"
        )
        return PromptBuilderOutput(
            prompt=prompt,
            question=input.question
        )


class LLMRunner(Runnable[PromptBuilderOutput, LLMRunnerOutput]):
    def __init__(self):
        super().__init__()
        self.pipe = hf_pipeline("text-generation", 
        model=settings.model_id,
        token=settings.hf_token
        )

    def run(self, input: PromptBuilderOutput) -> LLMRunnerOutput:
        messages = [{"role": "user", "content": input.prompt}]
        result = self.pipe(messages, max_new_tokens=settings.max_new_tokens)
        raw = result[0]["generated_text"][-1]["content"]
        return LLMRunnerOutput(
            raw_answer=raw,
            question=input.question,
        )

class ResponseParser(Runnable[LLMRunnerOutput, ResponseParserOutput]):
    def run(self, input: LLMRunnerOutput) -> ResponseParserOutput:
        raw = input.raw_answer.strip()
        answer = raw.split("\n\n")[0].strip()
        return ResponseParserOutput(
            question=input.question,
            answer=answer
        )