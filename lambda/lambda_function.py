import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from data.facts_pt_BR import data, GET_FACT_MESSAGE, SKILL_NAME, HELP_MESSAGE, HELP_REPROMPT, STOP_MESSAGE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MyMorningRemediesHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("MyMorningRemediesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In MyMorningRemediesHandler")

        slotValue = Alexa.getSlotValue(handlerInput.requestEnvelope, 'remedio')
        random_fact_type = random.choice(data)
        ramdom_fact = random.choice(ramdom_fact_type)
        speech = GET_FACT_MESSAGE + ramdom_fact.nome - ramdom_fact.marca + "É um" + random_fact.indicacao

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, ramdom_fact))
        return handler_input.response_builder.response


class MyAfternoonRemediesHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("MyAfternoonRemediesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In MyAfternoonRemediesHandler")

        slotValue = Alexa.getSlotValue(handlerInput.requestEnvelope, 'remedio')
        random_fact_type = random.choice(data)
        ramdom_fact = random.choice(ramdom_fact_type)
        speech = GET_FACT_MESSAGE + ramdom_fact.nome - ramdom_fact.marca+ "É um" + random_fact.indicacao

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, ramdom_fact))
        return handler_input.response_builder.response


class MyNightRemediesHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("MyNightRemediesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In MyNightRemediesHandler")

        slotValue = Alexa.getSlotValue(handlerInput.requestEnvelope, 'remedio')
        random_fact_type = random.choice(data)
        ramdom_fact = random.choice(ramdom_fact_type)
        speech = GET_FACT_MESSAGE + ramdom_fact.nome - ramdom_fact.marca + "É um" + random_fact.indicacao

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, ramdom_fact))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):

        return (
            handler_input.response_builder
                .speak(HELP_MESSAGE)
                .ask(HELP_REPROMPT)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

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
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
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


sb = SkillBuilder()

sb.add_request_handler(MyMorningRemediesHandler())
sb.add_request_handler(MyAfternoonRemediesHandler())
sb.add_request_handler(MyNightRemediesHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()