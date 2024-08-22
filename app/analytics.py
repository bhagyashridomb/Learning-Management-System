from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route('/analyze_performance')
def analyze_performance():
    # Fetch data from database
    performance_data = pd.read_sql_query("SELECT * FROM performance", con=db.engine)
    
    # Perform analysis
    summary = performance_data.groupby('course_id').agg({'score': ['mean', 'max', 'min']})
    
    # Display or save the summary
    return summary.to_html()
