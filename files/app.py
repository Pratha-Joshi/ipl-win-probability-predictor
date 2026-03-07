import streamlit as st
import pickle
import pandas as pd

# -----------------------------
# LOAD MODEL
# -----------------------------
pipe = pickle.load(open('pipe.pkl', 'rb'))

# -----------------------------
# CONSTANTS
# -----------------------------
teams = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Kings XI Punjab',
    'Kolkata Knight Riders',
    'Mumbai Indians',
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad'
]

venues = [
    'M Chinnaswamy Stadium',
    'Eden Gardens',
    'Feroz Shah Kotla',
    'Wankhede Stadium',
    'Rajiv Gandhi International Stadium',
    'MA Chidambaram Stadium'
]

# -----------------------------
# APP TITLE
# -----------------------------
st.title(" IPL Win Probability Predictor")

st.write(
    "Enter the current match situation for the chasing team "
    "to estimate their probability of winning."
)

# -----------------------------
# USER INPUT
# -----------------------------
batting_team = st.selectbox("Batting Team", teams)
bowling_team = st.selectbox("Bowling Team", teams)

venue = st.selectbox("Venue", venues)

runs_left = st.slider("Runs Left", 0, 250)
balls_left = st.slider("Legal Balls Remaining", 0, 120)
wickets_left = st.slider("Wickets Left", 0, 10)
total_runs = st.slider("Current Score", 0, 300)

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("Predict Win Probability"):

    # -----------------------------
    # EDGE CASE VALIDATION
    # -----------------------------
    if batting_team == bowling_team:
        st.error("Batting and bowling teams cannot be the same.")

    elif balls_left == 0 and runs_left > 0:
        st.error("No legal balls remaining. Match result already determined.")

    elif runs_left == 0:
        st.success("Target already achieved! Batting team wins.")

    elif wickets_left == 0 and runs_left > 0:
        st.error("All wickets lost. Batting team cannot win.")

    elif runs_left > balls_left * 6:
        st.error("Required runs exceed the maximum possible runs from remaining balls.")

    elif runs_left > balls_left * 4:
        st.warning(
            "This is an extremely difficult chase scenario. "
            "Model predictions may be unreliable."
        )

    elif balls_left > 120 or balls_left < 0:
        st.error("Legal balls remaining must be between 0 and 120.")

    elif wickets_left > 10 or wickets_left < 0:
        st.error("Wickets left must be between 0 and 10.")

    elif runs_left < 0:
        st.error("Runs left cannot be negative.")

    elif balls_left == 120 and total_runs > 0:
        st.error("Score cannot exist before the innings begins.")

    else:

        # -----------------------------
        # FEATURE ENGINEERING
        # -----------------------------
        overs_completed = (120 - balls_left) / 6

        if overs_completed == 0:
            current_run_rate = 0
        else:
            current_run_rate = total_runs / overs_completed

        required_run_rate = runs_left / (balls_left / 6)

        # -----------------------------
        # PREPARE MODEL INPUT
        # -----------------------------
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'venue': [venue],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'total_runs': [total_runs],
            'current_run_rate': [current_run_rate],
            'required_run_rate': [required_run_rate]
        })

        # -----------------------------
        # MODEL PREDICTION
        # -----------------------------
        result = pipe.predict_proba(input_df)

        loss_prob = result[0][0]
        win_prob = result[0][1]

        # -----------------------------
        # DISPLAY RESULT
        # -----------------------------
        st.subheader("Prediction")

        st.success(f" Winning Probability: {round(win_prob * 100)}%")
        st.warning(f" Losing Probability: {round(loss_prob * 100)}%")