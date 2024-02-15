from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from normalizer import normalize  # pip install git+https://github.com/csebuetnlp/normalizer

print("Loading model...")
model = AutoModelForSeq2SeqLM.from_pretrained("csebuetnlp/banglat5_nmt_bn_en")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/banglat5_nmt_bn_en", use_fast=False)

input_sentence =""

input_ids = tokenizer(normalize(input_sentence), return_tensors="pt").input_ids
generated_tokens = model.generate(input_ids)
decoded_tokens = tokenizer.batch_decode(generated_tokens)[0]

print("====")
print("Translated Text:")
print(decoded_tokens)
print("Saving model to Current Directory...")
model.save_pretrained("model_registry/banglat5_nmt_bn_en/model")
print("Saving tokenizer to Current Directory...")
tokenizer.save_pretrained("model_registry/banglat5_nmt_bn_en/tokenizer")