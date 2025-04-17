from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TRANSFORMERS_CACHE
import torch
import os

# Models configuration: model_id -> quantization mode
models_config = {
    # "deepseek-ai/deepseek-coder-v2-lite-base": "8bit",
    "Qwen/Qwen2.5-Coder-14B": "8bit"
}

for model_id, precision in models_config.items():
    print(f"\n🔽 Downloading {model_id} with precision: {precision}")

    # Configure quantization depending on precision
    if precision == "8bit":
        quant_config = BitsAndBytesConfig(
            load_in_8bit=True,
        )
        dtype = None  # dtype auto-determined by quantization
    elif precision == "16bit":
        quant_config = None  # No quantization for FP16
        dtype = torch.float16
    else:
        raise ValueError(f"Unsupported precision mode: {precision}")

    # Model Downloading
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=quant_config,
        torch_dtype=dtype,            # float16 explicitly for FP16, None otherwise
        device_map="auto",
        force_download=True,          # Force fresh download explicitly once
        trust_remote_code=True
    )

    # Tokenizer Downloading
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        trust_remote_code=True,
        force_download=True
    )

    # Clean up VRAM after downloading each model
    del model
    del tokenizer
    torch.cuda.empty_cache()

# Verify cached paths to ensuring success (recommended)
print("\n✅ Download Verification & Cache Locations:")
for model_id in models_config.keys():
    cache_path = os.path.join(TRANSFORMERS_CACHE, f"models--{model_id.replace('/', '--')}")
    print(f"✅ Model cached at: {cache_path}/snapshots/*")