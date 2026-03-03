import logging


logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything

# Para enviar para um arquivo de log
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')

# Para aparecer no console
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')

# Formatação de data
logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is when this event was logged.')

# Para AWS
logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=logging.INFO)
