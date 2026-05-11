import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from pathlib import Path
import warnings
warnings.filterwarnings("ignore") # Hides annoying background warnings

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'algorithm_data.csv'

def train_and_test_ai():
    print("Loading your generated data...")
    # 1. Read the CSV you just made
    df = pd.read_csv(DATA_FILE)

    # 2. AI only understands numbers, not text. So we encode the words into numbers.
    problem_encoder = LabelEncoder()
    algo_encoder = LabelEncoder()

    df['Problem_Type_Num'] = problem_encoder.fit_transform(df['Problem_Type'])
    df['Target_Num'] = algo_encoder.fit_transform(df['Best_Algorithm'])

    # 3. Define our Inputs (X) and what we want to predict (y)
    X = df[['Problem_Type_Num', 'Input_Size']]
    y = df['Target_Num']

    # 4. Train the AI!
    print("Training the Machine Learning model...")
    model = DecisionTreeClassifier()
    model.fit(X, y)
    print("Training complete! 🧠\n")

    # --- 5. LET'S TEST IT OUT ---
    def predict_best_algo(problem_type, input_size):
        # Convert our text input into the number the AI learned
        prob_num = problem_encoder.transform([problem_type])[0]
        
        # Make the prediction
        prediction_num = model.predict([[prob_num, input_size]])[0]
        
        # Convert the predicted number back into the algorithm's name
        best_algo = algo_encoder.inverse_transform([prediction_num])[0]
        return best_algo

    # Run a test prediction!
    test_type = "Sorting"
    test_size = 750
    print(f"--- AI PREDICTION TEST ---")
    print(f"Scenario: We have a '{test_type}' problem with {test_size} items.")
    predicted_algo = predict_best_algo(test_type, test_size)
    print(f"The AI predicts the fastest algorithm to use is: ** {predicted_algo} **!")

if __name__ == "__main__":
    train_and_test_ai()