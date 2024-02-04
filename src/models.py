from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from normalizer import normalize
import logging

logger = logging.getLogger(__name__)

MODEL_PATH = "model_registry/banglat5_nmt_bn_en/model"
TOKENIZER_PATH = "model_registry/banglat5_nmt_bn_en/tokenizer"


class Bn2EnTranslator:
    def __init__(self, model_path=MODEL_PATH, tokenizer_path=TOKENIZER_PATH) -> None:
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, use_fast=False)

    def __call__(self, sentence_bn: str) -> str:
        return self.translate(sentence_bn)

    @staticmethod
    def post_process_translation(translation: str) -> str:
        logger.info("Removing special tokens ...")
        return translation.replace("<pad>", "").replace("</s>", "").strip()

    def translate(self, sentence_bn: str) -> str:
        """
        Translates a sentence from Bangla to English
        :param sentence_bn: Sentence in Bangla
        :return: Sentence in English
        """
        logger.info(f"Translating {sentence_bn}")
        input_ids = self.tokenizer(normalize(sentence_bn), return_tensors="pt").input_ids
        generated_tokens = self.model.generate(input_ids)
        decoded_tokens = self.tokenizer.batch_decode(generated_tokens)[0]
        decoded_tokens = self.post_process_translation(decoded_tokens)
        logger.info(f"Translated Text: {decoded_tokens}")
        return decoded_tokens

    def __str__(self):
        return "Bn2EnTranslator"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    bn2en = Bn2EnTranslator()
    input_sentence = "আন্দোলন দমনে পুলিশ ১৪৪ ধারা জারি করে ঢাকা শহরে মিছিল, সমাবেশ ইত্যাদি বেআইনি ও নিষিদ্ধ ঘোষণা করে।"
    print(bn2en(input_sentence))

