import joblib

def validate():
    model = joblib.load("models/xgboost_frozen.pkl")
    print(f"Model loaded: {type(model)}")
    print(f"n_features_in_: {getattr(model, 'n_features_in_', 'Not Found')}")
    print(f"classes: {list(model.classes_)}")
    
if __name__ == '__main__':
    validate()
