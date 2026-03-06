"""Skill-based role matcher used by the dashboard analysis endpoint."""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Set

from utils.data_processor import DataProcessor


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
ROLES_PATH = os.path.join(DATA_DIR, "career_roles.json")


def _tokenize_skills(raw_skills: Any) -> List[str]:
    """Normalize skills from mixed input shapes into clean, lowercase tokens."""
    if not raw_skills:
        return []

    if isinstance(raw_skills, str):
        candidates = raw_skills.split(",")
    elif isinstance(raw_skills, list):
        candidates = raw_skills
    else:
        return []

    normalized = []
    for item in candidates:
        text = re.sub(r"\s+", " ", str(item).strip().lower())
        if text:
            normalized.append(text)

    # Keep insertion order while removing duplicates.
    return list(dict.fromkeys(normalized))


def _normalize_profile(user_data: Dict[str, Any]) -> Dict[str, Any]:
    skills = _tokenize_skills(user_data.get("skills", []))

    interests_raw = user_data.get("interests", [])
    if isinstance(interests_raw, str):
        interests = _tokenize_skills(interests_raw)
    elif isinstance(interests_raw, list):
        interests = _tokenize_skills(interests_raw)
    else:
        interests = []

    experience = user_data.get("experience", []) or []
    years = 0.0
    if isinstance(experience, list):
        for entry in experience:
            try:
                years += float(entry.get("years", 0))
            except (TypeError, ValueError, AttributeError):
                continue

    return {
        "skills": skills,
        "skills_set": set(skills),
        "interests": interests,
        "experience_years": years,
        "education": user_data.get("education", {}) or {},
    }


def _load_roles() -> List[Dict[str, Any]]:
    with open(ROLES_PATH, "r", encoding="utf-8") as f:
        payload = json.load(f)
    return payload if isinstance(payload, list) else []


def build_roadmap(missing: List[str], related: List[str]) -> List[Dict[str, Any]]:
    """Generate a compact, structured roadmap used by the dashboard."""
    structured_roadmap = []
    priority_skills = list(dict.fromkeys((missing or []) + (related or [])))[:4]

    for idx, skill in enumerate(priority_skills, 1):
        structured_roadmap.append(
            {
                "phase": f"Phase {idx}: {skill.title()} Mastery",
                "actions": [
                    f"Complete a focused project using {skill}",
                    f"Practice {skill} through role-specific exercises",
                    f"Document what you learned in a portfolio artifact",
                ],
                "estimated_time": "2-4 weeks",
            }
        )

    return structured_roadmap


def build_explanation(matched: List[str], missing: List[str]) -> Dict[str, Any]:
    """Return explainability messages for recommendation cards."""
    return {
        "strengths": [f"Strong overlap in {skill}" for skill in matched[:3]],
        "gaps": [f"Upskill in {skill}" for skill in missing[:3]],
        "summary": f"Matched {len(matched)} required skills.",
    }


def _experience_bucket(years: float) -> str:
    if years >= 6:
        return "senior"
    if years >= 2:
        return "mid"
    return "entry"


def _score_role(user_skills: Set[str], required_skills: List[str]) -> Dict[str, Any]:
    required = _tokenize_skills(required_skills)
    if not required:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = [skill for skill in required if skill in user_skills]
    missing = [skill for skill in required if skill not in user_skills]
    score = round((len(matched) / len(required)) * 100, 2)

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
    }


def _extract_market_skills(user_skills: List[str]) -> Dict[str, int]:
    """Return top market-demand skills from live/local job data."""
    processor = DataProcessor()
    query = " ".join(user_skills[:3]).strip() or "software developer"
    market = processor.get_job_market_data({"query": query, "location": "India", "results": 15})

    if not isinstance(market, dict):
        return {}

    top_skills = market.get("top_skills")
    if isinstance(top_skills, dict) and top_skills:
        return {str(k): int(v) for k, v in top_skills.items() if str(k).strip()}

    # When using live API, parse the live job descriptions to infer demand counts.
    live_jobs = market.get("live_jobs") or market.get("jobs") or []
    if not isinstance(live_jobs, list):
        return {}

    counts: Dict[str, int] = {}
    known_skills = {
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "node",
        "sql",
        "aws",
        "docker",
        "kubernetes",
        "machine learning",
        "data analysis",
        "excel",
        "linux",
        "flask",
        "django",
    }

    for job in live_jobs:
        blob = " ".join(
            [
                str(job.get("job_title", "")),
                str(job.get("description", "")),
            ]
        ).lower()
        for skill in known_skills:
            if skill in blob:
                counts[skill] = counts.get(skill, 0) + 1

    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:15])


def match_roles(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Match user profile to available roles and return explainable recommendations."""
    profile = _normalize_profile(user_data or {})
    roles = _load_roles()

    experience_bucket = _experience_bucket(profile["experience_years"])
    recommendations: List[Dict[str, Any]] = []

    for role in roles:
        required = role.get("required_skills", [])
        scored = _score_role(profile["skills_set"], required)

        # Soft boost if role level aligns with user experience.
        role_level = str(role.get("experience_level", "entry")).lower()
        level_bonus = 5 if role_level == experience_bucket else 0
        adjusted_score = min(100, round(scored["match_score"] + level_bonus, 2))

        explanation = build_explanation(scored["matched_skills"], scored["missing_skills"])
        recommendations.append(
            {
                "job_title": role.get("role", "Career Role"),
                "required_skills": required,
                "experience_level": role_level,
                "match_score": adjusted_score,
                "matched_skills": scored["matched_skills"],
                "missing_skills": scored["missing_skills"],
                "related_skills_to_learn": role.get("related_skills_to_learn", []),
                "explanation": [
                    explanation["summary"],
                    *explanation["strengths"],
                    *explanation["gaps"],
                ],
                "roadmap": build_roadmap(
                    scored["missing_skills"], role.get("related_skills_to_learn", [])
                ),
            }
        )

    recommendations.sort(key=lambda item: item["match_score"], reverse=True)

    return {
        "recommendations": recommendations[:10],
        "normalized_profile": {
            "skills": profile["skills"],
            "interests": profile["interests"],
            "experience_years": profile["experience_years"],
            "experience_level": experience_bucket,
            "education": profile["education"],
        },
        "market_skills": _extract_market_skills(profile["skills"]),
    }
