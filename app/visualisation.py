from flask import Flask, send_file
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

app = Flask(__name__)

@app.route('/performance_plot')
def performance_plot():
    performance_data = pd.read_sql_query("SELECT * FROM performance", con=db.engine)
    performance_data['completion_date'] = pd.to_datetime(performance_data['completion_date'])
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=performance_data, x='completion_date', y='score', hue='course_id')
    plt.title('Student Performance Over Time')
    plt.xlabel('Completion Date')
    plt.ylabel('Score')
    plt.legend(title='Course ID')
    
    # Save plot to file
    plt.savefig('static/performance_plot.png')
    return send_file('static/performance_plot.png', mimetype='image/png')
