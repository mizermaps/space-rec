from flask import Flask, request, render_template_string

app = Flask(__name__)

# ----------------------------------------------------
# Your space recommender logic, adapted to return a string
# ----------------------------------------------------
def space_recommender(people_count, using_phone, using_laptop):
    LIKE_CONF = "This situation is 'like a Conference.'"
    LIKE_CONV = "This situation is 'like a Conversation.'"
    OFFICE_RECO = "RECOMMENDATION: Use an OFFICE."
    PHONE_RECO = "RECOMMENDATION: Use a PHONE ROOM."

    EXPL_3PLUS = "Reason: With 3+ people, you need a larger, more formal space."
    EXPL_12_PHONE = "Reason: 1–2 people + phone usage => Office."
    EXPL_12_LAPTOP = "Reason: 1–2 people + laptop usage => Office."
    EXPL_12_BOTH = "Reason: 1–2 people + phone + laptop => Definitely Office."
    EXPL_12_NONE = "Reason: 1–2 people, no phone, no laptop => a more casual discussion fits a Phone Room."

    SUMMARY_TEXT = """Thank you for using the Space Recommender!<br><br>
    Summary of Logic:<br>
    • If 3+ people => 'like a conference' => Use an OFFICE.<br>
    • If only 1 or 2 people:<br>
       - If phone OR laptop => OFFICE<br>
       - Else => PHONE ROOM<br>
    """

    SEPARATOR = "----------------------------------------------------------"

    # We'll accumulate our output in a list, then join into one string
    output_lines = []

    # MAIN DECISION LOGIC
    if people_count >= 3:
        output_lines.append(f"<br>{SEPARATOR}")
        output_lines.append(LIKE_CONF)
        output_lines.append(SEPARATOR)
        output_lines.append(OFFICE_RECO)
        output_lines.append(EXPL_3PLUS)
        output_lines.append(SEPARATOR)
    else:
        # 1 or 2 people
        if using_phone or using_laptop:
            output_lines.append(f"<br>{SEPARATOR}")
            output_lines.append(LIKE_CONF)
            output_lines.append(SEPARATOR)
            output_lines.append(OFFICE_RECO)

            if using_phone and not using_laptop:
                output_lines.append(EXPL_12_PHONE)
            elif using_laptop and not using_phone:
                output_lines.append(EXPL_12_LAPTOP)
            else:
                output_lines.append(EXPL_12_BOTH)
            output_lines.append(SEPARATOR)
        else:
            # No phone, no laptop => Phone Room
            output_lines.append(f"<br>{SEPARATOR}")
            output_lines.append(LIKE_CONV)
            output_lines.append(SEPARATOR)
            output_lines.append(PHONE_RECO)
            output_lines.append(EXPL_12_NONE)
            output_lines.append(SEPARATOR)

    # Append summary text
    output_lines.append("")
    output_lines.append(SUMMARY_TEXT)

    # Convert to a single HTML-formatted string
    return "<br>".join(output_lines)


# ----------------------------------------------------
# Simple HTML form that POSTs to the same route
# ----------------------------------------------------
HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Space Recommender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        h1 {
            color: #5A67D8;
        }

        form, .result-container {
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 400px;
            width: 100%;
            transition: opacity 0.5s ease;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }

        input[type="number"], select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            transition: border-color 0.3s;
        }

        input[type="number"]:focus, select:focus {
            border-color: #5A67D8;
            outline: none;
        }

        input[type="submit"] {
            background: #5A67D8;
            color: #ffffff;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }

        input[type="submit"]:hover {
            background: #434190;
        }

        .result-container {
            display: none;
            opacity: 0;
        }

        .visible {
            display: block;
            opacity: 1;
        }

        .beach-ball {
            width: 50px;
            height: 50px;
            margin: 20px auto;
            border-radius: 50%;
            background: conic-gradient(#ff6347, #ffa07a, #87cefa, #4682b4, #ff6347);
            animation: spin 2s linear infinite;
            cursor: pointer;
        }

        @keyframes spin {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
        }

        @media (max-width: 600px) {
            form, .result-container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <h1>Space Recommender</h1>
    <form id="inputForm" method="POST">
        <label for="people_count">Number of People:</label>
        <input type="number" name="people_count" value="1" min="1" required>

        <label for="using_phone">Phone/Web Call Usage?</label>
        <select name="using_phone">
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select>

        <label for="using_laptop">Laptop Usage?</label>
        <select name="using_laptop">
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select>

        <input type="submit" value="Submit">
    </form>

    <div class="result-container" id="resultContainer">
        <h2>Result:</h2>
        <p id="resultContent"></p>
        <div class="beach-ball" id="resetButton"></div>
    </div>

    <script>
        const form = document.getElementById('inputForm');
        const resultContainer = document.getElementById('resultContainer');
        const resultContent = document.getElementById('resultContent');
        const resetButton = document.getElementById('resetButton');

        form.addEventListener('submit', function(event) {
            event.preventDefault();

            // Fade out the form
            form.style.opacity = '0';
            setTimeout(() => {
                form.style.display = 'none';
                // Update the result content and fade in the result box
                const formData = new FormData(form);
                fetch('/', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.text())
                .then(data => {
                    resultContent.innerHTML = data.split('<body>')[1].split('</body>')[0]; // Get the result content from the response
                    resultContainer.classList.add('visible');
                });
            }, 500);
        });

        resetButton.addEventListener('click', function() {
            // Reset form and result display
            resultContainer.classList.remove('visible');
            setTimeout(() => {
                form.style.display = 'block';
                form.style.opacity = '1';
            }, 500);
        });
    </script>
</body>
</html>



@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        # 1) Grab inputs from the form
        people_count = request.form.get('people_count', '1')
        using_phone = request.form.get('using_phone', 'no')
        using_laptop = request.form.get('using_laptop', 'no')

        try:
            people_count = int(people_count)
        except ValueError:
            people_count = 1  # fallback if something invalid is entered

        phone_bool = (using_phone.lower() == 'yes')
        laptop_bool = (using_laptop.lower() == 'yes')

        # 2) Run the space recommender logic
        result = space_recommender(people_count, phone_bool, laptop_bool)

    # Render the form, optionally with the result
    return render_template_string(HTML_FORM, result=result)

# ----------------------------------------------------
# For local development use only:
# ----------------------------------------------------
if __name__ == '__main__':
    # Access at http://127.0.0.1:5000
    app.run(debug=True)
