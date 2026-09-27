
# Import data manipulation libraries
import numpy as np
import pandas as pd

# For serialization
import joblib

# Flask API
from flask import Flask, request, jsonify

# Import logging
import logging
import sys


# ---------------------------------------------------------
# Initialize Flask app
# ---------------------------------------------------------

lead_conversion_api = Flask("lead_conversion_app")


# ---------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


logger.info(f"Module name: {__name__}")
logger.info(f"Flask app name: {lead_conversion_api.name}")
logger.info(f"Root path: {lead_conversion_api.root_path}")


# ---------------------------------------------------------
# Load the trained model
# ---------------------------------------------------------

model = joblib.load(
    "lead_conversion_model.joblib"
)


# ---------------------------------------------------------
# Features expected from API input
# ---------------------------------------------------------

FEATURES = [
    'age',
    'website_visits',
    'time_spent_on_website',
    'page_views_per_visit',
    'current_occupation',
    'first_interaction',
    'profile_completed',
    'last_activity',
    'print_media_type1',
    'print_media_type2',
    'digital_media',
    'educational_channels',
    'referral'
]


# ---------------------------------------------------------
# Home endpoint
# ---------------------------------------------------------

@lead_conversion_api.route('/', methods=['GET'])
def home():

    return """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Lead Conversion Prediction API</title>
    </head>

    <body>

        <h1>Welcome to Lead Conversion Prediction API</h1>

        <p>
            To obtain a lead conversion prediction,
            send a POST request to:
        </p>

        <p>
            <code>/v1/predict</code>
        </p>

    </body>

    </html>
    """


# ---------------------------------------------------------
# Preprocessing function
# ---------------------------------------------------------

def preprocess_input(input_data):

    """
    Apply the same encoding used during model training.
    """

    # Apply one-hot encoding
    input_data = pd.get_dummies(
        input_data,
        drop_first=True
    )

    # Convert Boolean values to integers
    input_data = input_data.astype(int)

    # Get the feature names used by the trained model
    expected_columns = model.feature_names_in_

    # Add missing encoded columns
    for column in expected_columns:

        if column not in input_data.columns:
            input_data[column] = 0

    # Keep only the columns used during training
    input_data = input_data.reindex(
        columns=expected_columns,
        fill_value=0
    )

    return input_data


# ---------------------------------------------------------
# Single prediction endpoint
# ---------------------------------------------------------

@lead_conversion_api.route(
    '/v1/predict',
    methods=['POST']
)
def predict_lead():

    try:

        # Read JSON request
        data = request.get_json()

        # Check for empty request
        if not data:

            return jsonify({
                'error': 'Request body cannot be empty'
            }), 400


        # Check required fields
        missing_fields = [
            field
            for field in FEATURES
            if field not in data
        ]


        if missing_fields:

            return jsonify({

                'error': 'Missing required fields',

                'fields': missing_fields

            }), 400


        # Create DataFrame
        input_data = pd.DataFrame(
            [[data[field] for field in FEATURES]],
            columns=FEATURES
        )


        logger.info(
            f"Prediction input:\n{input_data}"
        )


        # Preprocess input
        processed_data = preprocess_input(
            input_data
        )


        # Make prediction
        prediction = model.predict(
            processed_data
        )[0]


        # Convert prediction into meaningful status
        status = (
            "Converted"
            if prediction == 1
            else "Not Converted"
        )


        return jsonify({

            'prediction': int(prediction),

            'status': status

        })


    except Exception as e:

        logger.exception(
            "Prediction failed"
        )

        return jsonify({

            'error':
            f'Prediction failed: {str(e)}'

        }), 500


# ---------------------------------------------------------
# Run Flask application
# ---------------------------------------------------------

if __name__ == '__main__':

    lead_conversion_api.run(
        host='0.0.0.0',
        port=7860,
        debug=True
    )
