import os

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, Pipeline
from langchain_community.llms import HuggingFacePipeline

def get_llm() -> Pipeline:
    model = "gemma-3-1b-it"

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    MODEL_DIR = os.path.join(BASE_DIR, "models", "google", model)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR,
        device_map=None,         # ❌ GPU 자동 할당 끄기
    )
    gen_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        temperature=0.7,
        top_p=0.95,
        do_sample=True,
        repetition_penalty=1.1
    )

    return gen_pipeline
