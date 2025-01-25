import os
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
<html>
<head>
    <title>Space Recommender</title>
</head>
<body>
    <h1>Space Recommender</h1>
    <p>Enter details below:</p>
    <form method="POST">
        <label for="people_count">Number of People:</label>
        <input type="number" name="people_count" value="1" min="1" required><br><br>

        <label for="using_phone">Phone/Web Call Usage?</label>
        <select name="using_phone">
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select><br><br>

        <label for="using_laptop">Laptop Usage?</label>
        <select name="using_laptop">
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select><br><br>

        <input type="submit" value="Submit">
    </form>

    {% if result %}
    <hr>
    <h2>Result:</h2>
    <p>{{ result|safe }}</p>
    {% endif %}
</body>
</html>
"""

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
# Entry point for local development and Render:
# ----------------------------------------------------
if __name__ == '__main__':
    # Render uses PORT env variable; default to 5000 locally
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
