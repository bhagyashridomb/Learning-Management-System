from app import db

# Define the Student model
class Student(db.Model):
    __tablename__ = 'students'
    stud_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    learning_style = db.Column(db.String(50))
    current_level = db.Column(db.String(50))
    progress = db.Column(db.Float)

    # Relationship with Performance and Recommendations
    performances = db.relationship('Performance', backref='student', lazy=True)
    #recommendations = db.relationship('Recommendation', backref='student', lazy=True)

# Define the Course model
class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    difficulty = db.Column(db.String(50))
    prerequisite_cid = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    prerequisites = db.relationship('Course', remote_side=[course_id], backref='prerequisite_courses')
    # Relationship with Materials
    materials = db.relationship('Material', backref='course', lazy=True)
    # Relationship with Assessments
    assessments = db.relationship('Assessment', backref='course_assessments', lazy=True)

class Material(db.Model):
    __tablename__ = 'materials'
    material_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    material_type = db.Column(db.Enum('video', 'article', 'quiz'), nullable=False)
    content = db.Column(db.Text)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))  # Ensure this is correctly referenced

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    assessment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    assessment_type = db.Column(db.Enum('assignment', 'quiz'), nullable=False)
    questions = db.Column(db.Text, nullable=False)
    grading_scheme = db.Column(db.Text, nullable=False)
    
    # Relationships
    course = db.relationship('Course', backref='course_related_assessments')
    
    # Define the Performance model
class Performance(db.Model):
    performance_id = db.Column(db.Integer, primary_key=True)
    stud_id = db.Column(db.Integer, db.ForeignKey('students.stud_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    score = db.Column(db.Float)
    completion_date = db.Column(db.Date)
    feedback = db.Column(db.Text)

# Define the Recommendation model
class Recommendation(db.Model):
    __tablename__ = 'recommendations'  # Ensure this matches your table name

    recommendation_id = db.Column(db.Integer, primary_key=True)
    stud_id = db.Column(db.Integer, db.ForeignKey('students.stud_id'))  # Adjust as needed
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))  # Adjust as needed
    recommended_material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))  # Adjust as needed
    reason_for_recommendation = db.Column(db.String(255))

    student = db.relationship('Student', backref='recommendations')  # Adjust as needed
    course = db.relationship('Course', backref='recommendations')  # Adjust as needed
    material = db.relationship('Material', backref='recommendations')  # Adjust as needed

