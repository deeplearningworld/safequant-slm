import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

class SafeQuant:
    def __init__(self, model_id: str, bits: int = 4):
        self.model_id = model_id
        self.bits = bits

    def quantize(self):
        # Settings with high precision configuration to maintain security alignment
        compute_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=(self.bits == 4),
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True, 
            bnb_4bit_compute_dtype=compute_dtype
        )

        tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, 
            trust_remote_code=True,
            use_fast=False
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )

        return model, tokenizer