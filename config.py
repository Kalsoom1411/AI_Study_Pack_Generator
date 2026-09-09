# config.py

# Default Groq Model
DEFAULT_MODEL = "openai/gpt-oss-120b"

# System Prompt Templates for Multi-Stage AI Workflow
PLANNER_PROMPT = """
You are an Instructional Design Planner.
Analyze the provided study notes and build a pedagogical plan suited for target academic level: {level}.

Source Text:
{notes}

Return JSON strictly matching this structure:
{{
    "learning_objectives": ["objective 1", "objective 2"],
    "key_themes": ["theme 1", "theme 2"],
    "estimated_difficulty": "string"
}}
"""

CONTENT_PROMPT = """
You are an Expert Educational Content Creator.
Using the provided plan, draft comprehensive study materials from the raw notes.

Blueprint:
{plan}

Raw Notes:
{notes}

Return JSON strictly matching this structure:
{{
    "summary": "Comprehensive markdown summary of core concepts",
    "flashcards": [
        {{"question": "Question text", "answer": "Answer text"}}
    ]
}}
"""

ASSESSMENT_PROMPT = """
You are an Assessment Specialist.
Create 5 multiple-choice questions based on the learning objectives and material provided.

Learning Objectives:
{objectives}

Source Material:
{notes}

Return JSON array strictly matching this structure:
[
  {{
    "question": "Question stem",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Exact string matching one option",
    "explanation": "Rationale for answer"
  }}
]
"""

REVIEWER_PROMPT = """
You are a Lead Curriculum Reviewer.
Audit and refine this study bundle for educational accuracy, completeness, and formatting.

Bundle:
{bundle}

Return JSON strictly matching this structure:
{{
    "passed": true,
    "summary": "Polished final markdown summary",
    "flashcards": [{{"question": "string", "answer": "string"}}],
    "quiz": [
        {{
            "question": "string",
            "options": ["string", "string", "string", "string"],
            "correct_answer": "string",
            "explanation": "string"
        }}
    ]
}}
"""

            "explanation": "string"
        }}
    ]
}}
"""
