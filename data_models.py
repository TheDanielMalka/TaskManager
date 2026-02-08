from datetime import datetime
import json
import os

def load_learning_data():

    """ This func loads learned words data from JSON file.
        If file doesn't exist - creates it with initial empty categories.
        Returns dictionary with learned_categories and settings """

    file_path = "learned_words.json"
    if not os.path.exists(file_path):
        initial_data = {
            "learned_categories": {
                "Work": {}, "Study": {}, "Home": {}, "Health": {}, "Fun": {}
            },
            "settings": {"threshold": 5}
        }
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(initial_data, file, indent=4)
        return initial_data

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"learned_categories": {"Work": {}, "Study": {}, "Home": {}, "Health": {}, "Fun": {}},
                "settings": {"threshold": 5}}

def save_learning_data(data):

    """ This func saves updated learning data to JSON file """

    with open("learned_words.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def update_learning_model(category:str, remaining_words:list) -> None:

    """ This func updates word count for each remaining word in the detected category.
    Words that reach threshold will be used for future categorization """

    if not remaining_words:
        return
    data = load_learning_data()
    category_scores = data["learned_categories"].get(category, {})
    for word in remaining_words:
        category_scores[word] = category_scores.get(word, 0) + 1
    data["learned_categories"][category] = category_scores
    save_learning_data(data)

class TaskAttributes:

    """ Task as an object containing: task_name, priority (1-5), category, created_at """

    def __init__(self,task_name:str,priority:int,category:str,created_at:str=None):
        self.priority = priority
        self.task_name = task_name
        self.category = category
        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().strftime("%d/%m/%Y %H:%M")

def priority_analyze(input_list:list) -> int:

    """This func analyzes input words and returns priority level (1-5).
    Removes detected priority word from list.
    Returns 0 if no priority word found """

    priority_5 = ["crit", "urgent", "now", "asap", "immediate", "emergency", "deadly", "top", "burning", "instant"]
    priority_4 = ["please", "fast", "important", "soon", "priority", "quickly", "today", "must", "serious", "needed"]
    priority_3 = ["can", "normal", "regular", "standard", "maybe", "weekly", "routine", "usual", "next", "planning"]
    priority_2 = ["later", "someday", "slow", "whenever", "chill", "eventually", "backup", "secondary", "optional", "extra"]
    priority_1 = ["low", "future", "free", "spare", "ignore", "minor", "background", "trivial", "minimal", "easy"]
    for word in priority_5:
        if word in input_list:
            input_list.remove(word)
            return 5
    for word in priority_4:
        if word in input_list:
            input_list.remove(word)
            return 4
    for word in priority_3:
        if word in input_list:
            input_list.remove(word)
            return 3
    for word in priority_2:
        if word in input_list:
            input_list.remove(word)
            return 2
    for word in priority_1:
        if word in input_list:
            input_list.remove(word)
            return 1
    return 0

def category_analyze(input_list:list) -> tuple:

    """This func analyzes input words and returns (category_name, remaining_words).
    Uses hardcoded categories + learned words from JSON that reached threshold.
    Creates new categories when learned words reach threshold """

    stop_words = ["no",'yes','and','if','when','why']
    input_list = [word for word in input_list if word not in stop_words]
    categories = {
        "Work": ["office", "boss", "mail", "meeting", "project", "report", "salary", "client", "work", "job"],
        "Study": ["python", "exam", "math", "learn", "book", "university", "course", "homework", "test", "science"],
        "Home": ["clean", "cook", "buy", "laundry", "dishes", "fix", "rent", "garden", "home", "family"],
        "Health": ["gym", "doctor", "workout", "sport", "medicine", "dentist", "run", "water", "sleep", "healthy"],
        "Fun": ["movie", "game", "party", "trip", "beer", "friends", "vacation", "music", "hobby", "rest"]
    }
    data = load_learning_data()
    threshold = data["settings"]["threshold"]
    for category_name, words_dict in data["learned_categories"].items():
        for word, count in words_dict.items():
            if count >= threshold:
                if category_name not in categories:
                    categories[category_name] = []
                if word not in categories[category_name]:
                    categories[category_name].append(word)
    for key, sections in categories.items():
        for section in sections:
            if section in input_list:
                input_list.remove(section)
                return key, input_list
    return "General", input_list

def build_task(inp):

    """This func is the main function - builds TaskAttributes object from user input string.
    Analyzes priority, category, and updates learning model with remaining words """

    word = inp.lower().split()
    priority = priority_analyze(word)
    category_name, remaining_words = category_analyze(word)
    update_learning_model(category_name, remaining_words)
    new_word = " ".join(word)
    task = TaskAttributes(new_word,priority,category_name)
    return task