import sys

from app.config.config import get_config_by_name
from app import create_app

config_name = sys.argv[1] if len(sys.argv) > 1 else "development"
app = create_app(config_class=get_config_by_name(config_name))

if __name__ == '__main__':
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=5000,
    )

