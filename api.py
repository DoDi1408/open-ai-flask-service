from logging.config import dictConfig
from flask import Flask, jsonify, request
from openai import OpenAI
import datetime

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

client = OpenAI()

app = Flask(__name__)

@app.route("/")
def test():
    app.logger.info('received a /')
    return "Hello, WORLD!!", 200

@app.route("/task", methods=['POST'])
def get_task_JSON():
    app.logger.info('received a /task')
    task_message = request.get_data(as_text=True)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        temperature=0.3,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "The current time is: " + str(datetime.datetime.now())  + " but minus 6 hours"},
            {"role": "system", "content": "Do not include hour on startDate or dueDate, format must be yyyy-MM-dd"},
            {"role": "system", "content": "You will receive text in spanish, make sure you dont subtitute letters with ñ or accents"},
            {"role": "system", "content": "You are a helpful assistant designed to output JSON. IT MUST have the following attributes. startDate, dueDate, description, title, stateTask (this one is always 0), and employee (this one is always null)"},
            {"role": "system", "content": "If you can't find dueDate in the incoming message, assign due date to be a day later."},
            {"role": "user", "content": task_message}
        ]
    )
    task_data = response.choices[0].message.content
    app.logger.info("returning:" + task_data)
    return task_data, 200, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    from waitress import serve
    PORT = 5134
    serve(app, host="0.0.0.0", port=PORT)