from intentBox.parsers.fuzzy_extract import FuzzyExtractor
from intentBox.parsers.template import IntentExtractor
from intentBox.utils import LOG, resolve_resource_file


class IntentBox(IntentExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engines_config = self.config.get("engines") or {}
        # TODO plugin system
        self.engines = {"fuzzy": None, "adapt": None, "padacioso": None,
                        "padaos": None, "padatious": None}
        self._load_engines()

    def _load_engines(self):
        fuzzy_config = self.engines_config.get("fuzzy") or {}
        if fuzzy_config.get("enabled", True):
            self.engines["fuzzy"] = FuzzyExtractor(config=fuzzy_config)

        adapt_config = self.engines_config.get("adapt") or {}
        if adapt_config.get("enabled", True):
            from intentBox.parsers.adapt_extract import AdaptExtractor
            self.engines["adapt"] = AdaptExtractor(config=adapt_config)

        padaos_config = self.engines_config.get("padaos") or {}
        if padaos_config.get("enabled", False):
            from intentBox.parsers.padaos_extract import PadaosExtractor
            self.engines["padaos"] = PadaosExtractor(config=padaos_config)

        padacioso_config = self.engines_config.get("padacioso") or {}
        if padacioso_config.get("enabled", True):
            from intentBox.parsers.padacioso_extract import PadaciosoExtractor
            self.engines["padacioso"] = PadaciosoExtractor(
                config=padacioso_config)

        padatious_config = self.engines_config.get("padatious") or {}
        if padatious_config.get("enabled", False):
            from intentBox.padatious_extract import PadatiousExtractor
            self.engines["padatious"] = PadatiousExtractor(
                config=padatious_config)

    # intentBox interface
    def register_intent(self, name, samples=None):
        super().register_intent(name, samples)
        for parser, engine in self.engines.items():
            if not engine:
                continue
            self.engines[parser].register_intent(name, samples)

    def register_intent_from_file(self, intent_name, file_name):
        super().register_intent_from_file(intent_name, file_name)
        if file_name.endswith(".voc") or file_name.endswith(".entity"):
            self.register_adapt_intent_from_file(intent_name, file_name)
        elif file_name.endswith(".rx"):
            self.register_adapt_regex_from_file(file_name)
        else:
            for parser, engine in self.engines.items():
                if not engine:
                    continue
                self.engines[parser].register_intent_from_file(intent_name, file_name)

    def register_entity(self, name, samples=None):
        super().register_entity(name, samples)
        for parser, engine in self.engines.items():
            if not engine:
                continue
            self.engines[parser].register_entity(name, samples)

    def register_entity_from_file(self, entity_name, file_name):
        super().register_entity_from_file(entity_name, file_name)
        if file_name.endswith(".rx"):
            self.register_adapt_regex_from_file(file_name)
        else:
            for k, v in self.engines.items():
                if v:
                    self.engines[k].register_entity_from_file(entity_name,
                                                              file_name)

    def detach_intent(self, intent_name):
        super().detach_intent(intent_name)
        for k, v in self.engines.items():
            if v:
                self.engines[k].detach_intent(intent_name)

    def detach_skill(self, skill_id):
        super().detach_skill(skill_id)
        for k, v in self.engines.items():
            if v:
                self.engines[k].detach_skill(skill_id)

    def calc_intent(self, utterance):
        # lots of magic numbers below, these try to weight the relative
        # accuracy of the different parsers
        utterance = utterance.strip()  # spaces should not mess with exact matches
        a = p = p2 = p3 = f = None

        # best intent
        if self.engines["adapt"]:
            a = self.engines["adapt"].calc_intent(utterance)
            _a = a.copy()
            if "__tags__" in _a:
                _a.pop("__tags__")
            LOG.debug("Adapt match: {intent}".format(intent=_a))

        if self.engines["padatious"]:
            p = self.engines["padatious"].calc_intent(utterance)
            LOG.debug("Padatious match: {intent}".format(intent=p))

        if self.engines["padaos"]:
            p2 = self.engines["padaos"].calc_intent(utterance)
            LOG.debug("Padaos match: {intent}".format(intent=p2))

        if self.engines["padacioso"]:
            p3 = self.engines["padacioso"].calc_intent(utterance)
            LOG.debug("Padacioso match: {intent}".format(intent=p2))

        if self.engines["fuzzy"]:
            f = self.engines["fuzzy"].calc_intent(utterance)
            LOG.debug("Fuzzy match: {intent}".format(intent=f))

        if p3 and p3["conf"] >= 0.9:
            return p
        if p2 and p2["conf"] >= 0.8:
            return p2
        if a and a["conf"] >= 0.7:
            return a
        if p and p["conf"] >= 0.8:
            return p
        if p3 and p3["conf"] >= 0.7:
            return p
        if a and a["conf"] > 0.4 or (a and p and 0 < p["conf"] < a["conf"]):
            return a
        if p and p["conf"] > 0.6:  # lots of false positives on 0.5 range
            return p
        if f and f["conf"] > 0.8:
            return f
        if a and a["conf"]:  # adapt regex/context is often low confidence
            return a
        if p2 and p2["conf"] > 0.3:
            return p2
        if p and p["conf"] > 0.3:
            return p
        return None

    def calc_intents(self, utterance, min_conf=0.5):
        utterance = utterance.strip()  # spaces should not mess with exact matches
        # segment + best intent per chunk
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            bucket[ut] = self.calc_intent(ut)
        return bucket

    def calc_intents_list(self, utterance):
        utterance = utterance.strip()
        intents = []
        for parser in self.engines:
            if not self.engines[parser]:
                continue
            intents += self.engines[parser].calc_intents_list(utterance)
        return intents

    def intent_scores(self, utterance):
        utterance = utterance.strip()
        intents = []
        for parser in self.engines:
            if not self.engines[parser]:
                continue
            intents += self.engines[parser].intent_scores(utterance)
        return intents

    # engine specific interfaces
    ## Adapt
    def register_adapt_intent(self, intent_name, samples=None,
                              optional_samples=None):
        LOG.info("Registering adapt intent: " + intent_name)
        optional_samples = optional_samples or []
        self.engines["adapt"].register_intent(intent_name, samples,
                                              optional_samples)

    def register_adapt_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt intent file: " + file_name)
        self.register_adapt_entity_from_file(intent_name, file_name)
        self.register_adapt_intent(intent_name)

    def register_adapt_entity(self, entity_name, samples=None, alias_of=None):
        LOG.info("Registering adapt entity: " + entity_name)
        self.engines["adapt"].register_entity(entity_name, samples,
                                              alias_of=alias_of)

    def register_adapt_regex_entity(self, regex_str):
        LOG.info("Registering adapt regex: " + regex_str)
        self.engines["adapt"].register_regex_entity(regex_str)

    def register_adapt_regex_from_file(self, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt regex file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        for s in samples:
            self.register_adapt_regex_entity(s)

    def register_adapt_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt entity file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        self.register_adapt_entity(entity_name, samples)

    ## Padatious
    def register_padatious_intent(self, intent_name, samples=None):
        LOG.info("Registering padatious intent: " + intent_name)
        self.engines["padatious"].register_intent(intent_name, samples)

    def register_padatious_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padatious intent file: " + file_name)
        self.engines["padatious"].register_intent_from_file(intent_name,
                                                            file_name)

    def register_padatious_entity(self, entity_name, samples=None):
        LOG.info("Registering padatious entity: " + entity_name)
        self.engines["padatious"].register_entity(entity_name, samples)

    def register_padatious_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padatious entity file: " + file_name)
        try:
            self.engines["padatious"].register_entity_from_file(entity_name,
                                                                file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)

    ## Padaos
    def register_padaos_intent(self, intent_name, samples=None):
        LOG.info("Registering padaos intent: " + intent_name)
        self.engines["padaos"].register_intent(intent_name, samples)

    def register_padaos_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padaos intent file: " + file_name)
        self.engines["padaos"].register_intent_from_file(intent_name,
                                                         file_name)

    def register_padaos_entity(self, entity_name, samples=None):
        LOG.info("Registering padaos entity: " + entity_name)
        self.engines["padaos"].register_entity(entity_name, samples)

    def register_padaos_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padaos entity file: " + file_name)
        try:
            self.engines["padaos"].register_entity_from_file(entity_name,
                                                             file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)

    ## Padacioso
    def register_padacioso_intent(self, intent_name, samples=None):
        LOG.info("Registering padacioso intent: " + intent_name)
        self.engines["padacioso"].register_intent(intent_name, samples)

    def register_padacioso_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padacioso intent file: " + file_name)
        self.engines["padacioso"].register_intent_from_file(intent_name,
                                                            file_name)

    def register_padacioso_entity(self, entity_name, samples=None):
        LOG.info("Registering padacioso entity: " + entity_name)
        self.engines["padacioso"].register_entity(entity_name, samples)

    def register_padacioso_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padacioso entity file: " + file_name)
        try:
            self.engines["padacioso"].register_entity_from_file(entity_name,
                                                                file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)

    ## Fuzzy
    def register_fuzzy_intent(self, intent_name, samples=None):
        LOG.info("Registering fuzzy intent: " + intent_name)
        self.engines["fuzzy"].register_intent(intent_name, samples)

    def register_fuzzy_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering fuzzy intent file: " + file_name)
        self.engines["fuzzy"].register_intent_from_file(intent_name, file_name)

    def register_fuzzy_entity(self, entity_name, samples=None):
        LOG.info("Registering fuzzy entity: " + entity_name)
        self.engines["fuzzy"].register_entity(entity_name, samples)

    def register_fuzzy_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering fuzzy entity file: " + file_name)
        try:
            self.engines["fuzzy"].register_entity_from_file(entity_name,
                                                            file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)
