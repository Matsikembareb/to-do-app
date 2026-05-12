from app.config.config import get_config_by_name
from app import create_app

app = create_app(config_class=get_config_by_name())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

