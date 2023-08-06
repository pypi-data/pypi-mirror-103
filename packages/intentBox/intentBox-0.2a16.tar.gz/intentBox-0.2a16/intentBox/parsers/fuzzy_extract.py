from intentBox.parsers.template import IntentExtractor
from intentBox.utils import LOG, match_one, MatchStrategy, word_tokenize


class FuzzyExtractor(IntentExtractor):
    def __init__(self, fuzzy_strategy=MatchStrategy.SIMPLE_RATIO, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.fuzzy_strategy = fuzzy_strategy
        self.registered_intents = []
        self.registered_entities = {}

    # matching
    @staticmethod
    def get_utterance_remainder(utterance, best_match):
        words = [t for t in word_tokenize(utterance)
                 if t not in word_tokenize(best_match)]
        return " ".join(words)

    def match_fuzzy(self, sentence):
        scores = {}
        for intent in self.registered_intents:
            samples = self.intent_samples[intent]
            sent, score = match_one(sentence, samples,
                                    strategy=self.fuzzy_strategy)
            scores[intent] = {"best_match": sent,
                              "conf": score,
                              "intent_engine": "fuzzy",
                              "match_strategy": self.fuzzy_strategy,
                              "utterance": sentence,
                              "utterance_remainder":
                                  self.get_utterance_remainder(sentence, sent),
                              "intent_name": intent}
        return scores

    def fuzzy_best(self, sentence, min_conf=0.6):
        scores = {}
        best_s = 0
        best_intent = None
        for intent in self.registered_intents:
            samples = self.intent_samples[intent]
            sent, score = match_one(sentence, samples,
                                    strategy=self.fuzzy_strategy)
            scores[intent] = {"best_match": sent,
                              "conf": score,
                              "intent_engine": "fuzzy",
                              "match_strategy": self.fuzzy_strategy,
                              "utterance": sentence,
                              "utterance_remainder":
                                  self.get_utterance_remainder(sentence, sent),
                              "intent_type": intent}
            if score > best_s:
                best_s = score
                best_intent = intent
        return scores[best_intent] if best_s > min_conf else \
            {"best_match": None,
             "conf": 0,
             "intent_type": None,
             "intent_engine": "fuzzy",
             "utterance": sentence,
             "utterance_remainder": sentence,
             "match_strategy": self.strategy}

    def calc_intent(self, utterance, min_conf=0.6):
        return self.fuzzy_best(utterance)

    def intent_scores(self, utterance):
        utterance = utterance.strip() # spaces should not mess with exact matches
        intents = []
        bucket = self.calc_intents(utterance)
        for utt in bucket:
            intent = bucket[utt]
            if not intent:
                continue
            intents.append(intent)
        return intents

    def calc_intents(self, utterance, min_conf=0.6):
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            intent = self.calc_intent(ut)
            bucket[ut] = intent
        return bucket

    def calc_intents_list(self, utterance):
        utterance = utterance.strip() # spaces should not mess with exact matches
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            bucket[ut] = self.filter_intents(ut)
        return bucket