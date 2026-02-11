#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

print("=" * 60)
print("Testing Cognitive Career Recommender Imports")
print("=" * 60)

# Test 1: Simple App
print("\n[1/5] Testing simple_app...")
try:
    import simple_app
    print("✅ simple_app.py imports successfully")
except Exception as e:
    print(f"❌ simple_app.py failed: {e}")

# Test 2: AI Engine
print("\n[2/5] Testing AI engine...")
try:
    from ai_engine.cognitive_engine import CognitiveRecommendationEngine
    print("✅ CognitiveRecommendationEngine imports successfully")
except Exception as e:
    print(f"❌ AI engine failed: {e}")

# Test 3: NLP Processor
print("\n[3/5] Testing NLP processor...")
try:
    from nlp_processor.resume_analyzer import ResumeAnalyzer
    print("✅ ResumeAnalyzer imports successfully")
except Exception as e:
    print(f"❌ NLP processor failed: {e}")

# Test 4: Data Processor
print("\n[4/5] Testing data processor...")
try:
    from utils.data_processor import DataProcessor
    print("✅ DataProcessor imports successfully")
except Exception as e:
    print(f"❌ Data processor failed: {e}")

# Test 5: Main App
print("\n[5/5] Testing main app...")
try:
    import app
    print("✅ app.py imports successfully")
except Exception as e:
    print(f"❌ Main app failed: {e}")

print("\n" + "=" * 60)
print("All Tests Complete!")
print("=" * 60)
