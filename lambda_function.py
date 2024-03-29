# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from ask_sdk_model.interfaces.videoapp import (LaunchDirective,VideoItem,Metadata)
from ask_sdk_model import ui

from ask_sdk_model.ui import SimpleCard

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


import time
from cards import *

# gameSession will be an object of the CardGame class
gameSession = CardGame()


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
   #     speak_output = "Okay! I'm ready to play when you are!"

        welcome_info = "Welcome to Card Find Game! The system will select a random card among the 12 candidate cards. Your task is to find out the number of this secret card in 60 seconds. To narrow down your choices, you could ask Alexa about the rotation, symbol and color of the symbol in different positions, like center left. You have only 3 chances to guess. Now, when you get ready, say start to begin this game."
        show_info = "Task: find out the number of this secret card among 12 candidates in 60 seconds (3 chances in total). To narrow down your choices, you could ask Alexa about the rotation, symbol and color of the symbol in different positions, like row 1 column 1. When you get ready, say start to begin this game."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .set_card(SimpleCard("Card Match Game", show_info))
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask, 'the color of center left symbol'"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .set_card(SimpleCard("Card Match Game", speak_output))
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


# Begin the Alexa Card Matching Game
class StartGameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StartGameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Okay. I've put 60 seconds on the clock. Let's begin!"
        gameSession.start()

        handler_input.response_builder.set_card(
            ui.StandardCard(
                title="Card Match Game",
                text="Welcome to Card Match Game!",
                image=ui.Image(
                    small_image_url="https://d2o906d8ln7ui1.cloudfront.net/images/BT7_Background.png",
                    large_image_url= "https://d2o906d8ln7ui1.cloudfront.net/images/BT2_Background.png"
                )
            )
        ) 
        ##### comment codes below for online simulation
        handler_input.response_builder.add_directive(
            LaunchDirective(
                VideoItem(
                    source = "https://cardmatchgamevideo.s3.amazonaws.com/clock1.mp4", 
                    metadata = Metadata(title = "Card Match Game", subtitle = "Clock")
                )
            )
        )
        ### end of your comment
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("You can ask the color of center left symbol")
                .set_card(SimpleCard("Card Match Game", "You can ask, 'the color of center left symbol'"))
                .response
        )

# Handle a Question the Human Asks
class QueryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("QueryIntent")(handler_input)

    def handle(self, handler_input):
        if( not gameSession.isInProgress ):
            return (
                handler_input.response_builder
                    .speak("We aren't playing right now!")
                    .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )
        if( time.time() - gameSession.startTime > 60 ):
            gameSession.end()
            return (
                handler_input.response_builder
                    .speak("I'm sorry. The game is over!")
                    .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )
        try:
            position = handler_input.request_envelope.request.intent.slots['Position'].value
            symbol = gameSession.query( position )
        except:
            try:
                symbol = gameSession.lastSymbol
            except:
                symbol = False
                
        if( symbol ):
            data = handler_input.request_envelope.request.intent.slots['Data'].value
            if( str(data) == "None" ):
                speak_output = "It's " + str(symbol.character)
            else:
                speak_output = "It's "
                if( data == "color" ):
                    speak_output += str(symbol.color)
                elif( data == "rotation" ):
                    speak_output += str(symbol.rotation)
                elif( data == "character" ):
                    speak_output += str(symbol.character)
                else:
                    speak_output = "I got confused sorry. What? " + str(data)
        else:
            speak_output = "I don't know which symbol you mean!"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("You can ask the color of center left symbol")
                .response
        )

# Handle an Answer the Human Gives
class AnswerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AnswerIntent")(handler_input)

    def handle(self, handler_input):
        if( not gameSession.isInProgress ):
            return (
                handler_input.response_builder
                    .speak("We aren't playing right now!")
                    .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )
        speak_output = ""
        gameSession.guesses += 1
        if( time.time() - gameSession.startTime > 60 ):
            gameSession.end()
            speak_output = "We just ran out of time, but "
        elif( gameSession.guesses >= 3 ):
            gameSession.end()
            speak_output = "You just used your last guess, and "
            
        isAnswerValid = ( int(handler_input.request_envelope.request.intent.slots['Number'].value) == gameSession.card.id )
        # add emotion words(begin)
        speechConsCorrect = ('Booya', 'All righty', 'Bam', 'Bazinga', 'Bingo', 'Boom', 'Bravo', 'Cha Ching', 'Cheers', 'Dynomite', 'Hip hip hooray', 'Hurrah', 'Hurray', 'Huzzah', 'Oh dear.  Just kidding.  Hurray', 'Kaboom', 'Kaching', 'Oh snap', 'Phew','Righto', 'Way to go', 'Well done', 'Whee', 'Woo hoo', 'Yay', 'Wowza', 'Yowsa')
        speechConsWrong = ('Argh', 'Aw man', 'Blarg', 'Blast', 'Boo', 'Bummer', 'Darn', "D'oh", 'Dun dun dun', 'Eek', 'Honk', 'Le sigh', 'Mamma mia', 'Oh boy', 'Oh dear', 'Oof', 'Ouch', 'Ruh roh', 'Shucks', 'Uh oh', 'Wah wah', 'Whoops a daisy', 'Yikes')
        if( isAnswerValid ):
            speak_output += "<say-as interpret-as='interjection'>"+ random.choice( tuple(speechConsCorrect) )+"</say-as><break strength='strong'/>"
            speak_output += " That's "+"<emphasis level='strong'>"+"correct"+ "</emphasis><break strength='strong'/>"
        else:
            speak_output += "<say-as interpret-as='interjection'>"+ random.choice( tuple(speechConsWrong) ) +"</say-as><break strength='strong'/>"
            speak_output +=  "<say-as interpret-as='interjection'>"+" not right!"+"</say-as><break strength='strong'/>"
        ##### (end) 
        # speak_output += "That's " + ("right! " if isAnswerValid else "not right! ")

        if( isAnswerValid ):
            speak_output += "<say-as interpret-as='interjection'>"+"We win! "+"</say-as><break strength='strong'/>"
            gameSession.end()
        if( not gameSession.isInProgress ):
            speak_output += "Just say start the game if you'd like to try again."

        return (
            handler_input.response_builder
                .speak("<voice name='Matthew'>"+speak_output+"</voice>" if isAnswerValid else speak_output)
                .ask("You can ask the color of center left symbol")
                .response
        )

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(StartGameIntentHandler())
sb.add_request_handler(QueryIntentHandler())
sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
