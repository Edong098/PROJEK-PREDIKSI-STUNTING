import pandas as pd
from utils.loader import load_metrics_data

def get_all_models_summary():
    """
    Mengembalikan DataFrame pandas yang merangkum metrik evaluasi semua model.
    """
    metrics = load_metrics_data()
    summary_list = []
    for name, data in metrics['models_evaluation'].items():
        summary_list.append({
            'Model': name,
            'Accuracy': data['accuracy'],
            'Precision': data['precision'],
            'Recall': data['recall'],
            'F1-Score (Macro)': data['f1_macro']
        })
    return pd.DataFrame(summary_list).sort_values(by='F1-Score (Macro)', ascending=False).reset_index(drop=True)

def get_model_evaluation(model_name):
    """
    Mengembalikan classification report dan confusion matrix untuk model tertentu.
    """
    metrics = load_metrics_data()
    return metrics['models_evaluation'].get(model_name, None)

def get_feature_importances():
    """
    Mengembalikan nilai feature importances dari model Random Forest dalam bentuk dictionary.
    """
    metrics = load_metrics_data()
    return metrics.get('feature_importances', {})

def get_classes():
    """
    Mengembalikan daftar kelas target klasifikasi.
    """
    metrics = load_metrics_data()
    return metrics.get('classes', ['normal', 'severely stunted', 'stunted', 'tinggi'])
