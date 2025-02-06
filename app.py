from flask import Flask, request, jsonify,send_file
from main import get_youtube_transcript, summarize
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/v1/api", methods=["POST"])
def creatJsonFromData():
    url_data = request.get_json() 
    print(url_data) # Get the JSON from the request body
    youtube_url = url_data.get("url")  # Extract the URL from the JSON dictionary
    print(youtube_url)
    
    if youtube_url:
        subtitle = get_youtube_transcript(youtube_url)  # Get the transcript
        if subtitle:
            summary = summarize(subtitle) 
            # final = convert_to_structure(summary)
            print("success") # Summarize the transcript
            return jsonify({"summary": summary}), 200  # Return the summary as JSON
        else:
            return jsonify({"error": "Unable to fetch transcript"}), 400
    else:
        return jsonify({"error": "URL is required"}), 400


if __name__ == "__main__":
    app.run(debug=True)
