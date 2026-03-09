# IPL Win Probability Predictor

This project builds a machine learning model to estimate the probability of the chasing team winning an IPL match based on the current match situation.

The model uses match-state variables such as runs remaining, balls remaining, wickets remaining, and run rates to predict the likelihood of victory during the second innings.

---

## Dataset

The model is trained on IPL ball-by-ball match data obtained from Kaggle.

Dataset source:  
https://www.kaggle.com/datasets/ramjidoolla/ipl-data-set

The dataset contains two main files:

- matches.csv  
- deliveries.csv  

These datasets include information about teams, venues, runs scored, wickets, and ball-by-ball match progression.

---

## Feature Engineering

The following match-state features are used by the model:

- runs_left – runs required to win  
- balls_left – legal deliveries remaining  
- wickets_left – wickets remaining  
- current_run_rate  
- required_run_rate  

These features represent the current state of the match during a chase.

---

## Model

A Logistic Regression model is trained using a machine learning pipeline with:

- One-hot encoding for categorical variables (teams and venue)
- Numerical match-state features

The model predicts the probability of the batting team winning the match.

---

## Model Evaluation

The model was evaluated using a train-test split (80% training, 20% testing).

The Logistic Regression model achieved **approximately 81% accuracy** on the test dataset.

---

## Streamlit Application

The trained model is deployed using **Streamlit**, allowing users to interactively input match conditions and obtain win probability predictions.

Run the application using:

streamlit run app.py

---

## Win Probability Visualization

The project also includes a visualization showing how the predicted win probability evolves during a match. The model calculates probabilities for each ball of the second innings to illustrate how match momentum changes throughout the chase.

---

## Installation

Install the required dependencies using:

pip install -r requirements.txt

Libraries used:

- pandas  
- numpy  
- scikit-learn  
- matplotlib  
- streamlit  

---

## Limitations

The model uses match-state features and does not include player-level statistics, bowler performance, or match momentum factors. As a result, predictions in rare or extreme match situations may be less accurate.
