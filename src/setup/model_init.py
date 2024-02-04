from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from normalizer import normalize # pip install git+https://github.com/csebuetnlp/normalizer

print("Loading model and tokenizer...")
model = AutoModelForSeq2SeqLM.from_pretrained("csebuetnlp/banglat5_nmt_bn_en")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/banglat5_nmt_bn_en", use_fast=False)

input_sentence ="আন্দোলন দমনে পুলিশ ১৪৪ ধারা জারি করে ঢাকা শহরে মিছিল, সমাবেশ ইত্যাদি বেআইনি ও নিষিদ্ধ ঘোষণা করে।"

input_ids = tokenizer(normalize(input_sentence), return_tensors="pt").input_ids
generated_tokens = model.generate(input_ids)
decoded_tokens = tokenizer.batch_decode(generated_tokens)[0]

print("====")
print("Translated Text:")
print(decoded_tokens)
# print("Saving model to Current Directory...")
# model.save_pretrained("model_registry/banglat5_nmt_bn_en/model")
# print("Saving tokenizer to Current Directory...")
# tokenizer.save_pretrained("model_registry/banglat5_nmt_bn_en/tokenizer")