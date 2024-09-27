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
        # logger.info("Removing special tokens ...")
        return translation.replace("<pad>", "").replace("</s>", "").strip()

    def translate(self, sentence_bn: str) -> str:
        """
        Translates a sentence from Bangla to English
        :param sentence_bn: Sentence in Bangla
        :return: Sentence in English
        """
        # logger.info(f"Translating {sentence_bn}")
        input_ids = self.tokenizer(normalize(sentence_bn), return_tensors="pt").input_ids
        generated_tokens = self.model.generate(input_ids)
        decoded_tokens = self.tokenizer.batch_decode(generated_tokens)[0]
        decoded_tokens = self.post_process_translation(decoded_tokens)
        logger.info(f"Translated Text: {decoded_tokens}")
        return decoded_tokens

    def split_n_translate(self, sentence_bn: str) -> str:
        sentence_list_bn = sentence_bn.strip().split("।")
        if len(sentence_list_bn[-1]) <= 1:
            sentence_list_bn = sentence_list_bn[:-1]
        sentence_list_bn = [item.strip() + "।" for item in sentence_list_bn]
        # print(sentence_list_bn)
        sentence_list_en = []
        for i, item in enumerate(sentence_list_bn, 1):
            logger.info(f"Translating {i}/{len(sentence_list_bn)}")
            sentence_list_en.append(self.translate(item))
        return " ".join(sentence_list_en)

    def __str__(self):
        return "Bn2EnTranslator"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    bn2en = Bn2EnTranslator()
    # print("Input Text:")
    # input_sentence = "আন্দোলন দমনে পুলিশ ১৪৪ ধারা জারি করে ঢাকা শহরে মিছিল, সমাবেশ ইত্যাদি বেআইনি ও নিষিদ্ধ ঘোষণা করে।"
    # print(input_sentence)
    # print("Translated Text")
    # print(bn2en(input_sentence))
    input_sentence = "বাংলাদেশের ভাষা আন্দোলন আমাদের ইতিহাসের একটি গৌরবময় অধ্যায় । ১৯৫২ সালের ২১শে ফেব্রুয়ারি বাংলাভাষাকে রাষ্ট্রভাষা হিসেবে স্বীকৃতি দেওয়ার দাবিতে ঢাকার ছাত্র-জনতা আন্দোলনে নামে । পাকিস্তান সরকার উর্দুকে একমাত্র রাষ্ট্রভাষা করার সিদ্ধান্ত নিলে এ আন্দোলন গড়ে ওঠে । পুলিশের গুলিতে সালাম, বরকত, রফিকসহ অনেক সাহসী তরুণ জীবন উৎসর্গ করেন । তাদের এই আত্মত্যাগের ফলেই বাংলা আমাদের মাতৃভাষা হিসেবে স্বীকৃতি পায় । ২১শে ফেব্রুয়ারি এখন আন্তর্জাতিক মাতৃভাষা দিবস হিসেবে পালিত হয়, যা আমাদের ভাষার জন্য ভালোবাসা ও আত্মত্যাগের প্রতীক ।"
    print(input_sentence)
    print("Translated Text")
    print(bn2en.split_n_translate(input_sentence))