"""
Build With AI — Alexander AI Course Platform
A lightweight Flask app serving the course home, module list, and lesson visual walkthroughs.
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template, send_from_directory, abort, jsonify

app = Flask(__name__)

# ── Lesson registry ────────────────────────────────────────────────────────────
MODULES = [
    {
        "id": 1,
        "title": "The Foundation",
        "subtitle": "Understand what AI agents can do for your business",
        "color": "#7c3aed",
        "lessons": [
            {"id": "1-1", "title": "What Is an AI Agent?", "duration": "15 min"},
            {"id": "1-2", "title": "Your Business Automation Map", "duration": "20 min"},
        ]
    },
    {
        "id": 2,
        "title": "Your First AI Agent",
        "subtitle": "Build and deploy a live AI agent in one session",
        "color": "#0891b2",
        "lessons": [
            {"id": "2-1", "title": "Setting Up OpenRouter", "duration": "10 min"},
            {"id": "2-2", "title": "Writing Your System Prompt", "duration": "20 min"},
            {"id": "2-3", "title": "Deploying Your Agent Live", "duration": "25 min"},
        ]
    },
    {
        "id": 3,
        "title": "Building Your First App",
        "subtitle": "Go from idea to a live web app on the internet",
        "color": "#0d9488",
        "lessons": [
            {"id": "3-3", "title": "Using AI to Build Your App", "duration": "30 min"},
            {"id": "3-4", "title": "Deploying to Railway", "duration": "25 min"},
        ]
    },
    {
        "id": 4,
        "title": "Automation & Notifications",
        "subtitle": "Make your apps work while you sleep",
        "color": "#b45309",
        "lessons": [
            {"id": "4-1", "title": "Customer Notifications: Text & Email", "duration": "25 min"},
        ]
    },
    {
        "id": 5,
        "title": "Business Playbooks",
        "subtitle": "Your industry-specific build plan",
        "color": "#be185d",
        "lessons": [
            {"id": "5-1", "title": "Pick Your Business Playbook", "duration": "20 min"},
        ]
    },
    {
        "id": 6,
        "title": "Launch & Level Up",
        "subtitle": "Go live, get students, build your next app",
        "color": "#1d4ed8",
        "lessons": [
            {"id": "6-1", "title": "Your 90-Day Roadmap", "duration": "20 min"},
        ]
    },
]

LESSON_META = {}
for mod in MODULES:
    for lesson in mod["lessons"]:
        LESSON_META[lesson["id"]] = {
            **lesson,
            "module_id": mod["id"],
            "module_title": mod["title"],
            "module_color": mod["color"],
        }

LESSONS_DIR = Path(__file__).parent / "lessons"


def get_lesson_steps(lesson_id):
    """Load steps.json for a lesson if it exists."""
    steps_file = LESSONS_DIR / f"lesson-{lesson_id}" / "steps.json"
    if steps_file.exists():
        with open(steps_file) as f:
            return json.load(f)
    return None


@app.route("/")
def index():
    return render_template("index.html", modules=MODULES)


@app.route("/module/<int:module_id>")
def module_page(module_id):
    mod = next((m for m in MODULES if m["id"] == module_id), None)
    if not mod:
        abort(404)
    return render_template("module.html", module=mod, modules=MODULES)


@app.route("/lesson/<lesson_id>")
def lesson_page(lesson_id):
    meta = LESSON_META.get(lesson_id)
    if not meta:
        abort(404)
    steps_data = get_lesson_steps(lesson_id)

    # Find prev/next lessons
    all_lesson_ids = [l["id"] for m in MODULES for l in m["lessons"]]
    idx = all_lesson_ids.index(lesson_id) if lesson_id in all_lesson_ids else -1
    prev_id = all_lesson_ids[idx - 1] if idx > 0 else None
    next_id = all_lesson_ids[idx + 1] if idx < len(all_lesson_ids) - 1 else None

    return render_template(
        "lesson.html",
        lesson_id=lesson_id,
        meta=meta,
        steps_data=steps_data,
        prev_id=prev_id,
        next_id=next_id,
        prev_meta=LESSON_META.get(prev_id),
        next_meta=LESSON_META.get(next_id),
        modules=MODULES,
    )


@app.route("/lessons/<lesson_id>/<filename>")
def lesson_asset(lesson_id, filename):
    """Serve screenshots and other assets for a lesson."""
    asset_dir = LESSONS_DIR / f"lesson-{lesson_id}"
    if not asset_dir.exists():
        abort(404)
    return send_from_directory(str(asset_dir), filename)


@app.route("/health")
def health():
    return jsonify({"app": "Build With AI — Alexander AI Course", "status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
