from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so our frontend can communicate with this API
CORS(app)

# The core logic for standard GPA mapping
def get_gp(marks):
    if marks >= 85: return 4.0
    if marks >= 80: return 3.8
    if marks >= 75: return 3.4
    if marks >= 71: return 3.0
    if marks >= 68: return 2.8
    if marks >= 64: return 2.4
    if marks >= 61: return 2.0
    if marks >= 57: return 1.8
    if marks >= 53: return 1.4
    if marks >= 50: return 1.0
    return 0.0

def get_proficiency(score):
    if score >= 3.8: return "Elite Scholar - Outstanding Mastery"
    if score >= 3.4: return "Excellent - Highly Proficient"
    if score >= 3.0: return "Strong Competence - Proficient"
    if score >= 2.5: return "Developing - Room for Growth"
    if score >= 2.0: return "Needs Improvement - Academic Warning"
    return "Critical - Immediate Action Required"

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    calc_type = data.get('calc_type') # 'gpa' or 'cgpa'
    items = data.get('items', [])
    
    total_points = 0
    total_credits = 0

    for item in items:
        credits = float(item.get('credits', 0))
        
        if calc_type == 'gpa':
            marks = float(item.get('score', 0))
            gp = get_gp(marks)
            total_points += (gp * credits)
        else:
            # If CGPA, the user enters their previous GPA directly instead of marks
            gpa = float(item.get('score', 0))
            total_points += (gpa * credits)
            
        total_credits += credits

    final_score = (total_points / total_credits) if total_credits > 0 else 0.0

    return jsonify({
        "final_score": round(final_score, 2),
        "total_credits": total_credits,
        "proficiency": get_proficiency(final_score)
    })

if __name__ == '__main__':
    # Runs the backend API on localhost port 5000
    app.run(debug=True, port=5000)