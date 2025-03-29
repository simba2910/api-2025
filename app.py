from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    program = db.Column(db.String(100), nullable=False)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    program = db.Column(db.String(100), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()
    
    # Populate with sample data if empty
    if not Student.query.first():
        students = [
            Student(name="John Doe", program="Software Engineering"),
            Student(name="Jane Smith", program="Computer Science"),
            Student(name="Alice Johnson", program="Software Engineering"),
            Student(name="Bob Brown", program="Information Technology"),
            Student(name="Charlie Davis", program="Software Engineering"),
            Student(name="Diana Evans", program="Computer Science"),
            Student(name="Ethan Garcia", program="Software Engineering"),
            Student(name="Fiona Harris", program="Information Technology"),
            Student(name="George Clark", program="Software Engineering"),
            Student(name="Hannah Lewis", program="Computer Science")
        ]
        db.session.add_all(students)
        
    if not Subject.query.first():
        subjects = [
            # Year 1
            Subject(name="Introduction to Programming", year=1, program="Software Engineering"),
            Subject(name="Discrete Mathematics", year=1, program="Software Engineering"),
            Subject(name="Computer Fundamentals", year=1, program="Software Engineering"),
            # Year 2
            Subject(name="Data Structures", year=2, program="Software Engineering"),
            Subject(name="Algorithms", year=2, program="Software Engineering"),
            Subject(name="Database Systems", year=2, program="Software Engineering"),
            # Year 3
            Subject(name="Software Engineering", year=3, program="Software Engineering"),
            Subject(name="Computer Networks", year=3, program="Software Engineering"),
            Subject(name="Web Development", year=3, program="Software Engineering"),
            # Year 4
            Subject(name="Project Management", year=4, program="Software Engineering"),
            Subject(name="Distributed Systems", year=4, program="Software Engineering"),
            Subject(name="Advanced Algorithms", year=4, program="Software Engineering")
        ]
        db.session.add_all(subjects)
        
    db.session.commit()

# API Endpoints
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.limit(10).all()
    return jsonify([{'name': s.name, 'program': s.program} for s in students])

@app.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.filter_by(program="Software Engineering").order_by(Subject.year).all()
    result = {}
    for subject in subjects:
        if f"Year {subject.year}" not in result:
            result[f"Year {subject.year}"] = []
        result[f"Year {subject.year}"].append(subject.name)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)