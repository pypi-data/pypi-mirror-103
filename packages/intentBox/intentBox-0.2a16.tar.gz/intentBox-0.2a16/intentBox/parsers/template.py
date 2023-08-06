import abc
import re
from adapt.context import ContextManagerFrame
from intentBox.utils import flatten, normalize, LOG
from intentBox.segmenter import Segmenter
from intentBox.coreference import replace_coreferences
import time
import enum


class IntentStrategy(str, enum.Enum):
    SINGLE_INTENT = "single"
    REMAINDER = "remainder"
    SEGMENT = "segment"
    SEGMENT_REMAINDER = "segment+remainder"
    SEGMENT_MULTI = "segment+multi"


class ContextManager:
    """
    ContextManager
    Use to track context throughout the course of a conversational session.
    How to manage a session's lifecycle is not captured here.
    """

    def __init__(self, timeout):
        self.frame_stack = []
        self.timeout = timeout * 60  # minutes to seconds

    def clear_context(self):
        self.frame_stack = []

    def remove_context(self, context_id):
        for context, ts in list(self.frame_stack):
            ents = context.entities[0].get('data', [])
            for e in ents:
                if context_id == e:
                    self.frame_stack.remove((context, ts))

    def inject_context(self, entity, metadata=None):
        """
        Args:
            entity(object): Format example...
                               {'data': 'Entity tag as <str>',
                                'key': 'entity proper name as <str>',
                                'confidence': <float>'
                               }
            metadata(object): dict, arbitrary metadata about entity injected
        """
        metadata = metadata or {}
        try:
            if len(self.frame_stack) > 0:
                top_frame = self.frame_stack[0]
            else:
                top_frame = None
            if top_frame and top_frame[0].metadata_matches(metadata):
                top_frame[0].merge_context(entity, metadata)
            else:
                frame = ContextManagerFrame(entities=[entity],
                                            metadata=metadata.copy())
                self.frame_stack.insert(0, (frame, time.time()))
        except (IndexError, KeyError):
            pass
        except Exception as e:
            LOG.exception(e)

    def get_context(self, max_frames=5, missing_entities=None):
        """ Constructs a list of entities from the context.

        Args:
            max_frames(int): maximum number of frames to look back
            missing_entities(list of str): a list or set of tag names,
            as strings

        Returns:
            list: a list of entities

        """
        try:
            missing_entities = missing_entities or []

            relevant_frames = [frame[0] for frame in self.frame_stack if
                               time.time() - frame[1] < self.timeout]

            if not max_frames or max_frames > len(relevant_frames):
                max_frames = len(relevant_frames)

            missing_entities = list(missing_entities)

            context = []
            last = ''
            depth = 0
            for i in range(max_frames):
                frame_entities = [entity.copy() for entity in
                                  relevant_frames[i].entities]
                for entity in frame_entities:
                    entity['confidence'] = entity.get('confidence', 1.0) \
                                           / (2.0 + depth)
                context += frame_entities

                # Update depth
                if entity['origin'] != last or entity['origin'] == '':
                    depth += 1
                last = entity['origin']
            result = []
            if len(missing_entities) > 0:

                for entity in context:
                    if entity.get('data') in missing_entities:
                        result.append(entity)
                        # NOTE: this implies that we will only ever get one
                        # of an entity kind from context, unless specified
                        # multiple times in missing_entities. Cannot get
                        # an arbitrary number of an entity kind.
                        missing_entities.remove(entity.get('data'))
            else:
                result = context

            # Only use the latest instance of each keyword
            stripped = []
            processed = []
            for f in result:
                keyword = f['data'][0][1]
                if keyword not in processed:
                    stripped.append(f)
                    processed.append(keyword)
            result = stripped
        except Exception as e:
            LOG.exception(e)
            return []
        #LOG.debug("Adapt Context: {}".format(result))
        return result


class IntentExtractor:
    def __init__(self, lang="en-us", use_markers=True, solve_corefs=True,
                 config=None, strategy=IntentStrategy.SEGMENT_REMAINDER):
        self.config = config or {}
        self.solve_corefs = solve_corefs
        self.segmenter = Segmenter(lang=lang, use_markers=use_markers,
                                   solve_corefs=solve_corefs)
        self.lang = lang
        self.strategy = strategy
        self._intent_samples = {}
        self.registered_intents = []
        self.registered_entities = {}
        # Context related initializations
        # the context manager is from adapt, however it can be used by any
        # intent engine, in a future PR this will be generalized using
        # ContextManager.get_context and ContextManager.inject_context in
        # the self.calc methods
        self.context_config = self.config.get('context', {})
        self.context_keywords = self.context_config.get('keywords', [])
        self.context_max_frames = self.context_config.get('max_frames', 3)
        self.context_timeout = self.context_config.get('timeout', 2)
        self.context_greedy = self.context_config.get('greedy', False)
        self.context_manager = ContextManager(self.context_timeout)

    @property
    def intent_samples(self):
        return self._intent_samples

    def get_normalizations(self, utterance, lang=None):
        lang = lang or self.lang
        norm = normalize(utterance,
                         remove_articles=True,
                         lang=lang)
        norm2 = normalize(utterance,
                          remove_articles=False,
                          lang=lang)
        norm3 = re.sub(r'[^\w]', ' ', utterance)
        norm4 = ''.join([i if 64 < ord(i) < 128 or ord(i) == 32
                         else ''
                         for i in utterance])
        return [u for u in [norm, norm2, norm3, norm4] if u != utterance]

    def detach_skill(self, skill_id):
        LOG.debug("Detaching padaos skill: " + str(skill_id))
        remove_list = [i for i in self.registered_intents if skill_id in i]
        for i in remove_list:
            self.detach_intent(i)

    def detach_intent(self, intent_name):
        if intent_name in self.registered_intents:
            LOG.debug("Detaching padaous intent: " + intent_name)
            self.registered_intents.remove(intent_name)

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
            entities = f.read().split("\n")
            self.register_entity(entity_name, entities)

    def register_intent_from_file(self, intent_name, file_name):
        with open(file_name) as f:
            intents = f.read().split("\n")
            self.register_entity(intent_name, intents)

    @abc.abstractmethod
    def calc_intent(self, utterance):
        """ return intent result for utterance

       UTTERANCE: tell me a joke and say hello

        {'name': 'joke', 'sent': 'tell me a joke and say hello', 'matches': {}, 'conf': 0.5634853146417653}

        """
        pass

    @abc.abstractmethod
    def calc_intents(self, utterance, min_conf=0.5):
        """ segment utterance and return best intent for individual segments

        if confidence is below min_conf intent is None

       UTTERANCE: tell me a joke and say hello

        {'say hello': {'conf': 0.5750943775957492, 'matches': {}, 'name': 'hello'},
         'tell me a joke': {'conf': 1.0, 'matches': {}, 'name': 'joke'}}

        """
        pass

    @abc.abstractmethod
    def calc_intents_list(self, utterance):
        """ segment utterance and return all intents for individual segments

       UTTERANCE: tell me a joke and say hello

        {'say hello': [{'conf': 0.1405158302488502, 'matches': {}, 'name': 'weather'},
                       {'conf': 0.5750943775957492, 'matches': {}, 'name': 'hello'},
                       {'conf': 0.0, 'matches': {}, 'name': 'name'},
                       {'conf': 0.36216947883621736, 'matches': {}, 'name': 'joke'}],
         'tell me a joke': [{'conf': 0.0, 'matches': {}, 'name': 'weather'},
                            {'conf': 0.0, 'matches': {}, 'name': 'hello'},
                            {'conf': 0.0, 'matches': {}, 'name': 'name'},
                            {'conf': 1.0, 'matches': {}, 'name': 'joke'}]}

        """
        pass

    def intent_remainder(self, utterance, _prev=""):
        """
        calc intent, remove matches from utterance, check for intent in leftover, repeat

        :param utterance:
        :param _prev:
        :return:
        """
        intent_bucket = []
        original_utt = utterance
        while _prev != utterance:
            _prev = utterance

            intent = self.calc_intent(utterance)
            if intent:
                intent["utterance"] = original_utt
                intent["consumed_utterance"] = utterance
                intent_bucket += [intent]
                if intent.get("__tags__"):
                    # adapt
                    tags = []
                    for token in intent["__tags__"]:
                        # Substitute only whole words matching the token
                        tags.append(token.get("key", ""))
                        utterance = re.sub(
                            r'\b' + token.get("key", "") + r"\b", "",
                            utterance)
                    intent["consumed_utterance"] = " ".join(tags)
                elif len(intent.get("entities", {})):
                    # padatious
                    for token in intent["entities"]:
                        # TODO figure out a decent remainder logic for padatious
                        pass

        return intent_bucket

    def intents_remainder(self, utterance, min_conf=0.5):
        """
        segment utterance and for each chunk recursively check for intents in utterance remainer

        :param utterance:
        :param min_conf:
        :return:
        """
        utterances = self.segmenter.segment(utterance)
        bucket = []
        for utterance in utterances:
            bucket += self.intent_remainder(utterance)
        return [b for b in bucket if b]

    @abc.abstractmethod
    def intent_scores(self, utterance):
        pass

    def filter_intents(self, utterance, min_conf=0.5):
        """

        returns all intents above a minimum confidence, meant for disambiguation

        can somewhat be used for multi intent parsing

        UTTERANCE: close the door turn off the lights
        [{'conf': 0.5311372507542608, 'entities': {}, 'name': 'lights_off'},
         {'conf': 0.505765852348431, 'entities': {}, 'name': 'door_close'}]

        :param utterance:
        :param min_conf:
        :return:
        """
        return [i for i in self.intent_scores(utterance) if
                i["conf"] >= min_conf]

    def calc(self, utterance):
        """
        segment utterance and for each chunk recursively check for intents in utterance remainer

        :param utterance:
        :return:
        """
        if self.solve_corefs:
            utterance = replace_coreferences(utterance)

        if self.strategy in [IntentStrategy.SEGMENT_REMAINDER,
                             IntentStrategy.SEGMENT]:
            utterances = self.segmenter.segment(utterance)
            # up to N intents
        else:
            utterances = [utterance]
        prev_ut = ""
        bucket = []
        for utterance in utterances:
            # calc intent + calc intent again in leftover text
            if self.strategy in [IntentStrategy.REMAINDER,
                                 IntentStrategy.SEGMENT_REMAINDER]:
                intents = self.intent_remainder(utterance)  # up to 2 intents

                # use a bigger chunk of the utterance
                if not intents and prev_ut:
                    # TODO ensure original utterance form
                    # TODO lang support
                    intents = self.intent_remainder(prev_ut + " " + utterance)
                    if intents:
                        # replace previous intent match with
                        # larger utterance segment match
                        bucket[-1] = intents
                        prev_ut = prev_ut + " " + utterance
                else:
                    prev_ut = utterance
                    bucket.append(intents)

            # calc single intent over full utterance
            # if this strategy is selected the segmenter step is skipped
            # and there is only 1 utterance
            elif self.strategy == IntentStrategy.SINGLE_INTENT:
                bucket.append([self.calc_intent(utterance)])

            # calc multiple intents over full utterance
            # "segment+multi" is misleading in the sense that
            # individual intent engines should do the segmentation
            # if this strategy is selected the segmenter step is skipped
            # and there is only 1 utterance
            else:
                intents = [intent for ut, intent in
                           self.calc_intents(utterance).items()]
                bucket.append(intents)

        return [i for i in flatten(bucket) if i]

    def manifest(self):
        return {
            "intent_names": self.registered_intents,
            "entities": self.registered_entities
        }


