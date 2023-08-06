from intentBox.parsers.template import IntentExtractor
from intentBox.utils import LOG, match_one, MatchStrategy, word_tokenize


class FuzzyExtractor(IntentExtractor):
    def __init__(self, strategy=MatchStrategy.SIMPLE_RATIO, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.strategy = strategy
        self.registered_intents = []
        self.registered_entities = {}

    def detach_intent(self, intent_name):
        if intent_name in self.registered_intents:
            LOG.debug("Detaching padaous intent: " + intent_name)
            self.registered_intents.remove(intent_name)

    def detach_skill(self, skill_id):
        LOG.debug("Detaching padaos skill: " + str(skill_id))
        remove_list = [i for i in self.registered_intents if skill_id in i]
        for i in remove_list:
            self.detach_intent(i)

    def register_entity(self, entity_name, samples=None):
        samples = samples or [entity_name]
        if entity_name not in self.registered_entities:
            self.registered_entities[entity_name] = []
        self.registered_entities[entity_name] += samples

    def register_intent(self, intent_name, samples=None):
        samples = samples or [intent_name]
        if intent_name not in self._intent_samples:
            self._intent_samples[intent_name] = samples
        else:
            self._intent_samples[intent_name] += samples
        self.registered_intents.append(intent_name)

    def register_entity_from_file(self, entity_name, file_name):
        with open(file_name) as f:
            samples = f.read().split("\n")
        self.register_entity(entity_name, samples)

    def register_intent_from_file(self, intent_name, file_name):
        with open(file_name) as f:
            samples = f.read().split("\n")
        self.register_intent(intent_name, samples)

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
            sent, score = match_one(sentence, samples)
            scores[intent] = {"best_match": sent,
                              "conf": score,
                              "intent_engine": "fuzzy",
                              "match_strategy": self.strategy,
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
            sent, score = match_one(sentence, samples)
            scores[intent] = {"best_match": sent,
                              "conf": score,
                              "intent_engine": "fuzzy",
                              "match_strategy": self.strategy,
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

    def manifest(self):
        # TODO vocab, skill ids, intent_data
        return {
            "intent_names": self.registered_intents
        }
