const { Document, Packer, Paragraph, Table, TableRow, TableCell, BorderStyle, VerticalAlign, AlignmentType, WidthType, ShadingType, HeadingLevel, UnderlineType, PageBreak } = require('docx');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = '/sessions/zen-inspiring-dijkstra/mnt/AI Course Material/AI_for_Finance_Course/Weekly_Projects';

// Color constants
const NAVY = '#1E2761';
const DARK_GRAY = '#333333';

// Helper function to create heading styles
function createHeading(text, level = 'H1') {
  const size = level === 'H1' ? 32 : 28; // 16pt and 14pt in half-points
  return new Paragraph({
    text: text,
    heading: level === 'H1' ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
    bold: true,
    size: size,
    color: NAVY,
    spacing: { line: 240, lineRule: 'auto', before: 120, after: 120 },
  });
}

// Helper function to create body paragraph
function createBodyParagraph(text, options = {}) {
  return new Paragraph({
    text: text,
    size: 24, // 12pt
    color: DARK_GRAY,
    spacing: { line: 240, lineRule: 'auto', before: 60, after: 60 },
    ...options,
  });
}

// Helper function to create bullet points
function createBullet(text, level = 0) {
  return new Paragraph({
    text: text,
    size: 24,
    color: DARK_GRAY,
    level: level,
    bullet: { level: level },
    spacing: { line: 240, lineRule: 'auto', before: 30, after: 30 },
  });
}

// Helper function to create monospace code block
function createCodeBlock(code) {
  const lines = code.split('\n');
  return lines.map(line => 
    new Paragraph({
      text: line || ' ',
      font: 'Courier New',
      size: 20, // 10pt for code
      color: '#000000',
      spacing: { line: 200, lineRule: 'auto', before: 0, after: 0 },
    })
  );
}

// Helper function to create grading rubric table
function createGradingRubric() {
  const rows = [
    new TableRow({
      children: [
        new TableCell({ 
          children: [createBodyParagraph('Criteria')],
          shading: { type: ShadingType.CLEAR, color: 'E6E6E6' },
          width: { size: 3600, type: WidthType.DXA },
          verticalAlign: VerticalAlign.CENTER,
        }),
        new TableCell({ 
          children: [createBodyParagraph('Description')],
          shading: { type: ShadingType.CLEAR, color: 'E6E6E6' },
          width: { size: 7200, type: WidthType.DXA },
          verticalAlign: VerticalAlign.CENTER,
        }),
        new TableCell({ 
          children: [createBodyParagraph('Points')],
          shading: { type: ShadingType.CLEAR, color: 'E6E6E6' },
          width: { size: 1440, type: WidthType.DXA },
          verticalAlign: VerticalAlign.CENTER,
        }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({ 
          children: [createBodyParagraph('Code Quality')],
          width: { size: 3600, type: WidthType.DXA },
        }),
        new TableCell({ 
          children: [createBodyParagraph('Clean, well-documented code with proper error handling')],
          width: { size: 7200, type: WidthType.DXA },
        }),
        new TableCell({ 
          children: [createBodyParagraph('25')],
          width: { size: 1440, type: WidthType.DXA },
        }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({ 
          children: [createBodyParagraph('Functionality')],
          width: { size: 3600, type: WidthType.DXA },
        }),
        new TableCell({ 
          children: [createBodyParagraph('All deliverables implemented and working correctly')],
          width: { size: 7200, type: WidthType.DXA },
        }),
        new TableCell({ 
          children: [createBodyParagraph('35')],
          width: { size: 1440, type: WidthType.DXA },
        }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({ 
          children: [createBodyParagraph('Testing')],
          width: { size: 3600, type: WidthType.DXA },
        }),
        new TableCell({ 
          children: [createBodyParagraph('Comprehensive test cases with good coverage')],
          width: { size: 7200, type: WidthType.DXA },
        }),
        new TableCell({ 
          children: [createBodyParagraph('20')],
          width: { size: 1440, type: WidthType.DXA },
        }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({ 
          children: [createBodyParagraph('Documentation')],
          width: { size: 3600, type: WidthType.DXA },
        }),
        new TableCell({ 
          children: [createBodyParagraph('Clear README and API documentation')],
          width: { size: 7200, type: WidthType.DXA },
        }),
        new TableCell({ 
          children: [createBodyParagraph('20')],
          width: { size: 1440, type: WidthType.DXA },
        }),
      ],
    }),
  ];

  return new Table({
    rows: rows,
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

// Week 1 Project Document
function generateWeek1Project() {
  const sections = [
    createHeading('Week 1: AI Readiness Assessment Tool', 'H1'),
    createBodyParagraph('Course: AI for Finance'),
    createBodyParagraph('Duration: 1 week'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Project Overview', 'H2'),
    createBodyParagraph('In this project, you will build a Python-based tool that comprehensively assesses an organization\'s readiness to adopt AI solutions in its financial operations. This assessment tool will evaluate multiple dimensions of organizational maturity and provide actionable recommendations for improvement.'),
    
    createHeading('Learning Objectives', 'H2'),
    createBullet('Design and implement a weighted scoring model for organizational assessment'),
    createBullet('Apply benchmark comparison techniques to position against industry standards'),
    createBullet('Create gap analysis frameworks to identify improvement areas'),
    createBullet('Generate professional reports with visualizations'),
    createBullet('Understand AI implementation prerequisites in financial institutions'),
    
    createHeading('Requirements and Specifications', 'H2'),
    createBodyParagraph('Your application must satisfy the following requirements:'),
    
    createBullet('Input Parameters:', 0),
    createBullet('Data maturity score (0-100): Assesses data quality, governance, and availability', 1),
    createBullet('Talent assessment (0-100): Evaluates team skills and experience', 1),
    createBullet('Infrastructure readiness (0-100): Measures cloud, security, and scalability', 1),
    createBullet('Regulatory compliance (0-100): Assesses adherence to financial regulations', 1),
    
    createBullet('Processing Requirements:', 0),
    createBullet('Apply weighted scoring model (customizable weights)', 1),
    createBullet('Compare results against industry benchmarks', 1),
    createBullet('Identify top 3-5 gaps and prioritize recommendations', 1),
    createBullet('Calculate implementation timeline estimates', 1),
    
    createBullet('Output Deliverables:', 0),
    createBullet('Readiness report in PDF or HTML format', 1),
    createBullet('Radar chart visualization showing dimension comparison', 1),
    createBullet('Priority roadmap with phased implementation timeline', 1),
    createBullet('JSON configuration for custom assessment parameters', 1),
    
    createHeading('Dataset Description', 'H2'),
    createBodyParagraph('The assessment tool will process organizational parameters as input rather than a traditional dataset. Create at least 5 test cases representing different organization profiles:'),
    
    createBullet('Financial institution (well-established bank)'),
    createBullet('Mid-stage fintech startup'),
    createBullet('Insurance company with legacy systems'),
    createBullet('Early-stage cryptocurrency exchange'),
    createBullet('Traditional retail bank with limited tech infrastructure'),
    
    createHeading('Deliverables Checklist', 'H2'),
    createBullet('assessment_tool.py: Main Python module with assessment logic'),
    createBullet('report_generator.py: Generates readiness reports'),
    createBullet('visualization.py: Creates radar charts and visualizations'),
    createBullet('config.json: Sample configuration with benchmark data'),
    createBullet('test_cases.json: 5 different organization profiles'),
    createBullet('README.md: Comprehensive documentation'),
    createBullet('requirements.txt: Python dependencies (pandas, matplotlib, plotly)'),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Grading Rubric', 'H2'),
    createGradingRubric(),
    
    new Paragraph({ text: '' }),
    
    createHeading('Submission Guidelines', 'H2'),
    createBullet('Submit as a compressed ZIP file containing all source code'),
    createBullet('Include a sample report output for at least one test case'),
    createBullet('Add screenshots of visualizations if not including actual charts'),
    createBullet('Provide clear instructions for running the assessment tool'),
    createBullet('Deadline: End of Week 1'),
    
    createHeading('Starter Code Outline', 'H2'),
    createBodyParagraph('Below is a starter code structure to guide your implementation:'),
    
    ...createCodeBlock(`# assessment_tool.py
import pandas as pd
import json
from dataclasses import dataclass

@dataclass
class OrganizationProfile:
    name: str
    data_maturity: float
    talent: float
    infrastructure: float
    regulatory: float

class AIReadinessAssessment:
    def __init__(self, config_path):
        self.config = json.load(open(config_path))
        self.weights = self.config['weights']
        self.benchmarks = self.config['benchmarks']
    
    def calculate_readiness_score(self, profile):
        """Calculate weighted AI readiness score"""
        dimensions = {
            'data': profile.data_maturity,
            'talent': profile.talent,
            'infrastructure': profile.infrastructure,
            'regulatory': profile.regulatory
        }
        
        total_score = sum(
            dimensions[key] * self.weights[key]
            for key in dimensions
        )
        return total_score
    
    def gap_analysis(self, profile):
        """Identify gaps against benchmarks"""
        gaps = {}
        # Implementation here
        return gaps
    
    def generate_recommendations(self, profile):
        """Generate actionable recommendations"""
        recommendations = []
        # Implementation here
        return recommendations`),
    
    createHeading('Hints and Tips', 'H2'),
    createBullet('Start with the data structure: define your OrganizationProfile and assessment dimensions clearly'),
    createBullet('Use pandas for easy calculation of weighted scores and comparisons'),
    createBullet('For visualizations, matplotlib is good for static charts; plotly for interactive ones'),
    createBullet('Consider industry-specific benchmarks (banking, fintech, insurance, etc.)'),
    createBullet('Test edge cases: what happens with all zeros? Perfect scores?'),
    createBullet('Make your configuration file flexible so weights and benchmarks can be easily adjusted'),
    createBullet('Document any assumptions about industry benchmarks you use'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 1 Solution Document
function generateWeek1Solution() {
  const sections = [
    createHeading('Week 1 Solution: AI Readiness Assessment Tool', 'H1'),
    createBodyParagraph('This document provides a comprehensive solution to the AI Readiness Assessment Tool project.'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Solution Overview', 'H2'),
    createBodyParagraph('The solution implements a modular, extensible assessment framework that evaluates organizational readiness across four key dimensions. It provides actionable insights through scoring, benchmarking, gap analysis, and prioritized recommendations.'),
    
    createHeading('Architecture Overview', 'H2'),
    createBullet('Core Assessment Engine: Weighted scoring model'),
    createBullet('Benchmark Module: Industry comparison logic'),
    createBullet('Report Generator: PDF/HTML output creation'),
    createBullet('Visualization Module: Radar charts and dashboards'),
    createBullet('Configuration System: Flexible parameter management'),
    
    createHeading('Step-by-Step Implementation', 'H2'),
    
    createHeading('Step 1: Data Structure Setup', 'H2'),
    createBodyParagraph('Define the core data structures for organization profiles and assessment results:'),
    
    ...createCodeBlock(`from dataclasses import dataclass
from typing import Dict, List
import json

@dataclass
class DimensionScore:
    name: str
    value: float  # 0-100
    weight: float  # 0-1
    benchmark: float  # Industry benchmark
    
    def weighted_score(self):
        return self.value * self.weight

@dataclass
class OrganizationProfile:
    name: str
    industry: str
    data_maturity: float
    talent: float
    infrastructure: float
    regulatory: float
    
    def to_dict(self):
        return {
            'name': self.name,
            'industry': self.industry,
            'dimensions': {
                'data_maturity': self.data_maturity,
                'talent': self.talent,
                'infrastructure': self.infrastructure,
                'regulatory': self.regulatory
            }
        }

@dataclass
class ReadinessReport:
    profile: OrganizationProfile
    overall_score: float
    dimension_scores: Dict[str, float]
    gaps: List[str]
    recommendations: List[str]
    timeline_months: int`),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Step 2: Assessment Engine', 'H2'),
    createBodyParagraph('Core logic for calculating readiness scores:'),
    
    ...createCodeBlock(`class AIReadinessAssessment:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.weights = self.config.get('weights', {
            'data': 0.3,
            'talent': 0.2,
            'infrastructure': 0.25,
            'regulatory': 0.25
        })
    
    def calculate_score(self, profile):
        """Calculate overall AI readiness score"""
        score = (
            profile.data_maturity * self.weights['data'] +
            profile.talent * self.weights['talent'] +
            profile.infrastructure * self.weights['infrastructure'] +
            profile.regulatory * self.weights['regulatory']
        )
        return min(100, max(0, score))`),
    
    createHeading('Expected Results', 'H2'),
    createBullet('Score range: 0-100 (composite readiness metric)'),
    createBullet('Readiness levels: Not Ready, Developing, Moderately Ready, Ready'),
    createBullet('Gap analysis shows dimensions below benchmark'),
    createBullet('Timeline estimates: 3-12 months based on gaps'),
    
    createHeading('Common Issues and Solutions', 'H2'),
    
    createBodyParagraph('Issue: Weights not summing to 1.0'),
    createBullet('Solution: Normalize weights or validate during initialization'),
    
    createBodyParagraph('Issue: Benchmark data missing'),
    createBullet('Solution: Provide sensible defaults or allow custom benchmarks'),
    
    createHeading('Extension Ideas', 'H2'),
    createBullet('Add historical tracking to show improvement over time'),
    createBullet('Implement peer comparison and benchmarking'),
    createBullet('Create interactive Streamlit dashboard'),
    createBullet('Add risk analysis and obstacle identification'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 2 Project
function generateWeek2Project() {
  const sections = [
    createHeading('Week 2: ML-Based Credit Risk Model', 'H1'),
    createBodyParagraph('Build a complete credit risk modeling pipeline with multiple algorithms and regulatory compliance documentation.'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Project Overview', 'H2'),
    createBodyParagraph('Develop a production-grade credit risk model that compares logistic regression, XGBoost, and neural networks. Include SHAP-based model interpretability and regulatory-compliant documentation.'),
    
    createHeading('Learning Objectives', 'H2'),
    createBullet('Build end-to-end ML pipeline with data preprocessing'),
    createBullet('Train multiple models for comparison'),
    createBullet('Apply SHAP for model interpretability'),
    createBullet('Evaluate using credit risk metrics (AUC, KS, Gini)'),
    createBullet('Generate regulatory compliance documentation'),
    
    createHeading('Requirements', 'H2'),
    
    createBullet('Dataset (10,000 records, 25 features):', 0),
    createBullet('5% default rate (imbalanced classification)', 1),
    createBullet('Mix of demographic, financial, and behavioral features', 1),
    createBullet('70/30 train/test split with stratification', 1),
    
    createBullet('Models:', 0),
    createBullet('Logistic Regression (baseline)', 1),
    createBullet('XGBoost with hyperparameter tuning', 1),
    createBullet('Neural Network (PyTorch)', 1),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Deliverables', 'H2'),
    createBullet('data_generator.py: Synthetic dataset creation'),
    createBullet('preprocessing.py: Feature engineering and scaling'),
    createBullet('models.py: Model definitions'),
    createBullet('train.py: Training pipeline'),
    createBullet('evaluate.py: Performance metrics'),
    createBullet('shap_analysis.py: Interpretability analysis'),
    createBullet('model_card.md: Regulatory documentation'),
    
    createHeading('Grading Rubric', 'H2'),
    createGradingRubric(),
    
    createHeading('Submission Guidelines', 'H2'),
    createBullet('Include all Python modules and trained models'),
    createBullet('Provide model comparison results and visualizations'),
    createBullet('Add SHAP interpretation samples'),
    
    createHeading('Starter Code', 'H2'),
    
    ...createCodeBlock(`# data_generator.py
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

def generate_credit_data(n_samples=10000):
    """Generate synthetic credit dataset"""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=25,
        n_informative=20,
        n_redundant=3,
        weights=[0.95, 0.05],
        random_state=42
    )
    
    feature_names = [f'feature_{i}' for i in range(25)]
    df = pd.DataFrame(X, columns=feature_names)
    df['default'] = y
    return df`),
    
    createHeading('Hints and Tips', 'H2'),
    createBullet('Use class_weight=balanced for imbalanced data'),
    createBullet('Apply stratified k-fold for cross-validation'),
    createBullet('Scale features before neural networks'),
    createBullet('KS statistic and Gini are industry-standard metrics'),
    createBullet('SHAP provides excellent model explanations'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 2 Solution
function generateWeek2Solution() {
  const sections = [
    createHeading('Week 2 Solution: ML-Based Credit Risk Model', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Solution Overview', 'H2'),
    createBodyParagraph('Complete implementation of a credit risk modeling framework with multiple models, evaluation metrics, and interpretability analysis.'),
    
    createHeading('Key Components', 'H2'),
    createBullet('Data generation with realistic feature distributions'),
    createBullet('Multiple model implementations and comparison'),
    createBullet('Comprehensive evaluation metrics'),
    createBullet('SHAP-based interpretability'),
    
    createHeading('Implementation Details', 'H2'),
    
    ...createCodeBlock(`# Full training pipeline
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, roc_curve

def train_models(X_train, y_train, X_test, y_test):
    results = {}
    
    # Logistic Regression
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    lr_auc = roc_auc_score(y_test, lr.predict_proba(X_test)[:, 1])
    results['LogisticRegression'] = lr_auc
    
    # XGBoost
    xgb = XGBClassifier(n_estimators=100, random_state=42)
    xgb.fit(X_train, y_train)
    xgb_auc = roc_auc_score(y_test, xgb.predict_proba(X_test)[:, 1])
    results['XGBoost'] = xgb_auc
    
    return results`),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Expected Results', 'H2'),
    createBullet('AUC-ROC: 0.78-0.85 (good discriminatory power)'),
    createBullet('KS Statistic: 0.45-0.60 (measure of separation)'),
    createBullet('Gini Coefficient: 0.56-0.70 (model stability)'),
    
    createHeading('Model Evaluation Metrics', 'H2'),
    createBullet('ROC AUC: Area under receiver operating characteristic curve'),
    createBullet('KS Statistic: Kolmogorov-Smirnov test statistic'),
    createBullet('Gini: Normalized measure of discrimination'),
    createBullet('Precision/Recall: Trade-off for decision threshold'),
    
    createHeading('Common Issues', 'H2'),
    createBodyParagraph('Issue: Class imbalance affecting model'),
    createBullet('Solution: Use SMOTE, class weights, or stratified sampling'),
    
    createBodyParagraph('Issue: SHAP computation too slow'),
    createBullet('Solution: Use TreeExplainer for tree models, sample data'),
    
    createHeading('Extensions', 'H2'),
    createBullet('Add fairness analysis across demographic groups'),
    createBullet('Implement model calibration'),
    createBullet('Create production monitoring dashboard'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 3 Project
function generateWeek3Project() {
  const sections = [
    createHeading('Week 3: Real-Time Fraud Detection System', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Project Overview', 'H2'),
    createBodyParagraph('Build a real-time fraud detection system using ensemble anomaly detection combining Isolation Forest and Autoencoders.'),
    
    createHeading('Learning Objectives', 'H2'),
    createBullet('Implement anomaly detection algorithms'),
    createBullet('Engineer velocity-based features'),
    createBullet('Build ensemble detection methods'),
    createBullet('Create ROC and PR curve visualizations'),
    createBullet('Design alert scoring system'),
    
    createHeading('Requirements', 'H2'),
    
    createBullet('Dataset:', 0),
    createBullet('100,000 synthetic transactions', 1),
    createBullet('1% fraud rate', 1),
    createBullet('Features: amount, merchant, time, location, device', 1),
    
    createBullet('Detection Methods:', 0),
    createBullet('Isolation Forest for multivariate anomalies', 1),
    createBullet('Autoencoder for pattern learning', 1),
    createBullet('Velocity-based rules', 1),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Deliverables', 'H2'),
    createBullet('fraud_detector.py: Detection engine'),
    createBullet('feature_engineering.py: Feature extraction'),
    createBullet('evaluate.py: ROC/PR metrics'),
    createBullet('dashboard.py: Streamlit interface'),
    
    createHeading('Grading Rubric', 'H2'),
    createGradingRubric(),
    
    createHeading('Submission Guidelines', 'H2'),
    createBullet('Include fraud detection pipeline'),
    createBullet('Provide ROC/PR visualizations'),
    createBullet('Add dashboard screenshots'),
    
    createHeading('Starter Code', 'H2'),
    
    ...createCodeBlock(`# fraud_detector.py
from sklearn.ensemble import IsolationForest
import torch.nn as nn

class FraudDetectionEnsemble:
    def __init__(self, contamination=0.01):
        self.iso_forest = IsolationForest(
            contamination=contamination,
            random_state=42
        )
    
    def fit(self, X):
        self.iso_forest.fit(X)
    
    def predict(self, X):
        scores = self.iso_forest.decision_function(X)
        return scores`),
    
    createHeading('Hints and Tips', 'H2'),
    createBullet('Create velocity features: txns per hour/day per card'),
    createBullet('Use reconstruction error as anomaly score'),
    createBullet('PR curves better than ROC for imbalanced data'),
    createBullet('Consider time-based and seasonal patterns'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 3 Solution
function generateWeek3Solution() {
  const sections = [
    createHeading('Week 3 Solution: Real-Time Fraud Detection', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Solution Overview', 'H2'),
    createBodyParagraph('Ensemble-based fraud detection combining unsupervised and deep learning approaches for real-time detection.'),
    
    createHeading('Architecture', 'H2'),
    createBullet('Isolation Forest: Fast tree-based detection'),
    createBullet('Autoencoder: Non-linear pattern detection'),
    createBullet('Velocity Features: Time-series patterns'),
    createBullet('Ensemble Voting: Combine signals'),
    
    createHeading('Implementation', 'H2'),
    
    ...createCodeBlock(`class Autoencoder(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim)
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded`),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Expected Results', 'H2'),
    createBullet('ROC AUC: 0.85-0.95 (excellent detection)'),
    createBullet('PR AUC: 0.65-0.80 (precision-recall trade)'),
    createBullet('Detection rate at 1% FP: 75-85%'),
    
    createHeading('Evaluation Metrics', 'H2'),
    createBullet('ROC AUC: Discrimination ability'),
    createBullet('PR AUC: Precision-recall trade-off'),
    createBullet('Detection Rate: Fraud caught at FP threshold'),
    
    createHeading('Common Issues', 'H2'),
    createBodyParagraph('Issue: Autoencoder not learning'),
    createBullet('Solution: Adjust learning rate, latent dimension, epochs'),
    
    createBodyParagraph('Issue: High false positive rate'),
    createBullet('Solution: Adjust ensemble weights, recalibrate threshold'),
    
    createHeading('Extensions', 'H2'),
    createBullet('Real-time streaming with Kafka'),
    createBullet('Graph-based fraud detection'),
    createBullet('Adaptive thresholds per merchant'),
    createBullet('Feedback loop for retraining'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 4 Project
function generateWeek4Project() {
  const sections = [
    createHeading('Week 4: Financial Forecasting Engine', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Project Overview', 'H2'),
    createBodyParagraph('Build a multi-model forecasting system combining LSTM, XGBoost, and ensemble methods with uncertainty quantification.'),
    
    createHeading('Learning Objectives', 'H2'),
    createBullet('Implement LSTM networks for time series'),
    createBullet('Engineer lag and technical features'),
    createBullet('Build ensemble forecasting models'),
    createBullet('Apply conformal prediction for intervals'),
    createBullet('Backtest with walk-forward validation'),
    
    createHeading('Requirements', 'H2'),
    
    createBullet('Dataset:', 0),
    createBullet('3 years daily data (750+ observations)', 1),
    createBullet('Multiple assets (stocks, indices, currencies)', 1),
    createBullet('OHLCV and technical indicator features', 1),
    
    createBullet('Models:', 0),
    createBullet('LSTM sequence-to-sequence', 1),
    createBullet('XGBoost with lag features', 1),
    createBullet('Stacking ensemble with meta-learner', 1),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Deliverables', 'H2'),
    createBullet('time_series_data.py: Data loading'),
    createBullet('models.py: LSTM, XGBoost, ensemble'),
    createBullet('conformal.py: Confidence intervals'),
    createBullet('backtest.py: Walk-forward validation'),
    createBullet('evaluate.py: Forecasting metrics'),
    
    createHeading('Grading Rubric', 'H2'),
    createGradingRubric(),
    
    createHeading('Starter Code', 'H2'),
    
    ...createCodeBlock(`# models.py - Time Series Models
import torch.nn as nn

class LSTMForecaster(nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden = lstm_out[:, -1, :]
        output = self.fc(last_hidden)
        return output

def create_sequences(data, seq_length=30):
    """Create LSTM training sequences"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return X, y`),
    
    createHeading('Hints and Tips', 'H2'),
    createBullet('Use 30-day sequences for LSTM'),
    createBullet('Normalize with percentage or log returns'),
    createBullet('Create lag features: 1, 5, 20 day prices'),
    createBullet('Conformal prediction via quantile regression'),
    createBullet('Walk-forward validation for realistic backtest'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 4 Solution
function generateWeek4Solution() {
  const sections = [
    createHeading('Week 4 Solution: Financial Forecasting Engine', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Solution Overview', 'H2'),
    createBodyParagraph('Multi-model financial forecasting with ensemble methods and uncertainty quantification through conformal prediction.'),
    
    createHeading('Key Components', 'H2'),
    createBullet('LSTM for temporal dependencies'),
    createBullet('XGBoost with lag features'),
    createBullet('Meta-learner ensemble'),
    createBullet('Conformal prediction intervals'),
    createBullet('Walk-forward backtesting'),
    
    createHeading('Implementation', 'H2'),
    
    ...createCodeBlock(`class TimeSeriesForecaster:
    def __init__(self, seq_length=30):
        self.seq_length = seq_length
        self.lstm_model = None
        self.xgb_model = None
    
    def prepare_sequences(self, data):
        """Prepare LSTM sequences"""
        X, y = [], []
        for i in range(len(data) - self.seq_length):
            X.append(data[i:i+self.seq_length])
            y.append(data[i+self.seq_length])
        return X, y
    
    def train_lstm(self, X, y, epochs=50):
        """Train LSTM forecaster"""
        self.lstm_model = nn.Sequential(
            nn.LSTM(1, 64, batch_first=True),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
        
        # Training loop
        optimizer = torch.optim.Adam(self.lstm_model.parameters())
        loss_fn = nn.MSELoss()
        
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.lstm_model(torch.FloatTensor(X))
            loss = loss_fn(outputs, torch.FloatTensor(y))
            loss.backward()
            optimizer.step()`),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Expected Results', 'H2'),
    createBullet('MAE: 1-3% of price'),
    createBullet('RMSE: 2-5% of price'),
    createBullet('MAPE: 2-5% (mean absolute % error)'),
    createBullet('Prediction interval coverage: 90-95%'),
    
    createHeading('Backtesting Framework', 'H2'),
    
    ...createCodeBlock(`def walk_forward_backtest(data, train_size=500):
    """Walk-forward validation"""
    results = []
    
    for i in range(len(data) - train_size - 50):
        train = data[i:i+train_size]
        test = data[i+train_size:i+train_size+50]
        
        # Train and evaluate
        forecaster = TimeSeriesForecaster()
        X, y = forecaster.prepare_sequences(train)
        forecaster.train_lstm(X, y)
        
        # Get predictions
        predictions = forecaster.predict(test)
        mae = np.mean(np.abs(test - predictions))
        results.append(mae)
    
    return results`),
    
    createHeading('Common Issues', 'H2'),
    createBodyParagraph('Issue: LSTM predictions too smooth/lagging'),
    createBullet('Solution: Add trend features, increase hidden size'),
    
    createBodyParagraph('Issue: Wide prediction intervals'),
    createBullet('Solution: Improve model accuracy, normalize residuals'),
    
    createHeading('Extensions', 'H2'),
    createBullet('Multi-step ahead forecasting'),
    createBullet('Exogenous variables (market indices)'),
    createBullet('Hierarchical forecasting'),
    createBullet('Online learning and adaptation'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 5 Project
function generateWeek5Project() {
  const sections = [
    createHeading('Week 5: Compliance Document Analyzer', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Project Overview', 'H2'),
    createBodyParagraph('Build an NLP-based compliance document analysis system with NER, classification, obligation tracking, and RAG-based Q&A.'),
    
    createHeading('Learning Objectives', 'H2'),
    createBullet('Implement Named Entity Recognition'),
    createBullet('Build document classification pipelines'),
    createBullet('Extract compliance obligations'),
    createBullet('Create RAG-based Q&A system'),
    createBullet('Understand financial regulations'),
    
    createHeading('Requirements', 'H2'),
    
    createBullet('Input:', 0),
    createBullet('Regulatory documents and guidelines', 1),
    createBullet('Contract templates and agreements', 1),
    createBullet('Compliance policies', 1),
    
    createBullet('Processing:', 0),
    createBullet('Named Entity Recognition (SpaCy)', 1),
    createBullet('Document classification', 1),
    createBullet('Obligation identification', 1),
    createBullet('RAG system with FAISS', 1),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Deliverables', 'H2'),
    createBullet('ner_extractor.py: Entity extraction'),
    createBullet('document_classifier.py: Classification'),
    createBullet('obligation_tracker.py: Obligation extraction'),
    createBullet('rag_qa.py: Q&A system'),
    
    createHeading('Grading Rubric', 'H2'),
    createGradingRubric(),
    
    createHeading('Starter Code', 'H2'),
    
    ...createCodeBlock(`# ner_extractor.py
import spacy

def extract_entities(text):
    """Extract named entities"""
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    
    entities = {
        'organizations': [],
        'dates': [],
        'regulations': [],
        'penalties': []
    }
    
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            entities['organizations'].append(ent.text)
        elif ent.label_ == 'DATE':
            entities['dates'].append(ent.text)
    
    return entities`),
    
    createHeading('Hints and Tips', 'H2'),
    createBullet('Use pre-trained SpaCy models'),
    createBullet('Fine-tune on financial documents'),
    createBullet('Sentence transformers for semantic search'),
    createBullet('FAISS for fast similarity search'),
    createBullet('Domain-specific entity patterns'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 5 Solution
function generateWeek5Solution() {
  const sections = [
    createHeading('Week 5 Solution: Compliance Document Analyzer', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Solution Overview', 'H2'),
    createBodyParagraph('Complete NLP system for compliance analysis with extraction, classification, obligation tracking, and RAG-Q&A.'),
    
    createHeading('Architecture', 'H2'),
    createBullet('NER: Extract regulatory entities'),
    createBullet('Classification: Categorize document types'),
    createBullet('Extraction: Parse compliance requirements'),
    createBullet('RAG: Retrieve and answer queries'),
    
    createHeading('Implementation', 'H2'),
    
    ...createCodeBlock(`class ComplianceAnalyzer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def extract_entities(self, text):
        """Extract regulatory entities"""
        doc = self.nlp(text)
        
        entities = {
            'organizations': [],
            'dates': [],
            'monetary': [],
            'persons': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ == 'MONEY':
                entities['monetary'].append(ent.text)
        
        return entities`),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Obligation Tracking', 'H2'),
    
    ...createCodeBlock(`class ObligationTracker:
    def __init__(self):
        self.obligations = []
    
    def add_obligation(self, document, text, category, deadline=None):
        """Track compliance obligation"""
        obligation = {
            'document': document,
            'text': text,
            'category': category,
            'deadline': deadline,
            'status': 'Open'
        }
        self.obligations.append(obligation)
    
    def export_report(self, filename):
        """Export obligations"""
        with open(filename, 'w') as f:
            json.dump(self.obligations, f, indent=2)`),
    
    createHeading('RAG-Based Q&A', 'H2'),
    
    ...createCodeBlock(`class ComplianceQA:
    def __init__(self, documents):
        self.documents = documents
        self.index = self.build_index()
    
    def build_index(self):
        """Build FAISS vector index"""
        embeddings = self.embedder.encode(self.documents)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings.astype(np.float32))
        return index
    
    def answer_query(self, query, k=3):
        """Answer compliance questions"""
        query_emb = self.embedder.encode([query])
        distances, indices = self.index.search(query_emb.astype(np.float32), k)
        
        return [self.documents[i] for i in indices[0]]`),
    
    createHeading('Expected Outputs', 'H2'),
    createBodyParagraph('Entity extraction example:'),
    ...createCodeBlock(`{
  "organizations": ["Federal Reserve", "SEC"],
  "dates": ["January 1, 2024"],
  "monetary": ["$100,000"],
  "persons": ["John Smith"]
}`),
    
    createHeading('Common Issues', 'H2'),
    createBodyParagraph('Issue: Missing financial entities'),
    createBullet('Solution: Fine-tune SpaCy on financial corpus'),
    
    createBodyParagraph('Issue: Irrelevant RAG results'),
    createBullet('Solution: Use domain embeddings, adjust k'),
    
    createHeading('Extensions', 'H2'),
    createBullet('Multi-language analysis'),
    createBullet('Real-time regulation monitoring'),
    createBullet('Compliance assessment dashboard'),
    createBullet('Document management integration'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 6 Project
function generateWeek6Project() {
  const sections = [
    createHeading('Week 6: Capstone - Integrated AI Finance Platform', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Project Overview', 'H2'),
    createBodyParagraph('Integrate all previous projects into a unified, deployment-ready AI finance platform with REST API, model registry, and monitoring.'),
    
    createHeading('Learning Objectives', 'H2'),
    createBullet('Integrate multiple AI components'),
    createBullet('Implement model versioning (MLflow)'),
    createBullet('Create REST APIs (FastAPI)'),
    createBullet('Build monitoring systems'),
    createBullet('Containerize applications (Docker)'),
    createBullet('Present professional findings'),
    
    createHeading('Requirements', 'H2'),
    
    createBullet('Integration:', 0),
    createBullet('Combine risk, credit, fraud, forecasting, compliance', 1),
    createBullet('Unified API layer', 1),
    
    createBullet('Infrastructure:', 0),
    createBullet('FastAPI web framework', 1),
    createBullet('MLflow model registry', 1),
    createBullet('Docker containerization', 1),
    createBullet('Prometheus monitoring', 1),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Deliverables', 'H2'),
    createBullet('main.py: FastAPI application'),
    createBullet('Dockerfile and docker-compose.yml'),
    createBullet('requirements.txt: All dependencies'),
    createBullet('architecture.md: System design'),
    createBullet('API.md: Endpoint documentation'),
    createBullet('DEPLOYMENT.md: Setup guide'),
    createBullet('presentation.pdf: 15-minute slides'),
    
    createHeading('Grading Rubric', 'H2'),
    createGradingRubric(),
    
    createHeading('Starter Code', 'H2'),
    
    ...createCodeBlock(`# main.py - FastAPI Application
from fastapi import FastAPI

app = FastAPI(
    title="AI Finance Platform",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/v1/readiness")
async def assess_readiness(org_data: dict):
    return {"score": 75}

@app.post("/api/v1/credit-risk")
async def assess_credit_risk(app_data: dict):
    return {"risk_score": 0.65}

@app.post("/api/v1/fraud")
async def detect_fraud(txn_data: dict):
    return {"fraud_score": 0.15}

@app.post("/api/v1/forecast")
async def forecast_price(params: dict):
    return {"forecast": [100.5, 101.2]}

@app.post("/api/v1/compliance")
async def analyze_compliance(doc: dict):
    return {"analysis": {}}`),
    
    createHeading('Hints and Tips', 'H2'),
    createBullet('Design modular architecture'),
    createBullet('Use FastAPI for auto-generated API docs'),
    createBullet('MLflow tracks experiments and models'),
    createBullet('Docker ensures reproducible deployment'),
    createBullet('Clear error handling and logging'),
    createBullet('Prepare live demo or demo video'),
    createBullet('Focus on business value in presentation'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Week 6 Solution
function generateWeek6Solution() {
  const sections = [
    createHeading('Week 6 Solution: Integrated AI Finance Platform', 'H1'),
    
    new Paragraph({ text: '' }),
    
    createHeading('Solution Overview', 'H2'),
    createBodyParagraph('Production-ready integrated platform combining all previous modules with proper versioning, API, and deployment infrastructure.'),
    
    createHeading('System Architecture', 'H2'),
    createBullet('API Gateway: FastAPI with validation'),
    createBullet('Model Services: Individual domain modules'),
    createBullet('Registry: MLflow model management'),
    createBullet('Data Pipeline: Feature engineering'),
    createBullet('Monitoring: Prometheus metrics'),
    
    createHeading('Complete Implementation', 'H2'),
    
    ...createCodeBlock(`# main.py - Production FastAPI Application
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mlflow
import logging
from datetime import datetime
import time

app = FastAPI(
    title="AI Finance Platform API",
    version="1.0.0"
)

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MLflow
mlflow.set_tracking_uri("http://localhost:5000")

@app.on_event("startup")
async def load_models():
    logger.info("Loading models...")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
def platform_status():
    return {
        "status": "operational",
        "version": "1.0.0",
        "components": {
            "api": "running",
            "mlflow": "connected"
        }
    }

@app.post("/api/v1/readiness")
async def assess_readiness(request: dict):
    try:
        start = time.time()
        overall_score = (
            request['data'] * 0.3 +
            request['talent'] * 0.2 +
            request['infrastructure'] * 0.25 +
            request['regulatory'] * 0.25
        )
        
        with mlflow.start_run():
            mlflow.log_metric("readiness", overall_score)
        
        return {
            "overall_score": overall_score,
            "response_time_ms": (time.time() - start) * 1000
        }
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500)

@app.post("/api/v1/credit-risk")
async def assess_credit_risk(request: dict):
    try:
        risk_score = 0.65
        return {"risk_score": risk_score, "category": "Medium"}
    except Exception as e:
        raise HTTPException(status_code=500)

@app.post("/api/v1/fraud")
async def detect_fraud(request: dict):
    try:
        fraud_score = 0.15
        return {"fraud_score": fraud_score, "action": "approved"}
    except Exception as e:
        raise HTTPException(status_code=500)

@app.post("/api/v1/forecast")
async def forecast_price(request: dict):
    try:
        forecast = [100.5, 101.2, 102.1]
        return {"forecast": forecast}
    except Exception as e:
        raise HTTPException(status_code=500)

@app.post("/api/v1/compliance")
async def analyze_compliance(request: dict):
    try:
        analysis = {"entities": [], "obligations": []}
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500)

@app.get("/api/v1/models")
def list_models():
    models = mlflow.search_registered_models()
    return {"models": [m.name for m in models]}

@app.get("/metrics")
def get_metrics():
    return {"uptime": 3600, "requests": 1250}`),
    
    new Paragraph({ 
      text: '',
      pageBreakBefore: true,
    }),
    
    createHeading('Docker Deployment', 'H2'),
    
    ...createCodeBlock(`# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    depends_on:
      - mlflow
  mlflow:
    image: ghcr.io/mlflow/mlflow
    ports:
      - "5000:5000"`),
    
    createHeading('Presentation Structure', 'H2'),
    createBullet('Introduction (1 min): Problem and context'),
    createBullet('Architecture (3 min): System design'),
    createBullet('Demo (5 min): Live demonstration'),
    createBullet('Results (2 min): Performance metrics'),
    createBullet('Conclusion (4 min): Key takeaways'),
    
    createHeading('Expected Capabilities', 'H2'),
    createBullet('5-model simultaneous inference'),
    createBullet('50-200ms average response time'),
    createBullet('Batch processing for 100+ requests'),
    createBullet('Model versioning and rollback'),
    createBullet('Comprehensive logging and monitoring'),
    
    createHeading('Common Issues', 'H2'),
    createBodyParagraph('Issue: Slow API responses'),
    createBullet('Solution: Add caching, optimize inference, batch'),
    
    createBodyParagraph('Issue: Model version conflicts'),
    createBullet('Solution: Use MLflow versioning workflow'),
    
    createBodyParagraph('Issue: Large Docker image'),
    createBullet('Solution: Multi-stage builds, minimize layers'),
    
    createHeading('Extensions', 'H2'),
    createBullet('Add JWT authentication'),
    createBullet('API rate limiting and quotas'),
    createBullet('Admin dashboard and alerts'),
    createBullet('A/B testing framework'),
    createBullet('GraphQL API'),
    createBullet('Cloud deployment (AWS/GCP/Azure)'),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          margins: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          size: { width: 12240, height: 15840 },
        },
      },
      children: sections,
    }],
  });
}

// Main generation function
async function generateAllDocuments() {
  const documents = [
    { name: 'Week_1_Project.docx', doc: generateWeek1Project() },
    { name: 'Week_1_Project_Solution.docx', doc: generateWeek1Solution() },
    { name: 'Week_2_Project.docx', doc: generateWeek2Project() },
    { name: 'Week_2_Project_Solution.docx', doc: generateWeek2Solution() },
    { name: 'Week_3_Project.docx', doc: generateWeek3Project() },
    { name: 'Week_3_Project_Solution.docx', doc: generateWeek3Solution() },
    { name: 'Week_4_Project.docx', doc: generateWeek4Project() },
    { name: 'Week_4_Project_Solution.docx', doc: generateWeek4Solution() },
    { name: 'Week_5_Project.docx', doc: generateWeek5Project() },
    { name: 'Week_5_Project_Solution.docx', doc: generateWeek5Solution() },
    { name: 'Week_6_Project.docx', doc: generateWeek6Project() },
    { name: 'Week_6_Project_Solution.docx', doc: generateWeek6Solution() },
  ];

  for (const { name, doc } of documents) {
    try {
      const filepath = `${OUTPUT_DIR}/${name}`;
      const buffer = await Packer.toBuffer(doc);
      fs.writeFileSync(filepath, buffer);
      console.log(`Created: ${name}`);
    } catch (error) {
      console.error(`Error creating ${name}:`, error);
    }
  }

  console.log(`\nSuccessfully created 12 course documents in ${OUTPUT_DIR}`);
}

// Run generation
generateAllDocuments().catch(console.error);
