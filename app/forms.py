# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class AddStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    learning_style = StringField('Learning Style', validators=[DataRequired()])
    current_level = StringField('Current Level', validators=[DataRequired()])
    progress = FloatField('Progress', validators=[DataRequired()])
    submit = SubmitField('Add Student')

class AddCourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    difficulty= SelectField('Difficulty Level', choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], validators=[DataRequired()])
    prerequisite_cid = IntegerField('Prerequisite Course ID',validators=[Optional()])
    submit = SubmitField('Add Course')

class AddMaterialForm(FlaskForm):
    material_type = SelectField('Material Type', choices=[('Video', 'Video'), ('Article', 'Article'), ('Quiz', 'Quiz')], validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    difficulty = SelectField('Difficulty Level', choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], validators=[DataRequired()])
    submit = SubmitField('Add Material')

class PerformanceForm(FlaskForm):
    stud_id = IntegerField('Student ID', validators=[DataRequired()])
    course_id = IntegerField('Course ID', validators=[DataRequired()])
    score = FloatField('Score', validators=[DataRequired()])
    completion_date = StringField('Completion Date (YYYY-MM-DD)', validators=[DataRequired()])
    feedback = TextAreaField('Feedback')
    submit = SubmitField('Record Performance')

class RecommendationForm(FlaskForm):
    stud_id = IntegerField('Student ID', validators=[DataRequired()])
    course_id = IntegerField('Course ID', validators=[DataRequired()])
    recommended_material_id = IntegerField('Recommended Material ID', validators=[DataRequired()])
    reason_for_recommendation = TextAreaField('Reason for Recommendation', validators=[DataRequired()])
    submit = SubmitField('Add Recommendation')
