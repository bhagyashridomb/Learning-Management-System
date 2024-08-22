from flask import render_template, request, redirect, url_for, flash,send_file
from app import app, db
from app.models import Student, Course, Material, Assessment, Performance, Recommendation
from app.forms import AddStudentForm, AddCourseForm, AddMaterialForm, PerformanceForm, RecommendationForm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Route to list all students
@app.route('/students')
def students():
    all_students = Student.query.all()
    return render_template('students.html', students=all_students)

# Route to view a single student's profile and performance
@app.route('/student/<int:stud_id>')
def student_profile(stud_id):
    student = Student.query.get_or_404(stud_id)
    performances = Performance.query.filter_by(stud_id=stud_id).all()
    recommendations = Recommendation.query.filter_by(stud_id=stud_id).all()
    return render_template('student_profile.html', student=student, performances=performances, recommendations=recommendations)

# Route to list all courses
@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

# Route to view a single course's details and materials
@app.route('/course/<int:course_id>')
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    materials = Material.query.filter_by(course_id=course_id).all()
    assessments = Assessment.query.filter_by(course_id=course_id).all()
    return render_template('course_details.html', course=course, materials=materials, assessments=assessments)

# Route to add a new student
@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = Student(
            name=form.name.data,
            email=form.email.data,
            learning_style=form.learning_style.data,
            current_level=form.current_level.data,
            progress=form.progress.data
        )
        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        except:
            flash('Error! Could not add student.', 'danger')
    return render_template('add_student.html', form=form)

# Route to add a new course
@app.route('/course/add', methods=['GET', 'POST'])
def add_course():
    form = AddCourseForm()
    if form.validate_on_submit():
        # Create a new Course instance from the form data
        new_course = Course(
            course_name=form.course_name.data,
            description=form.description.data,
            difficulty=form.difficulty.data,
            prerequisite_cid=form.prerequisite_cid.data
        )
        try:
            db.session.add(new_course)
            db.session.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('courses'))
        except Exception as e:
            db.session.rollback()  # Roll back the session in case of an error
            flash(f'Error! Could not add course. Details: {str(e)}', 'danger')
            print(f"Database error: {str(e)}")  # Print the specific error
    else:
        print("Form validation failed with errors:", form.errors)  # Print form validation errors

    # Ensure the template name is correct and matches the actual file
    return render_template('add_course.html', form=form)

# Route to add a new material to a course
@app.route('/course/<int:course_id>/material/add', methods=['GET', 'POST'])
def add_material(course_id):
    course = Course.query.get_or_404(course_id)
    form = AddMaterialForm()
    if form.validate_on_submit():
        new_material = Material(
            course_id=course_id,
            material_type=form.material_type.data,
            content=form.content.data,
            difficulty=form.difficulty.data
        )
        try:
            db.session.add(new_material)
            db.session.commit()
            flash('Material added successfully!', 'success')
            return redirect(url_for('course_details', course_id=course_id))
        except:
            flash('Error! Could not add material.', 'danger')
    return render_template('add_materials.html', course=course, form=form)

# Route to record student performance for an assessment
@app.route('/performance/add', methods=['POST'])
def add_performance():
    form = PerformanceForm()
    if form.validate_on_submit():
        new_performance = Performance(
            stud_id=form.stud_id.data,
            course_id=form.course_id.data,
            score=form.score.data,
            completion_date=form.completion_date.data,
            feedback=form.feedback.data
        )
        try:
            db.session.add(new_performance)
            db.session.commit()
            flash('Performance recorded successfully!', 'success')
        except:
            flash('Error! Could not record performance.', 'danger')
    return redirect(url_for('student_profile', stud_id=form.stud_id.data))

# Route to manage recommendations
@app.route('/recommendation/add', methods=['POST'])
def add_recommendation():
    form = RecommendationForm()
    if form.validate_on_submit():
        new_recommendation = Recommendation(
            stud_id=form.stud_id.data,
            course_id=form.course_id.data,
            recommended_material_id=form.recommended_material_id.data,
            reason_for_recommendation=form.reason_for_recommendation.data
        )
        try:
            db.session.add(new_recommendation)
            db.session.commit()
            flash('Recommendation added successfully!', 'success')
        except:
            flash('Error! Could not add recommendation.', 'danger')
    return redirect(url_for('student_profile', stud_id=form.stud_id.data))

app.route('/student_performance/<int:student_id>')
def student_performance(student_id):
    student = Student.query.get(student_id)
    performances = Performance.query.filter_by(student_id=student_id).all()
    return render_template('student_performance.html', student=student, performances=performances)

@app.route('/performance_summary')
def performance_summary():
    # Fetch performance data from the database
    performance_data = pd.read_sql_query("SELECT * FROM performance", con=db.engine)
    
    # Analyze performance data
    summary = performance_data.groupby('course_id').agg({'score': ['mean', 'max', 'min']})
    
    # Convert summary to HTML for display
    summary_html = summary.to_html()
    
    return render_template('performance_summary.html', summary=summary_html)

@app.route('/performance_plot')
def performance_plot():
    # Ensure the 'static' directory exists
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Fetch performance data from the database
    performance_data = pd.read_sql_query("SELECT * FROM performance", con=db.engine)
    performance_data['completion_date'] = pd.to_datetime(performance_data['completion_date'])
    
    # Create plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=performance_data, x='completion_date', y='score', hue='course_id')
    plt.title('Student Performance Over Time')
    plt.xlabel('Completion Date')
    plt.ylabel('Score')
    plt.legend(title='Course ID')
    
    # Save plot to file
    plot_path = 'static/performance_plot.png'
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free up memory
    
    # Check if the file was created successfully
    if not os.path.isfile(plot_path):
        return "Error: File not created", 500
    
    return send_file(plot_path, mimetype='image/png')