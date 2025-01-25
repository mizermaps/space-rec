import os
from flask import Flask, request, render_template_string, jsonify

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

    SEPARATOR = "----------------------------------------------------------"

    # Accumulate output in a list, then join into one string
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

    # Convert to a single HTML-formatted string
    return "<br>".join(output_lines)


# ----------------------------------------------------
# Combined HTML form and result container with styling,
# transitions, and spinning beach ball reset
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
            padding: 20px;
            background-color: #e0e0e0; /* Light gray background */
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }

        h1 {
            color: #4A4A4A; /* Space Gray */
            text-align: center;
            margin-bottom: 20px;
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
            color: #4A4A4A; /* Space Gray */
        }

        input[type="number"], select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            transition: border-color 0.3s;
            background-color: #f9f9f9;
            color: #333;
        }

        input[type="number"]:focus, select:focus {
            border-color: #4A4A4A; /* Space Gray */
            outline: none;
            background-color: #fff;
        }

        input[type="submit"] {
            background: #4A4A4A; /* Space Gray */
            color: #ffffff;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
            width: 100%;
            font-size: 16px;
        }

        input[type="submit"]:hover {
            background: #333333; /* Darker Space Gray */
        }

        .result-container {
            display: none;
            opacity: 0;
            margin-top: 20px;
            text-align: center;
        }

        .visible {
            display: block !important;
            opacity: 1 !important;
        }

        .beach-ball {
            width: 50px;
            height: 50px;
            margin: 20px auto;
            border-radius: 50%;
            background: conic-gradient(#ff6347, #ffa07a, #87cefa, #4682b4, #ff6347); /* Original Colorful Gradient */
            animation: spin 2s linear infinite;
            cursor: pointer;
            border: 2px solid #ccc;
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

        /* Loader styles */
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4A4A4A; /* Space Gray */
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 10px auto;
        }

    </style>
</head>
<body>
    <h1>Space Recommender</h1>
    <form id="inputForm">
        <label for="people_count">Number of People:</label>
        <input type="number" name="people_count" value="1" min="1" required>

        <label for="using_phone">Phone/Web Call Usage?</label>
        <select name="using_phone" required>
            <option value="" disabled selected>Select an option</option>
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select>

        <label for="using_laptop">Laptop Usage?</label>
        <select name="using_laptop" required>
            <option value="" disabled selected>Select an option</option>
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select>

        <input type="submit" value="Submit">
    </form>

    <div class="result-container" id="resultContainer">
        <h2>Result:</h2>
        <div id="resultContent"></div>
        <!-- Spinning beach ball for reset -->
        <div class="beach-ball" id="resetButton" title="Start Over"></div>
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
            form.style.pointerEvents = 'none'; // Disable form during submission

            // Show a loader
            const loader = document.createElement('div');
            loader.className = 'loader';
            form.appendChild(loader);

            // Collect form data
            const formData = new FormData(form);

            // Send POST request via fetch
            fetch('/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                return response.json();
            })
            .then(data => {
                // Remove loader
                form.removeChild(loader);

                // Hide the form
                form.style.display = 'none';

                // Populate the result content
                resultContent.innerHTML = data.result;

                // Fade in the result container
                resultContainer.classList.add('visible');
            })
            .catch(error => {
                // Remove loader
                form.removeChild(loader);

                // Re-enable form
                form.style.opacity = '1';
                form.style.pointerEvents = 'auto';

                // Display error message
                alert('An error occurred: ' + error.message);
            });
        });

        resetButton.addEventListener('click', function() {
            // Hide the result container
            resultContainer.classList.remove('visible');

            // Clear the result content
            resultContent.innerHTML = '';

            // Reset and show the form
            form.style.display = 'block';
            form.style.opacity = '1';
            form.style.pointerEvents = 'auto';

            // Reset form fields
            form.reset();
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    On GET: Display the form.
    On POST: If AJAX, return JSON with the result.
             Else, render the full page with the result.
    """
    if request.method == 'POST':
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

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

        if is_ajax:
            # Return JSON response for AJAX
            return jsonify({'result': result})
        else:
            # Non-AJAX POST, render the full page
            return render_template_string(HTML_FORM, result=result)

    # GET request, render the form
    return render_template_string(HTML_FORM)

# ----------------------------------------------------
# Entry point for local development and Render
# ----------------------------------------------------
if __name__ == '__main__':
    # Render dynamically sets PORT; locally defaults to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
