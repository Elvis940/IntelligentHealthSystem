import os
import sys
import django
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Add project root to sys.path (adjust as needed)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Step 2: Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_ai_viz.settings')
django.setup()

# Step 3: Import your Django models after setup
from symptom_checker.models import Disease


def train_and_save_model():
    diseases = Disease.objects.all()
    if not diseases:
        print("No diseases found in DB. Add some disease records first.")
        return

    disease_names = [d.name for d in diseases]
    symptoms_list = [d.symptoms for d in diseases]

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(symptoms_list)

    model_path = os.path.join(os.path.dirname(__file__), 'symptom_model.pkl')
    joblib.dump((vectorizer, vectors, disease_names), model_path)

    print(f"Model trained and saved to {model_path}")


def test_model(input_symptoms):
    model_path = os.path.join(os.path.dirname(__file__), 'symptom_model.pkl')
    if not os.path.exists(model_path):
        print("Model file not found. Run training first.")
        return

    vectorizer, vectors, disease_names = joblib.load(model_path)

    input_vec = vectorizer.transform([input_symptoms])
    similarities = cosine_similarity(input_vec, vectors)
    best_idx = similarities.argmax()
    best_score = similarities[0, best_idx]

    if best_score > 0.2:
        disease_name = disease_names[best_idx]
        print(f"Input Symptoms: {input_symptoms}")
        print(f"Predicted Disease: {disease_name} (Similarity: {best_score:.2f})")
    else:
        print("No matching disease found.")


if __name__ == '__main__':
    train_and_save_model()

    # Example test
    test_input = "fever, headache, cough"
    test_model(test_input)
