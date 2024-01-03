import logging
from app.app import app
from os import environ as env

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
log.info('%s logger started.', __name__)


def main():
    port = int(env.get('PORT', 5080))
    app.run(host='0.0.0.0', port=port, debug=True, load_dotenv=True)


if __name__ == '__main__':
    main()
