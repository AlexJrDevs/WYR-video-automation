import json
import random

# Load the JSON file
with open('question_file.json', 'r') as file:
    data = json.load(file)

# Separate questions into section 1 and section 2 lists
questions_section_1 = [item for item in data if item['section'] == 1]
questions_section_2 = [item for item in data if item['section'] == 2]

# Shuffle the questions within each section independently
random.shuffle(questions_section_1)
random.shuffle(questions_section_2)

# Combine the shuffled questions back together while maintaining the alternation
shuffled_data = []

for q1, q2 in zip(questions_section_1, questions_section_2):
    shuffled_data.append(q1)
    shuffled_data.append(q2)

# If there are extra questions in one section, append them to the end
shuffled_data.extend(questions_section_1[len(questions_section_2):])
shuffled_data.extend(questions_section_2[len(questions_section_1):])

# Create a set to store unique questions
unique_questions = set()

# Create a new list to store non-duplicate entries
filtered_data = []

# Iterate through the data and filter out duplicates
for entry in shuffled_data:
    question = entry['question']
    if question not in unique_questions:
        unique_questions.add(question)
        filtered_data.append(entry)
    else:
        print(f"Duplicate question found: {question}")

# Save the shuffled and filtered data to a new JSON file
with open('question_data.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)

print(f"Removed {len(shuffled_data) - len(filtered_data)} duplicate questions.")
