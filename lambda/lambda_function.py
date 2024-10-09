# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Constantes e variáveis globais
GET_FACT_MESSAGE = "Aqui está o fato sobre o remédio: "
SKILL_NAME = "Medicação Inteligente"
EXCEPTION_MESSAGE = "Desculpe, ocorreu um erro. Por favor, tente novamente."
HELP_REPROMPT = "Em que mais posso te ajudar?"
STOP_MESSAGE = "Até mais!"
FALLBACK_MESSAGE = "Desculpe, não entendi isso. Por favor, tente novamente."
FALLBACK_REPROMPT = "Em que mais posso te ajudar?"
HELP_MESSAGE = "Você pode me pedir para falar sobre um remédio pela manhã, tarde ou noite."
data = [
    [
        {"nome": "Paracetamol", "marca": "Tylenol", "indicacao": "analgésico"},
        {"nome": "Ibuprofeno", "marca": "Advil", "indicacao": "anti-inflamatório"}
    ]
]

class LaunchRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In LaunchRequestHandler")

        try:
            speech = "Bem vindo senhor ou senhora, ao Medicação Inteligente."
            ask = "Como posso te ajudar?"

            handler_input.response_builder.speak(speech).ask(ask).set_card(
                SimpleCard(SKILL_NAME, speech))
            logger.info("LaunchRequestHandler response success")
        except Exception as e:
            logger.error(f"Erro no LaunchRequestHandler: {e}", exc_info=True)
            raise e

        return handler_input.response_builder.response


# Built-in Intent Handlers
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

        # Limpa o valor do slot após o uso, se necessário
        handler_input.request_envelope.request.intent.slots['remedio'].value = None

        # Mantém a sessão aberta com ask()
        handler_input.response_builder.speak(speech).ask("Em que mais posso te ajudar?").set_card(
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

        # Limpa o valor do slot após o uso, se necessário
        handler_input.request_envelope.request.intent.slots['remedio'].value = None

        # Mantém a sessão aberta com ask()
        handler_input.response_builder.speak(speech).ask("Em que mais posso te ajudar?").set_card(
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

        # Limpa o valor do slot após o uso, se necessário
        handler_input.request_envelope.request.intent.slots['remedio'].value = None

        # Mantém a sessão aberta com ask()
        handler_input.response_builder.speak(speech).ask("Em que mais posso te ajudar?").set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler para Help Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In HelpIntentHandler")

        speech = HELP_MESSAGE
        reprompt = HELP_REPROMPT
        handler_input.response_builder.speak(speech).ask(
            reprompt).set_card(SimpleCard(
                SKILL_NAME, speech))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler para Cancel e Stop Intents."""

    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In CancelOrStopIntentHandler")

        speech = STOP_MESSAGE
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler para Fallback Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")

        speech = FALLBACK_MESSAGE
        reprompt = FALLBACK_REPROMPT
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Carrega dados de localização específicos para o locale."""

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info(f"Locale is {locale}")

        with open("language_strings.json", 'r', encoding='utf-8') as language_prompts:
            language_data = json.load(language_prompts)

        if locale[:2] in language_data:
            data = language_data[locale[:2]]
            if locale in language_data:
                data.update(language_data[locale])
        else:
            data = language_data.get(locale, {})
            
        handler_input.attributes_manager.request_attributes["_"] = data


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler para o fim da sessão."""

    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In SessionEndedRequestHandler")
        logger.info(f"Session ended reason: {handler_input.request_envelope.request.reason}")
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Handler para capturar todas as exceções."""

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(HELP_REPROMPT)
        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log de requests da Alexa."""

    def process(self, handler_input):
        logger.debug(f"Alexa Request: {handler_input.request_envelope.request}")


class ResponseLogger(AbstractResponseInterceptor):
    """Log de responses da Alexa."""

    def process(self, handler_input, response):
        logger.debug(f"Alexa Response: {response}")


# Registrar os intent handlers
sb.add_request_handler(MyMorningRemediesHandler())
sb.add_request_handler(MyAfternoonRemediesHandler())
sb.add_request_handler(MyNightRemediesHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Registrar exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Registrar interceptores de request e response
sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler para o AWS Lambda
lambda_handler = sb.lambda_handler()
