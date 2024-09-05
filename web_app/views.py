import os
import pandas as pd
from flask import Blueprint, request, render_template, current_app, send_from_directory

from .scripts.scraping_reviews import scrape_reviews

from datetime import datetime
import pytz

views = Blueprint('views', __name__)

@views.route('/')
def home():
    feature_title = 'Home'
    context = {
        'feature_title': feature_title,
    }
    return render_template("home.html", context=context)

@views.route('/scraping', methods=['GET', 'POST'])
def scraping():
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
        
    feature_title = 'Data Scraping'

    context = {
        'feature_title': feature_title,
    }
    return render_template("features/scraping.html", context=context)


@views.route('/eda')
def eda():
    feature_title = 'Exploratory Data Analysis'
    context = {
        'feature_title': feature_title,
    }
    return render_template("features/eda.html", context=context)

@views.route('/pre-processing')
def preprocessing():
    feature_title = 'Data Pre-Processing'
    context = {
        'feature_title': feature_title,
    }
    return render_template("features/pre-processing.html", context=context)

@views.route('/modeling-evaluation')
def modeling_evaluation():
    feature_title = 'Modeling & Evaluation'
    context = {
        'feature_title': feature_title,
    }
    return render_template("features/modeling-evaluation.html", context=context)

@views.route('/prediction')
def prediction():
    feature_title = 'Data Prediction'
    context = {
        'feature_title': feature_title,
    }
    return render_template("features/prediction.html", context=context)

