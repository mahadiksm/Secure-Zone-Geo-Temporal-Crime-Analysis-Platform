import requests
import pandas as pd
import numpy as np

from flask import Flask, jsonify
from flask_cors import CORS

# ML ALGORITHMS
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

# METRICS
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.model_selection import train_test_split

app = Flask(__name__)
CORS(app)

# =========================================
# HOME ROUTE
# =========================================

@app.route('/')
def home():

    return "Flask Working Successfully"


# =========================================
# FETCH DATA FROM PHP
# =========================================

def get_data():

    url = "http://localhost/Chronology/fetch_data.php"

    response = requests.get(url)

    data = response.json()

    df = pd.DataFrame(data)

    return df


# =========================================
# LOCATION ANALYSIS API
# =========================================

@app.route('/location_analysis')

def location_analysis():

    try:

        df = get_data()

        df['crime_count'] = pd.to_numeric(
            df['crime_count'],
            errors='coerce'
        ).fillna(0)

        location_group = df.groupby(
            'location'
        )['crime_count'].sum()

        labels = list(location_group.index)

        values = [
            int(v) for v in location_group.values
        ]

        return jsonify({

            "locations": labels,

            "counts": values

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        })


# =========================================
# TIME ANALYSIS API
# =========================================

@app.route('/time_analysis')

def time_analysis():

    try:

        df = get_data()

        df['crime_count'] = pd.to_numeric(
            df['crime_count'],
            errors='coerce'
        ).fillna(0)

        # CREATE TIME RANGE

        df['time_range'] = (
            df['start_time'].astype(str)
            + " - " +
            df['end_time'].astype(str)
        )

        time_group = df.groupby(
            'time_range'
        )['crime_count'].sum()

        labels = list(time_group.index)

        values = [
            int(v) for v in time_group.values
        ]

        max_val = max(values)

        intensity = []

        for v in values:

            percent = (v / max_val) * 100

            if percent > 60:

                level = "HIGH 🔴"

            elif percent > 30:

                level = "MODERATE 🟡"

            else:

                level = "LOW 🟢"

            intensity.append(level)

        return jsonify({

            "times": labels,

            "counts": values,

            "intensity": intensity

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        })


# =========================================
# OVERALL ML ANALYSIS API
# =========================================

@app.route('/overall_analysis')

def overall_analysis():

    try:

        df = get_data()

        df['year'] = pd.to_numeric(
            df['year'],
            errors='coerce'
        )

        df['crime_count'] = pd.to_numeric(
            df['crime_count'],
            errors='coerce'
        )

        df = df.dropna()

        # GROUP YEARWISE

        df = df.groupby(
            'year'
        )['crime_count'].sum().reset_index()

        df['year'] = df['year'].astype(int)

        df['crime_count'] = df['crime_count'].astype(int)

        X = df[['year']]

        y = df['crime_count']

        # TRAIN TEST SPLIT

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,
            test_size=0.2,
            random_state=42

        )

        # =====================================
        # ALGORITHMS
        # =====================================

        models = {

            "Linear Regression":
            LinearRegression(),

            "Decision Tree":
            DecisionTreeRegressor(),

            "Random Forest":
            RandomForestRegressor(
                n_estimators=50,
                random_state=42
            ),

            "KNN":
            KNeighborsRegressor(),

            "SVR":
            SVR()

        }

        results = []

        # =====================================
        # TRAINING
        # =====================================

        for name, model in models.items():

            model.fit(X_train, y_train)

            pred = model.predict(X_test)

            mae = mean_absolute_error(
                y_test,
                pred
            )

            mse = mean_squared_error(
                y_test,
                pred
            )

            rmse = np.sqrt(mse)

            r2 = r2_score(
                y_test,
                pred
            )

            next_year = np.array([[
                df['year'].max() + 1
            ]])

            future_pred = model.predict(
                next_year
            )

            prediction_value = float(
                abs(future_pred[0])
            )

            accuracy = float(r2 * 100)

            results.append({

                "algorithm": name,

                "accuracy": round(
                    accuracy,
                    2
                ),

                "mae": round(
                    float(mae),
                    2
                ),

                "mse": round(
                    float(mse),
                    2
                ),

                "rmse": round(
                    float(rmse),
                    2
                ),

                "prediction": round(
                    prediction_value,
                    2
                )

            })

        return jsonify({

            "results": results

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        })


# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )