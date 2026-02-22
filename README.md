# TaskManager

Python task management app with a self-learning classification system. The app learns from your input over time to automatically assign priority levels and categories to new tasks.

## How it works

When you add a task, the system analyzes your input:
- **Priority detection** – keywords like "urgent", "important", "later" set priority (1-5)
- **Category detection** – keywords like "gym", "exam", "cook" assign categories (Work, Study, Home, Health, Fun)
- **Self-learning** – words that don't match any keyword get tracked. After enough uses in a category, the system learns them automatically

For example, if you keep adding tasks with the word "milk" under Home, eventually the system will recognize "milk" as a Home keyword on its own.

## Features

- Add, edit, remove, and mark tasks as done
- Auto-sort by priority and date
- Duplicate detection
- JSON-based persistence (tasks + learning model)
- Dockerized with docker-compose and volume support

## Project structure

```
├── TaskManager.py       # Main app - menu, user interaction, task operations
├── data_models.py       # Task class, priority/category analysis, learning logic
├── TaskManager.json     # Saved tasks (persistent)
├── learned_words.json   # Learning model data (persistent)
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## How to run

**Without Docker:**
```bash
python TaskManager.py
```

**With Docker:**
```bash
docker-compose run --rm taskmanager
```

The docker-compose setup uses volumes so your tasks and learned words persist between runs.

## Tech

Python, OOP, JSON, File I/O, Docker, docker-compose
