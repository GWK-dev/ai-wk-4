# practical_implementation/breast_cancer_analysis.py
"""
Predictive Analytics for Resource Allocation
Breast Cancer Dataset Analysis for Issue Priority Prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer

class ResourceAllocationPredictor:
    """
    Predictive model for issue priority allocation using breast cancer dataset
    Adapted for software engineering resource allocation context
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.results = {}
    
    def load_and_preprocess_data(self):
        """Load and preprocess the breast cancer dataset"""
        print("📊 Loading and Preprocessing Data...")
        
        # Load dataset
        cancer_data = load_breast_cancer()
        df = pd.DataFrame(cancer_data.data, columns=cancer_data.feature_names)
        df['target'] = cancer_data.target
        
        # Adapt for software engineering context
        # Map medical features to software metrics analogy
        feature_mapping = {
            'mean radius': 'code_complexity',
            'mean texture': 'code_quality', 
            'mean perimeter': 'module_size',
            'mean area': 'test_coverage',
            'mean smoothness': 'code_maintainability',
            'mean compactness': 'performance_metrics',
            'mean concavity': 'security_risks',
            'mean concave points': 'bug_density',
            'mean symmetry': 'architecture_quality',
            'mean fractal dimension': 'documentation_quality'
        }
        
        # Select key features for our adapted context
        selected_features = list(feature_mapping.keys())[:8]  # Use first 8 features
        df = df[selected_features + ['target']]
        df = df.rename(columns=feature_mapping)
        
        # Convert target to priority levels (High, Medium, Low)
        # Malignant (1) -> High priority, Benign (0) -> Medium/Low priority
        def map_to_priority(target):
            if target == 1:  # Malignant - critical issues
                return 'High'
            else:  # Benign - normal issues
                return np.random.choice(['Medium', 'Low'], p=[0.6, 0.4])
        
        df['priority'] = df['target'].apply(map_to_priority)
        df = df.drop('target', axis=1)
        
        print(f"Dataset shape: {df.shape}")
        print(f"Priority distribution:\n{df['priority'].value_counts()}")
        
        return df
    
    def prepare_features(self, df):
        """Prepare features for model training"""
        # Encode target variable
        y = self.label_encoder.fit_transform(df['priority'])
        
        # Select features
        X = df.drop('priority', axis=1)
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y, X.columns
    
    def train_model(self, X_train, y_train):
        """Train the Random Forest model"""
        print("🤖 Training Random Forest Model...")
        self.model.fit(X_train, y_train)
        print("✅ Model training completed!")
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        print("📈 Evaluating Model Performance...")
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # Store results
        self.results = {
            'accuracy': accuracy,
            'f1_score': f1,
            'predictions': y_pred,
            'true_labels': y_test,
            'feature_importance': self.model.feature_importances_
        }
        
        print(f"🎯 Accuracy: {accuracy:.4f}")
        print(f"📊 F1-Score: {f1:.4f}")
        print("\n📋 Classification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=self.label_encoder.classes_))
        
        return accuracy, f1
    
    def visualize_results(self, feature_names):
        """Create visualizations of model performance"""
        print("🎨 Generating Visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Confusion Matrix
        cm = confusion_matrix(self.results['true_labels'], self.results['predictions'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=self.label_encoder.classes_,
                   yticklabels=self.label_encoder.classes_, ax=axes[0, 0])
        axes[0, 0].set_title('Confusion Matrix')
        axes[0, 0].set_xlabel('Predicted')
        axes[0, 0].set_ylabel('Actual')
        
        # 2. Feature Importance
        feature_imp = pd.DataFrame({
            'feature': feature_names,
            'importance': self.results['feature_importance']
        }).sort_values('importance', ascending=True)
        
        axes[0, 1].barh(feature_imp['feature'], feature_imp['importance'])
        axes[0, 1].set_title('Feature Importance')
        axes[0, 1].set_xlabel('Importance Score')
        
        # 3. Performance Metrics
        metrics = ['Accuracy', 'F1-Score']
        values = [self.results['accuracy'], self.results['f1_score']]
        bars = axes[1, 0].bar(metrics, values, color=['skyblue', 'lightcoral'])
        axes[1, 0].set_title('Model Performance Metrics')
        axes[1, 0].set_ylabel('Score')
        axes[1, 0].set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{value:.3f}', ha='center', va='bottom')
        
        # 4. Priority Distribution
        priority_counts = pd.Series(self.results['true_labels']).value_counts()
        axes[1, 1].pie(priority_counts.values, labels=self.label_encoder.classes_,
                      autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('Priority Distribution in Test Set')
        
        plt.tight_layout()
        plt.savefig('resource_allocation_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def run_complete_analysis(self):
        """Run the complete predictive analytics pipeline"""
        # Load and preprocess data
        df = self.load_and_preprocess_data()
        
        # Prepare features
        X, y, feature_names = self.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.train_model(X_train, y_train)
        
        # Evaluate model
        accuracy, f1 = self.evaluate_model(X_test, y_test)
        
        # Visualize results
        self.visualize_results(feature_names)
        
        return accuracy, f1

def main():
    """Main execution function"""
    print("🔮 Predictive Analytics for Resource Allocation")
    print("=" * 50)
    
    predictor = ResourceAllocationPredictor()
    accuracy, f1 = predictor.run_complete_analysis()
    
    print("\n" + "="*50)
    print("🎉 PREDICTIVE ANALYTICS PIPELINE COMPLETED!")
    print("="*50)
    print(f"Final Performance Metrics:")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  F1-Score: {f1:.4f}")
    print(f"  Model: Random Forest Classifier")
    print(f"  Application: Software Issue Priority Prediction")

if __name__ == "__main__":
    main()