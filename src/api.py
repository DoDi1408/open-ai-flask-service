from flask import Flask, jsonify, request
from openai import OpenAI

client = OpenAI()

app = Flask(__name__)

@app.route("/task", methods=['POST'])
def get_task_JSON():
    task_message = request.get_data(as_text=True)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        temperature=0.3,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON. IT MUST have the following attributes. startDate, dueDate, description, title, stateTask (this one is always 0), and employee (this one is always null)"},
            {"role": "user", "content": task_message}
        ]
    )
    task_data = response.choices[0].message.content
    print("returning: " + response.choices[0].message.content)
    return jsonify(task_data), 200


if __name__ == "__main__":
    from waitress import serve
    PORT = 9000
    print("Running server on port: " + str(PORT))
    serve(app, host="0.0.0.0", port=PORT)