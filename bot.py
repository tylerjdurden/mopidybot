from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
# from mopidy import core
from mopidy_json_client import MopidyClient
from mopidy_json_client.formatting import print_nice
from uuid import uuid4

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

mopidy = MopidyClient(
        ws_url='ws://localhost:6680/mopidy/ws',
        # event_handler=self.on_event,
        # error_handler=self.on_server_error,
        # connection_handler=self.on_connection,
        autoconnect=False
        # retry_max=10,
        # retry_secs=10
    )
mopidy.connect()



def show_search_results(search_results):
    print_nice('Search Results: ', search_results, format='search')

def start(bot, update):
    update.message.reply_text('Hello World!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def inline_hello(bot, update):
    query = update.inline_query.query
    response = 'Click me'

    mopidy.library.search(query={'any': [query]},
                          uris=['spotify:'],
                          on_result=show_search_results)

    # state = mopidy.playback.get_state(timeout=5)
    # print 'state:', state

    results = list()
    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title=response,
                                            input_message_content=InputTextMessageContent('You clicked me!')))
    update.inline_query.answer(results)

updater = Updater('236288754:AAFcbPuvblRM5vNq24HSBJUoALO_lTeY74c')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.dispatcher.add_handler(InlineQueryHandler(inline_hello))

updater.start_polling()
updater.idle()
