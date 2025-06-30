from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests from your frontend

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    try:
        image_file = request.files['image']
        input_image = Image.open(image_file.stream).convert("RGBA")
        output_image = remove(input_image)

        byte_io = io.BytesIO()
        output_image.save(byte_io, 'PNG')
        byte_io.seek(0)

        return send_file(byte_io, mimetype='image/png')

    except Exception as e:
        return f"Error processing image: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)