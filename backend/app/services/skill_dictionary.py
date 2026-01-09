"""
Central skill dictionary used by both
resume parsing and JD parsing.

Canonical skill -> list of variants
"""

SKILL_MAP = {
    # Frontend
    "react": ["react", "reactjs", "react.js"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "html": ["html"],
    "css": ["css"],

    # Backend
    "java": ["java"],
    "spring boot": ["spring boot", "springboot"],
    "spring": ["spring framework"],
    "python": ["python"],
    "node.js": ["node", "node.js", "nodejs"],
    "express": ["express", "express.js"],

    # Databases
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],

    # Messaging / Caching
    "kafka": ["kafka", "apache kafka"],
    "redis": ["redis"],
    "rabbitmq": ["rabbitmq"],

    # DevOps / Cloud
    "docker": ["docker", "dockerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "gcp": ["gcp", "google cloud"],
    "azure": ["azure"],

    # Tools
    "git": ["git", "github", "gitlab"],
    "linux": ["linux"],
}
