from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image
import os
from models import db, ImageModel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    width = int(request.form['width'])
    height = int(request.form['height'])

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Resize image
        img = Image.open(filepath)
        img = img.resize((width, height))
        resized_path = os.path.join(app.config['UPLOAD_FOLDER'], f"resized_{file.filename}")
        img.save(resized_path)

        # Save to DB
        new_image = ImageModel(
            original_filename=file.filename,
            resized_filename=f"resized_{file.filename}",
            original_path=filepath,
            resized_path=resized_path,
            width=width,
            height=height
        )
        db.session.add(new_image)
        db.session.commit()

        return redirect(url_for('view_image', image_id=new_image.id))
    return "Failed to upload image"

@app.route('/image/<int:image_id>')
def view_image(image_id):
    image = ImageModel.query.get_or_404(image_id)
    return render_template('view_image.html', image=image)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
