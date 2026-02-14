#!/bin/bash

# Test CareerAI Backend API

BASE_URL="http://localhost:5001/api"
TOKEN=""

echo "=========================================="
echo "CareerAI Backend API Testing"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "[TEST 1] Health Check"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""

# Test 2: Register User
echo "[TEST 2] Register User"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "password": "securepass123"
  }')
echo "$REGISTER_RESPONSE" | python3 -m json.tool
TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('token', ''))")
echo "📌 Token: $TOKEN"
echo ""

# Test 3: Create Profile
echo "[TEST 3] Create Profile with Manual Input"
curl -s -X POST "$BASE_URL/profile/manual" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "education_level": "Bachelor'\''s",
    "branch": "Computer Science",
    "experience_years": 3,
    "preferred_domains": "AI, Machine Learning, Data Science"
  }' | python3 -m json.tool
echo ""

# Test 4: Add Skills
echo "[TEST 4] Add Multiple Skills"
for skill in "Python:expert:5" "Machine Learning:intermediate:2" "SQL:intermediate:3" "Statistics:intermediate:2" "TensorFlow:beginner:1"; do
  IFS=':' read -r skill_name level years <<< "$skill"
  echo "Adding skill: $skill_name ($level)"
  curl -s -X POST "$BASE_URL/profile/skills" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "skill_name": "'"$skill_name"'",
      "skill_level": "'"$level"'",
      "years_experience": '$years'
    }' > /dev/null
done
echo "✓ Skills added"
echo ""

# Test 5: Get User Skills
echo "[TEST 5] Get All User Skills"
curl -s -X GET "$BASE_URL/profile/skills" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

# Test 6: Get Recommendations
echo "[TEST 6] Get Career Recommendations"
RECS=$(curl -s -X GET "$BASE_URL/recommendations?limit=5" \
  -H "Authorization: Bearer $TOKEN")
echo "$RECS" | python3 -m json.tool
echo ""

# Test 7: Get Detailed Recommendation
echo "[TEST 7] Get Detailed Recommendation (Job ID 1: ML Engineer)"
DETAIL=$(curl -s -X GET "$BASE_URL/recommendations/1" \
  -H "Authorization: Bearer $TOKEN")
echo "$DETAIL" | python3 -m json.tool | head -60
echo "... (truncated)"
echo ""

# Test 8: Get XAI Explanation
echo "[TEST 8] Get XAI Explanation for Job"
curl -s -X GET "$BASE_URL/recommendations/1/explain" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

# Test 9: Get Learning Roadmap
echo "[TEST 9] Get Career Roadmap"
curl -s -X GET "$BASE_URL/recommendations/1/roadmap" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

# Test 10: Dashboard Summary
echo "[TEST 10] Dashboard Summary"
curl -s -X GET "$BASE_URL/dashboard/summary" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "=========================================="
echo "✓ All tests completed!"
echo "=========================================="
