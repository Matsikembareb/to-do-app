import sys

from app.config.config import get_config_by_name
from app import create_app

#for python run.py "environment_name" e.g. python run.py testing
if __name__ == '__main__':
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=5000,
    )

