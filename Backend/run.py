from src import create_app
from config import DevelopmentConfig

app = create_app(config_class=DevelopmentConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
