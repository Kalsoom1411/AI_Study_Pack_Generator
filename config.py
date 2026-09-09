# config.py

# Recommended Groq Model
DEFAULT_MODEL = "openai/gpt-oss-120b"

# System Prompt Templates
PLANNER_PROMPT = """
You are an Instructional Design Planner.
Analyze the raw material and create a structured study plan for target academic level: {level}.

Raw Text:
{notes}

Return JSON strictly matching this structure (no conversational preamble):
{{
    "learning_objectives": ["string"],
    "key_themes": ["string"],
    "estimated_difficulty": "string"
}}
"""

CONTENT_PROMPT = """
You are an Expert Educational Content Creator.
Use the pedagogical blueprint below to draft core study materials from the raw notes.

Blueprint:
{plan}

Raw Notes:
{notes}

Return JSON strictly matching this structure (no conversational preamble):
{{
    "summary": "Detailed markdown formatted summary covering all learning objectives",
    "flashcards": [
        {{"question": "Front of card question", "answer": "Back of card concise answer"}}
    ]
}}
"""

ASSESSMENT_PROMPT = """
You are an Assessment Engine Specialist.
Construct 5 challenging multiple-choice questions based on the learning objectives and source material.

Learning Objectives:
{objectives}

Source Material:
{notes}

Return a JSON array strictly matching this structure (no conversational preamble):
[
  {{
    "question": "Clear question stem",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Exact string matching one of the options",
    "explanation": "Detailed rationale explaining why the answer is correct"
  }}
]
"""

REVIEWER_PROMPT = """
You are a Lead Curriculum Reviewer.
Audit this generated Study Pack bundle for factual consistency, target difficulty accuracy, and formatting completeness.

Generated Study Bundle:
{bundle}

Refine and fix any formatting errors or incomplete explanations.
Return JSON strictly matching this structure (no conversational preamble):
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