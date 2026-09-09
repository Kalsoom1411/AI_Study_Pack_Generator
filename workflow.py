# workflow.py

import json
from groq import Groq
import config

def get_client(api_key: str) -> Groq:
    """Initializes Groq client with API key."""
    return Groq(api_key=api_key)

def _call_json_model(client: Groq, prompt: str) -> dict:
    """Executes call to Groq model expecting structured JSON."""
    response = client.chat.completions.create(
        model=config.DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    return json.loads(response.choices[0].message.content)

def run_study_pack_pipeline(client: Groq, notes: str, level: str, status_callbacks: dict) -> dict:
    """Orchestrates 4-stage pipeline: Planning -> Generation -> Assessment -> QA & Refinement."""
    # Stage 1: Planning
    if "stage1" in status_callbacks:
        status_callbacks["stage1"]("⏳ Stage 1: Building Pedagogical Blueprint...")
    plan_prompt = config.PLANNER_PROMPT.format(level=level, notes=notes)
    plan = _call_json_model(client, plan_prompt)

    # Stage 2: Content Generation
    if "stage2" in status_callbacks:
        status_callbacks["stage2"]("⏳ Stage 2: Generating Core Summary & Flashcards...")
    content_prompt = config.CONTENT_PROMPT.format(plan=json.dumps(plan), notes=notes)
    content = _call_json_model(client, content_prompt)

    # Stage 3: Assessment Creation
    if "stage3" in status_callbacks:
        status_callbacks["stage3"]("⏳ Stage 3: Crafting Interactive Quiz Questions...")
    assessment_prompt = config.ASSESSMENT_PROMPT.format(
        objectives=json.dumps(plan.get("learning_objectives", [])),
        notes=notes
    )
    quiz = _call_json_model(client, assessment_prompt)

    # Stage 4: Review & Refinement
    if "stage4" in status_callbacks:
        status_callbacks["stage4"]("⏳ Stage 4: Performing QA & Final Refinement...")
    bundle = {"plan": plan, "content": content, "quiz": quiz}
    reviewer_prompt = config.REVIEWER_PROMPT.format(bundle=json.dumps(bundle))
    final_output = _call_json_model(client, reviewer_prompt)

    return final_output
