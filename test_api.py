#!/usr/bin/env python3
"""
Test script for Bank Churn Prediction API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_single_prediction():
    """Test single prediction"""
    print("\n🔍 Testing single prediction...")

    # Test data for a low-risk customer
    test_data = {
        "CreditScore": 650,
        "Age": 35,
        "Tenure": 5,
        "Balance": 50000,
        "NumOfProducts": 2,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 75000,
        "Geography_Germany": 0,
        "Geography_Spain": 1
    }

    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction result: {result}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction"""
    print("\n🔍 Testing batch prediction...")

    batch_data = [
        {
            "CreditScore": 650, "Age": 35, "Tenure": 5, "Balance": 50000,
            "NumOfProducts": 2, "HasCrCard": 1, "IsActiveMember": 1,
            "EstimatedSalary": 75000, "Geography_Germany": 0, "Geography_Spain": 1
        },
        {
            "CreditScore": 400, "Age": 60, "Tenure": 1, "Balance": 150000,
            "NumOfProducts": 1, "HasCrCard": 0, "IsActiveMember": 0,
            "EstimatedSalary": 20000, "Geography_Germany": 1, "Geography_Spain": 0
        }
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            json=batch_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch prediction result: {result}")
            return True
        else:
            print(f"❌ Batch prediction failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Batch prediction error: {e}")
        return False

def test_stats():
    """Test stats endpoint"""
    print("\n🔍 Testing stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Stats: {data}")
            return True
        else:
            print(f"❌ Stats check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stats check error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Bank Churn API Tests")
    print("=" * 50)

    # Wait a bit for the API to be ready
    print("⏳ Waiting for API to be ready...")
    time.sleep(2)

    tests = [
        test_health,
        test_single_prediction,
        test_batch_prediction,
        test_stats
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API logs.")

if __name__ == "__main__":
    main()