import argparse
import os
import sys

# Try importing the config helper; adjust sys.path if running from history or different cwd
try:
    from app.config.config import get_config_by_name
except Exception:
    # Add project root (two levels up from this history file) to path and retry
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if root not in sys.path:
        sys.path.insert(0, root)
    from app.config.config import get_config_by_name

from app import create_app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run the Flask backend')
    parser.add_argument(
        'environment',
        nargs='?',
        choices=['development', 'testing', 'production'],
        default='development',
        help='Environment configuration to use',
    )
    return parser.parse_args()


args = parse_args()
app = create_app(config_class=get_config_by_name(args.environment))

if __name__ == '__main__':
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=5000,
    )

