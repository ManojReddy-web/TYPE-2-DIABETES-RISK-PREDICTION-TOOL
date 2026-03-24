from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# -----------------------------
# Risk Calculation Function
# -----------------------------
def calculate_risk(data):
    score = 0
    reasons = []

    try:
        age = int(data.get("age", 0))
        bmi = float(data.get("bmi", 0))
        fbs = float(data.get("fbs", 0))
        hba1c = float(data.get("hba1c", 0))
    except:
        return 0, ["Invalid input values"]

    # Age
    if age >= 45:
        score += 15
        reasons.append("Age above 45")

    # BMI
    if bmi >= 25:
        score += 10
        reasons.append("High BMI")

    # FBS
    if fbs >= 126:
        score += 25
        reasons.append("High Fasting Blood Sugar")

    # HbA1c
    if hba1c >= 6.5:
        score += 25
        reasons.append("High HbA1c")

    # Risk Level
    if score < 20:
        level = "Low Risk"
    elif score < 50:
        level = "Moderate Risk"
    else:
        level = "High Risk"

    return level, reasons


# -----------------------------
# Home Page
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    reasons = []

    if request.method == "POST":
        result, reasons = calculate_risk(request.form)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Diabetes Risk Predictor</title>
        <style>
            body {
                font-family: Arial;
                background: #eef3f9;
                text-align: center;
            }
            .container {
                background: white;
                padding: 20px;
                margin: 50px auto;
                width: 350px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px gray;
            }
            input {
                margin: 8px;
                padding: 8px;
                width: 90%;
            }
            button {
                padding: 10px;
                background: #1565c0;
                color: white;
                border: none;
                border-radius: 5px;
            }
            .result {
                margin-top: 20px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h2>Type 2 Diabetes Risk Predictor</h2>

            <form method="POST">
                <input type="number" name="age" placeholder="Age" required>
                <input type="number" step="0.1" name="bmi" placeholder="BMI" required>
                <input type="number" step="0.1" name="fbs" placeholder="FBS" required>
                <input type="number" step="0.1" name="hba1c" placeholder="HbA1c" required>
                <br>
                <button type="submit">Check Risk</button>
            </form>

            {% if result %}
                <div class="result">
                    <p>Risk Level: {{result}}</p>
                    <p>Reasons:</p>
                    <ul>
                        {% for r in reasons %}
                            <li>{{r}}</li>
                        {% endfor %}
                    </ul>
                </div>
            {% endif %}

            <p style="margin-top:20px; font-size:12px;">
            Developed by Manoj Reddy
            </p>

        </div>

    </body>
    </html>
    """, result=result, reasons=reasons)


# -----------------------------
# Run App (for Render)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
