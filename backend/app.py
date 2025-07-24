from flask import Flask, request
from flask_cors import CORS 
from questions import Questions
from model.matching_logic import Matches
from flask import jsonify

app = Flask(__name__, template_folder="../templates")
CORS(app, origins="*")

TOTAL_ID = 10

DATA_PATH = "/Users/chansoon/Downloads/Matching Logic - Sheet1.csv"

try:
    match = Matches(data_path=DATA_PATH, student_status=True)
    questions = Questions()
    print("Successfully intialized the matching and questions system")

except Exception as e:
    print(f"Failed to intialize the matching system and questions system: {e}")
    match, questions = None, None

@app.route("/api/get-question", methods=["GET"])
def get_question():
    """
    Sends the payload of the requested question.
    """
    try:
        if not questions:
            return jsonify({"error" : "The question system was not successfully initialized"}), 500

        question_id = int(request.args.get("question_id"))

        if question_id > TOTAL_ID - 2:
            return jsonify({"error" : "Question and question IDs don't exist"}), 404

        question = questions.get_question(question_id)

        return jsonify(question), 200

    except Exception as e:
        return jsonify({"error" : f"Failed to get next question: {str(e)}"}), 500

@app.route("/api/update-role", methods=["POST"])
def update_role():
    """
    Front end POST data in object form: {
        "answer" : answer,
        "question_id" : question_id
    } with question_id being a str
    """
    try:
        if not match:
            return jsonify({"error": "Matching system not initialized"}), 500

        data = request.get_json()

        if not data:
            return jsonify({"error" : "No data received"}), 500

        # Validate required fields
        if not "answer" in data or not "question_id" in data:
            return jsonify({"error" : "Data was not formatted correctly, missing field requirements"}), 404 

        match.next_assessment(data)

        return jsonify({"status": "Success", "message" : "Role updated successfuly"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to update role: {str(e)}"}), 500

@app.route("/api/get-roles", methods=["GET"])
def get_best_fit_roles():
    try:
        if not match:
            return jsonify({"error": "Matching system not initialized"}), 500

        best_roles = match.get_best_fit_roles()

        if not best_roles:
            return jsonify({"error" : "no best fit roles data"}), 400

        # Validate required fields
        if not "Best fit roles" in best_roles:
            return jsonify({
                "error" : "Data was not formatted correctly, missing field requirements"
            }), 404 

        return jsonify(best_roles), 200

    except Exception as e:
        return jsonify({"error" : f"Failed to get best fit roles: {str(e)}"}), 500

@app.route("/api/reset", methods=["POST"])
def reset_assessment():
    try:
        global match, questions
        match = Matches(data_path=DATA_PATH, student_status=True)
        questions = Questions()
        
        return jsonify({
            "status": "Success", 
            "message" : "Assessment system reset successfully"
        }), 200

    except Exception as e:
         return jsonify({"error" : f"Failed to reset assessment system: {str(e)}"}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error" : "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error" : "Internal server error"}), 500
        
if __name__ == "__main__":
    print("Starting Flask development server...")
    app.run(debug=True)