from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the machine learning model
with open('ipl_score.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Dictionary for teams
teams = {'Chennai Super Kings': 0, 'Delhi Daredevils': 1, 'Kings XI Punjab': 2, 
         'Kolkata Knight Riders': 3, 'Mumbai Indians': 4, 'Rajasthan Royals': 5, 
         'Royal Challengers Bangalore': 6, 'Sunrisers Hyderabad': 7}

@app.route('/home')
def home():
    return render_template('index.html', teams=teams)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        current_runs = float(request.form['current_runs'])
        current_wickets = float(request.form['current_wickets'])
        overs = float(request.form['overs'])
        runs_last_5overs = float(request.form['runs_last_5overs'])
        wickets_last_5overs = float(request.form['wickets_last_5overs'])

        if batting_team == bowling_team:
            return "Batting and Bowling team cannot be the same!"

        # Predicting the score
        prediction = model.predict([[teams[batting_team], teams[bowling_team], current_runs,
                                      current_wickets, overs, runs_last_5overs, wickets_last_5overs]])
        predicted_range = [int(prediction[0] - 50), int(prediction[0])]
        
        # Calculating required run rate
        required_run_rate = (predicted_range[1] - current_runs) / (20 - overs)
        
        return render_template('index.html', teams=teams, predicted_range=predicted_range, required_run_rate=required_run_rate)

if __name__ == '__main__':
    app.run(debug=True)
