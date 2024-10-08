import random
import logging
import json
import prompts

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LaunchRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In LaunchRequestHandler")

        speech = "Bem vindo senhor ou senhora, ao Medicação Inteligente."
        ask = "Como posso te ajudar?"

        handler_input.response_builder.speak(speech).ask(ask).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response


class MyMorningRemediesHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return is_intent_name("MyMorningRemediesIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In MyMorningRemediesHandler")

        slot_value = get_slot_value(handler_input, 'remedio')
        random_fact_type = random.choice(data)
        random_fact = random.choice(random_fact_type)
        speech = (GET_FACT_MESSAGE + random_fact["nome"] + " - " + random_fact["marca"] + 
                  " é um " + random_fact["indicacao"])

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response


class MyAfternoonRemediesHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return is_intent_name("MyAfternoonRemediesIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In MyAfternoonRemediesHandler")

        slot_value = get_slot_value(handler_input, 'remedio')
        random_fact_type = random.choice(data)
        random_fact = random.choice(random_fact_type)
        speech = (GET_FACT_MESSAGE + random_fact["nome"] + " - " + random_fact["marca"] + 
                  " é um " + random_fact["indicacao"])

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response


class MyNightRemediesHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return is_intent_name("MyNightRemediesIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In MyNightRemediesHandler")

        slot_value = get_slot_value(handler_input, 'remedio')
        random_fact_type = random.choice(data)
        random_fact = random.choice(random_fact_type)
        speech = (GET_FACT_MESSAGE + random_fact["nome"] + " - " + random_fact["marca"] + 
                  " é um " + random_fact["indicacao"])

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        return (
            handler_input.response_builder
                .speak(HELP_MESSAGE)
                .ask(HELP_REPROMPT)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = STOP_MESSAGE

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent name."""

    def can_handle(self, handler_input):
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = get_intent_name(handler_input)
        speak_output = "Você acabou de acionar " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, tive problemas para fazer o que você pediu. Por favor, tente novamente."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))

        # localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        # set default translation data to broader translation
        if locale[:2] in language_data:
            data = language_data[locale[:2]]
            # if a more specialized translation exists, then select it instead
            # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
            # then pick that instead
            if locale in language_data:
                data.update(language_data[locale])
        else:
            data = language_data[locale]
        handler_input.attributes_manager.request_attributes["_"] = data
        

class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))



sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MyMorningRemediesHandler())
sb.add_request_handler(MyAfternoonRemediesHandler())
sb.add_request_handler(MyNightRemediesHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()
