from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import base64
import dotenv
import os

app = Flask(__name__)
CORS(app)
dotenv.load_dotenv()


@app.route("/tarea4-201900462", methods=["POST"])
def compare_faces():
    content = request.json
    source_image_data = content["sourceImage"].split(",")[-1]
    target_image_data = content["targetImage"].split(",")[-1]

    source_image = base64.b64decode(source_image_data)
    target_image = base64.b64decode(target_image_data)

    client = boto3.client(
        "rekognition",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("REKOGNITION_PUBLIC_KEY"),
        aws_secret_access_key=os.getenv("REKOGNITION_PRIVATE_KEY"),
    )

    try:
        response = client.compare_faces(
            SourceImage={"Bytes": source_image}, TargetImage={"Bytes": target_image}
        )

        faceMatches = response["FaceMatches"]
        similarity = faceMatches[0]["Similarity"] if faceMatches else 0

        return jsonify({"similarity": similarity})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
