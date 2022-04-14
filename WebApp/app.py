from flask import Flask, render_template
import logging

app = Flask(__name__)

''' HOME PAGE
'''

@app.route('/')
def home():
    return render_template('start.html')

if __name__ == '__main__':
    app.run()
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
