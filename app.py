from antigravity import app
import re

def check_strength(password):
    score = 0
    feedback = []
    
    # 1. Length Logic
    length = len(password)
    if length < 8:
        score += 10
        feedback.append("Password is too short (min 8 chars).")
    elif 8 <= length <= 12:
        score += 20
    else:
        score += 30

    # 2. Character presence logic
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    if has_upper: score += 15
    else: feedback.append("Add uppercase letters.")
    
    if has_lower: score += 15
    else: feedback.append("Add lowercase letters.")
    
    if has_digit: score += 20
    else: feedback.append("Add numbers.")
    
    if has_special: score += 20
    else: feedback.append("Add special characters (!@#$...).")

    # Final label
    if length < 8:
        strength = "Weak"
        score = min(score, 35) # Cap short passwords
    elif score < 50:
        strength = "Weak"
    elif score <= 75:
        strength = "Moderate"
    else:
        strength = "Strong"

    return {
        "strength": strength,
        "score": score,
        "feedback": feedback
    }

@app.route("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read(), 200, "text/html"

@app.route("/check-password", methods=["POST"])
def api_check(data):
    password = data.get("password", "")
    result = check_strength(password)
    return result, 200, "application/json"

if __name__ == "__main__":
    app.listen(8000)
