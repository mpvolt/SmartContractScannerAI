from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "deepseek-ai/deepseek-coder-6.7b-base"

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained(model_id)