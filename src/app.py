from flask import Flask, request, render_template_string
import pandas as pd
from dtd_calculator import AVCalculator
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>📊 DTD Calculator</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      padding: 40px;
      background-color: #f9f9f9;
    }
    h1 {
      margin-bottom: 30px;
    }
    .upload-box {
      padding: 20px;
      border: 1px solid #ddd;
      background: white;
      border-radius: 8px;
      max-width: 600px;
      margin: auto;
    }
    table.data {
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="upload-box">
    <h1 class="text-center">📈 DTD Calculator</h1>
    <form method="post" enctype="multipart/form-data" class="mb-3">
      <div class="mb-3">
        <label for="formFile" class="form-label">Upload your CSV file</label>
        <input class="form-control" type="file" name="file" id="formFile">
      </div>
      <button type="submit" class="btn btn-primary">Upload & Calculate</button>
    </form>

    {% if message %}
      <div class="alert alert-{{ 'success' if success else 'danger' }}">{{ message }}</div>
    {% endif %}

    {% if tables %}
      <h4 class="mt-4">✅ Results</h4>
      <div class="table-responsive">
        {{ tables|safe }}
      </div>
    {% endif %}
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    tables = None
    message = None
    success = False

    if request.method == 'POST':
        if 'file' not in request.files:
            message = "No file part in request."
            return render_template_string(HTML_TEMPLATE, tables=None, message=message, success=False)

        file = request.files['file']
        if file.filename == '':
            message = "No file selected."
            return render_template_string(HTML_TEMPLATE, tables=None, message=message, success=False)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            calc = AVCalculator(filepath)
            df = calc.run()
            tables = df.to_html(classes='table table-striped table-bordered data', index=False)
            message = "File processed successfully!"
            success = True
        except Exception as e:
            message = f"❌ Error processing file: {e}"
            success = False

    return render_template_string(HTML_TEMPLATE, tables=tables, message=message, success=success)

if __name__ == '__main__':
    app.run(debug=True)