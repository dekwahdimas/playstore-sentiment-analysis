import os
from datetime import datetime

from flask import Blueprint, request, current_app, render_template, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
import pytz

from .scripts.scraping_reviews import scrape_reviews
from .scripts.eda import explore_data
from .scripts.pre_processing import do_pre_processing
from .scripts.modeling_evaluation import modeling_and_evaluation

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

@views.route('/')
def home():
    feature_title = 'Home'
    context = {
        'feature_title': feature_title,
    }
    return render_template("home.html", context=context)


@views.route('/scraping', methods=['GET', 'POST'])
def scraping():
    feature_title = 'Data Scraping'
    if request.method == 'POST':
        app_id = request.form['app_id']
        total_scrape = int(request.form['total_scrape'])
        filter_score = request.form['filter_score']

        filter_score = None if filter_score == 'ALL' else int(filter_score)
        timestamp_scrape = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y_%H-%M-%S")

        df = scrape_reviews(app_id, total_scrape, filter_score)

        # Save the result to a CSV file
        filename = f"dataset_{app_id[4:].capitalize()}_{filter_score}_{total_scrape}_{timestamp_scrape}.csv"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Create the uploads folder if it doesn't exist
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        df.to_csv(filepath, index=False)

        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        
    return render_template("features/scraping.html", context={'feature_title': feature_title})


@views.route('/eda', methods=['GET', 'POST'])
def eda():
    feature_title = 'Exploratory Data Analysis'
    if request.method == 'POST':
        filepath = upload_file()
        df, headers, data = explore_data(filepath)

        # Create the uploads folder if it doesn't exist
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        df.to_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], f'EDA_{filepath.split("_")[1]}.csv'), index=False)

        context = {
            'feature_title': feature_title,
            'headers': headers,
            'data': data,
        }
        return render_template("features/eda.html", context=context)
    
    return render_template("features/eda.html", context={'feature_title': feature_title})


@views.route('/pre-processing', methods=['GET', 'POST'])
def preprocessing():
    feature_title = 'Data Pre-Processing'
    if request.method == 'POST':
        filepath = upload_file()
        df, headers, data = do_pre_processing(filepath)

        # Create the uploads folder if it doesn't exist
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        df.to_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], f'pre-processed_{filepath.split("_")[1]}.csv'), index=False)

        context = {
            'feature_title': feature_title,
            'headers': headers,
            'data': data,
        }
        return render_template("features/pre-processing.html", context=context)
    
    return render_template("features/pre-processing.html", context={'feature_title': feature_title})


@views.route('/modeling-evaluation', methods=['GET', 'POST'])
def modeling_evaluation():
    feature_title = 'Modeling & Evaluation'
    if request.method == 'POST':
        filepath = upload_file()
        chosen_model = request.form['chosen_model']
        cr, cm = modeling_and_evaluation(filepath, chosen_model)

        context = {
            'feature_title': feature_title,
            'classification_report': cr,
            'confusion_matrix': cm,
        }
        
        return render_template("features/modeling-evaluation.html", context=context)
    
    return render_template("features/modeling-evaluation.html", context={'feature_title': feature_title})


@views.route('/prediction')
def prediction():
    feature_title = 'Data Prediction'
    context = {
        'feature_title': feature_title,
    }
    return render_template("features/prediction.html", context=context)


# -------------------------Functions
# Check allowed file to be uploaded
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Receive uploaded file from user
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        # flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        # flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    return filepath