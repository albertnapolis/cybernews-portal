#!/usr/bin/env python
"""
Simple script to test if the API is working
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing Cybersecurity News Portal API...")
    print("=" * 50)

    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("[OK] Root endpoint is working")
            print(f"  Response: {response.json()}")
        else:
            print(f"[FAIL] Root endpoint failed with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[FAIL] Cannot connect to the server. Make sure it's running on port 8000")
        return

    # Test health endpoint
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("[OK] Health endpoint is working")
    else:
        print(f"[FAIL] Health endpoint failed with status {response.status_code}")

    # Test news endpoint
    response = requests.get(f"{BASE_URL}/api/v1/news")
    if response.status_code == 200:
        data = response.json()
        print("[OK] News endpoint is working")
        print(f"  Total articles: {data.get('total', 0)}")
        print(f"  Current page: {data.get('page', 1)}")
    else:
        print(f"[FAIL] News endpoint failed with status {response.status_code}")

    # Test categories endpoint
    response = requests.get(f"{BASE_URL}/api/v1/categories")
    if response.status_code == 200:
        categories = response.json()
        print("[OK] Categories endpoint is working")
        print(f"  Total categories: {len(categories)}")
        if categories:
            print(f"  Categories: {', '.join([c['name'] for c in categories[:5]])}")
    else:
        print(f"[FAIL] Categories endpoint failed with status {response.status_code}")

    # Test sources endpoint
    response = requests.get(f"{BASE_URL}/api/v1/sources")
    if response.status_code == 200:
        sources = response.json()
        print("[OK] Sources endpoint is working")
        print(f"  Total sources: {len(sources)}")
        if sources:
            print(f"  Sources: {', '.join([s['name'] for s in sources[:3]])}")
    else:
        print(f"[FAIL] Sources endpoint failed with status {response.status_code}")

    print("=" * 50)
    print("API test completed!")
    print("\nNext steps:")
    print("1. Run 'POST /api/v1/news/refresh' to fetch news from RSS feeds")
    print("2. Start the frontend with 'npm run dev' in the frontend directory")

if __name__ == "__main__":
    test_api()