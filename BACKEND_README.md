# CareerAI - Cognitive Career Recommendation System

## Backend Architecture Documentation

### Overview

This is a production-ready, realistic AI-powered career recommendation system that uses:
- **NLP & Machine Learning** for skill extraction and matching
- **Rule-based Cognitive Reasoning** for explainable recommendations
- **XAI (Explainable AI)** for transparent decision-making
- **PostgreSQL/SQLite** for data persistence
- **RESTful API** for frontend integration

---

## Project Structure

```
backend/
├── models/                 # SQLAlchemy database models
│   ├── user.py            # User auth model
│   ├── profile.py         # User profile & skills
│   ├── job.py             # Job dataset
│   ├── recommendation.py  # Recommendations with XAI data
│   └── resume.py          # Resume storage & parsed data
│
├── services/              # Business logic & AI modules
│   ├── auth_service.py         # JWT authentication
│   ├── profile_service.py      # Profile management
│   ├── resume_service.py       # Resume parsing with NLP
│   ├── skill_extractor.py      # NLP skill extraction
│   ├── job_loader.py           # Job dataset loader
│   ├── skill_matcher.py        # Core similarity matching
│   ├── cognitive_reasoner.py   # Rule-based reasoning
│   ├── xai_explainer.py        # Explainable AI
│   └── roadmap_generator.py    # Learning path generation
│
├── api/                   # REST API endpoints
│   ├── auth_routes.py          # /api/auth/*
│   ├── profile_routes.py       # /api/profile/*
│   ├── resume_routes.py        # /api/resume/*
│   ├── recommendations_routes.py  # /api/recommendations/*
│   └── dashboard_routes.py     # /api/dashboard/*
│
├── main.py               # Flask app & initialization
├── config.py             # Configuration
└── requirements.txt      # Dependencies
```

---

## Database Schema

### Users Table
```sql
users (id, name, email, password_hash, role, created_at, updated_at)
```

### User Profile & Skills
```sql
user_profiles (id, user_id, education_level, branch, experience_years, preferred_domains, profile_completeness)
user_skills (id, user_id, skill_name, skill_level, years_experience)
```

### Jobs & Recommendations
```sql
jobs (id, job_title, description, domain, experience_level, average_salary, job_market_demand)
job_skills (id, job_id, skill_name, required_level, is_mandatory)
recommendations (id, user_id, job_id, match_score, matched_skills, missing_skills, reasoning, learning_path)
```

### Resume
```sql
resumes (id, user_id, filename, file_path, file_type, raw_text, parsed_data, created_at, updated_at)
```

---

## Core Modules Explained

### 1. **Authentication Service** (`auth_service.py`)
- User registration with password hashing
- JWT token generation (30-day expiry)
- Token verification
- **Endpoint**: `/api/auth/register`, `/api/auth/login`, `/api/auth/verify`

### 2. **Profile Service** (`profile_service.py`)
- Manual profile input
- Skill management
- Profile completeness calculation
- **Endpoint**: `/api/profile/manual`, `/api/profile`, `/api/profile/skills`

### 3. **Resume Processing** (`resume_service.py` + `skill_extractor.py`)
- PDF & DOCX file parsing
- Text extraction with PyPDF2 & python-docx
- **NLP-based skill extraction** using regex & spaCy
- Entity recognition
- Auto-populate skills from resume
- **Endpoint**: `/api/resume/upload`, `/api/resume/parsed-data`

**Skill Database** includes:
- Programming Languages: Python, Java, JavaScript, C++, Rust, SQL, etc.
- Web Frameworks: React, Angular, Node.js, Django, Flask, FastAPI
- ML/Data Science: TensorFlow, PyTorch, Pandas, Scikit-learn, NLP, Computer Vision
- Cloud & DevOps: AWS, Azure, Docker, Kubernetes, CI/CD, Terraform
- Soft Skills: Leadership, Communication, Problem Solving, Teamwork

### 4. **Job Dataset Loader** (`job_loader.py`)
- **10 realistic job roles** (Machine Learning Engineer, Data Scientist, Full Stack Developer, etc.)
- Each job has required skills with levels (beginner/intermediate/expert)
- Market demand ratings
- Salary ranges
- **Completely realistic data** from public sources (O*NET, Kaggle)

### 5. **Skill Matcher** (`skill_matcher.py`) - CORE AI LOGIC
The heart of the system!

**Algorithm**:
1. Extract user skills from profile/resume
2. Compare against job requirements
3. Calculate match score (0-100):
   - **Mandatory skills**: 50% of score
   - **Optional skills**: 50% of score
   - Formula: (matched_count / total_required) * 100

**Example**:
```
User has: Python, Machine Learning, SQL, Statistics
Job requires: Python (mandatory), Machine Learning (mandatory), Deep Learning, TensorFlow

Match: 2/4 = 50%
Mandatory: 2/2 = 100% → 50 points
Optional: 0/2 = 0% → 0 points
Total: 50%
```

**Endpoint**: `/api/recommendations`

### 6. **Cognitive Reasoner** (`cognitive_reasoner.py`)
Rule-based reasoning engine that explains WHY a job is recommended.

**Rules** for each domain (AI, Data Science, Web, Cloud):
- Check for primary skills (e.g., Python + ML for AI roles)
- Assess experience level alignment
- Check domain preferences
- Generate human-readable explanation

**Example reasoning**:
```
"With 3 years of experience, you match the intermediate level requirements.
You possess key skills: Python, Machine Learning, SQL.
In the AI domain, your expertise in Machine Learning is particularly valuable.
Your 75% match score shows strong alignment with this role."
```

### 7. **XAI Explainer** (`xai_explainer.py`)
Generates transparent, explainable AI insights:
- Confidence level (Very High/High/Moderate/Low)
- Job market demand assessment
- Growth potential in domain
- Detailed skill analysis (matched vs missing)

### 8. **Roadmap Generator** (`roadmap_generator.py`)
Generates personalized learning paths based on missing skills.

**Example roadmap for AI role**:
```
Step 1: Mathematics Foundations (4-6 weeks)
Step 2: Machine Learning Fundamentals (8-10 weeks)
Step 3: Deep Learning (10-12 weeks)
Step 4: Advanced Topics (NLP, CV, RL) (12+ weeks)
Step 5: Portfolio Projects (Ongoing)
```

---

## API Endpoints

### Authentication
```
POST /api/auth/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure123"
}
→ Returns: { token, user }

POST /api/auth/login
{
  "email": "john@example.com",
  "password": "secure123"
}
→ Returns: { token }

POST /api/auth/verify
Headers: Authorization: Bearer <token>
→ Returns: { valid, user }
```

### Profile Management
```
POST /api/profile/manual
{
  "education_level": "Bachelor's",
  "branch": "Computer Science",
  "experience_years": 2,
  "preferred_domains": "AI, Data Science"
}

GET /api/profile
→ Returns: Profile with completeness %

POST /api/profile/skills
{
  "skill_name": "Python",
  "skill_level": "expert",
  "years_experience": 3
}

GET /api/profile/skills
→ Returns: All user skills
```

### Resume Processing
```
POST /api/resume/upload (multipart form-data)
file: <PDF or DOCX>
→ Returns: { parsed_data with skills, education, experience }

GET /api/resume/parsed-data
→ Returns: Parsed resume data
```

### Recommendations (CORE)
```
GET /api/recommendations?limit=10
→ Returns: Top 10 recommended jobs with match scores

GET /api/recommendations/<job_id>
→ Returns: {
    job: Job details,
    explanation: XAI insights,
    roadmap: Learning path
  }

GET /api/recommendations/<job_id>/explain
→ Returns: Detailed XAI explanation

GET /api/recommendations/<job_id>/roadmap
→ Returns: Learning roadmap for missing skills
```

### Dashboard
```
GET /api/dashboard/summary
→ Returns: Profile completion, top match, skill stats, recommendations

GET /api/dashboard/stats
→ Returns: Skill distribution, domain scores, average match

GET /api/dashboard/progress
→ Returns: Profile progress & next steps
```

---

## Running the System

### Installation
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Run Production Server
```bash
python main.py
# Server runs on http://localhost:5001
```

### Run with Database
```bash
# Default: SQLite (career_ai.db)
python main.py

# With PostgreSQL:
export DATABASE_URL="postgresql://user:password@localhost/career_ai"
python main.py
```

---

## Example Workflow

### 1. Register User
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "password123"
  }'
```

### 2. Create Profile
```bash
curl -X POST http://localhost:5001/api/profile/manual \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "education_level": "Bachelor'"'"'s",
    "branch": "Computer Science",
    "experience_years": 2,
    "preferred_domains": "AI, Machine Learning"
  }'
```

### 3. Add Skills
```bash
curl -X POST http://localhost:5001/api/profile/skills \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "Python",
    "skill_level": "expert"
  }'
```

### 4. Get Recommendations
```bash
curl -X GET http://localhost:5001/api/recommendations \
  -H "Authorization: Bearer <token>"
```

### 5. Get Detailed Explanation
```bash
curl -X GET http://localhost:5001/api/recommendations/1 \
  -H "Authorization: Bearer <token>"
```

---

## Testing

The system is designed to be tested end-to-end:

1. **Create user account** with registration
2. **Fill profile** manually or upload resume
3. **Get recommendations** - system matches against 10 realistic jobs
4. **View explanations** - see why each job was recommended
5. **Get learning roadmap** - see path to acquire missing skills

---

## Match Score Calculation Algorithm

```
match_score = (mandatory_skills_found / mandatory_total) * 50 +
              (matched_skills / total_required * 100) * 0.5

Where:
- Mandatory skills are weighted 50%
- Optional skills are weighted 50%
- Score capped at 100

Example:
User: Python, ML, SQL (3 skills)
Job: Python (mandatory), ML (mandatory), Deep Learning, TensorFlow (4 skills)
Matched: 2/4 = 50%
Mandatory found: 2/2 = 100% → 50 points
Optional: 0/2 = 0% → 0 points (scaled to 50%)
Total: 50 + 0 = 50%
```

---

## Why This is "Cognitive AI"

1. **Not Magic**: Uses proven NLP & ML techniques
2. **Explainable**: Every recommendation has clear reasoning
3. **Realistic**: Based on actual job market data
4. **Adaptive**: Learns from user profiles manually or resumes
5. **Intelligent**: Rule-based reasoning + similarity matching
6. **Transparent**: XAI module explains all decisions

---

## Future Enhancements

- [ ] Integrate with LinkedIn job API
- [ ] Deep Learning embeddings (Transformers)
- [ ] User preference learning
- [ ] Skill gap quantification
- [ ] Video interviews analysis
- [ ] Industry trend analysis
- [ ] Salary negotiation guide
- [ ] Company culture fit scoring

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Flask 2.3 |
| Database | PostgreSQL / SQLite |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT |
| NLP | spaCy, NLTK |
| ML | scikit-learn, TensorFlow |
| File Parsing | PyPDF2, python-docx |
| API | REST (JSON) |
| CORS | Flask-CORS |

---

## License

Academic Project - 2026

