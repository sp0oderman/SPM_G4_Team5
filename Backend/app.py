from __init__ import create_app
from config import DevelopmentConfig
from flask_cors import CORS

app = create_app(config_class=DevelopmentConfig)
CORS(app)

@app.route('/api/homepage')
def homepage():
    return {"message": "Homepage of flask app!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
