from flask import Flask, render_template, jsonify
# from flask_cors import CORS, cross_origin
import subprocess


# App Creation
app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/static/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search/<query>', methods=['GET'])
# @cross_origin(allow_headers=['Content-Type', 'ngrok-skip-browser-warning'])
def search(query: str):

    # QUERY
    # escape character for each search term
    
    # Popen() is async, run is synchronous
    rclip = subprocess.run(["rclip", "-fn", "-t", "10", query], cwd="static/img", encoding='utf-8', stdout=subprocess.PIPE)
    results = rclip.stdout.split('\n')


    # rclip returns the absolute path
    # get relative path to static
    d_path = ""
    for directory in results[0].split('/'):
        if directory == "static":
            break

        d_path += "/" + directory

    for i in range(len(results)):
        results[i] = results[i][d_path:]

    response = jsonify({"query":query, "result":results[:len(results) - 1]})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    

    # return response
    return render_template('results.html', imgs=results)

# Start the Server

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005, debug=True, use_reloader=False)