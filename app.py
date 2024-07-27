try:
    from flask import Flask, send_from_directory, abort, request, jsonify
    from dotenv import load_dotenv
    import os
except:
    print("Error at libraries.py importations")
    exit(-1)

# ==============================================================================================

# Load environment variables
load_dotenv()

# Flask app configuration
app = Flask(__name__)

# Defines the directory where the files will be
FILE_DIRECTORY = app.root_path + "\\download"  # Change it if you have another folder

# Getting the API key/password
API_KEY = os.environ.get("API-KEY")  # Create an .env file with this value


#
@app.route("/verify")
def verify():
    if request.args.get('p') != API_KEY:
        return jsonify({"response": False}), 200
    
    return jsonify({"response": True}), 200


# 
@app.route("/list_files")
def list_files():
    if request.args.get('p') != API_KEY:
        return jsonify({"response": []}), 200

    file_list: list[str] = []

    for dirpath, _, filenames in os.walk("."):
        for filename in filenames:
            if dirpath.startswith(".\\download"):
                file_list.append(filename)
    
    return jsonify({"response": file_list}), 200


# Request a download
@app.route("/download/<filename>")
def download_file(filename):
    if request.args.get("p") != API_KEY:
        abort(404)

    try:
        return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# ==============================================================================================

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2024)
