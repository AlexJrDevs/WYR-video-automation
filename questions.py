import os
import tkinter as tk
from tkinter import simpledialog, filedialog
import json
import sys
from PIL import Image

class QuestionManager:
    def check_question_lengths(self):
        for question_entry in self.question_data:
            if len(question_entry["question"]) > 40:
                answer = input(f"The question '{question_entry['question']}' has more than 40 characters. Do you want to change it? (yes/no): ")
                if answer.lower() == "yes":
                    new_question = input("Enter the new question: ")
                    question_entry["question"] = new_question
                    self.save_question_data()

    def __init__(self, data_file):
        self.data_file = data_file
        self.load_question_data()

    def load_question_data(self):
        try:
            with open(self.data_file, "r") as f:
                self.question_data = json.load(f)
        # Sanitize the loaded questions
                self.sanitize_questions() # Removes (.) , ("), (,)
        except FileNotFoundError:
            self.question_data = []

    def sanitize_questions(self):
        for question_entry in self.question_data:
            question_entry["question"] = self.sanitize_string(question_entry["question"])

    @staticmethod
    def sanitize_string(input_string):
        # Remove periods and double quotes from the input string and add capitilaziation
        sanitized_string = input_string.upper().replace(".", "").replace(",", "").replace("\"", "")
        return sanitized_string

    def save_question_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.question_data, f, indent=4)

    def add_question(self, question, image_path, section):
        self.question_data.append({"question": question, "image_path": image_path, "section": section})
        self.save_question_data()

    def get_section_questions(self, section):
        return [question for question in self.question_data if question["section"] == section]
    

    def get_section_question_with_image(self, section):
        section_questions = self.get_section_questions(section)
        
        if not section_questions:
            print("No more questions")
            sys.exit()
        
        for question in section_questions:
            if len(question["question"]) <= 70:
                image_path = os.path.normpath(os.path.join(base_image_folder, question["image_path"]))

                # Check the image format and convert to JPG if necessary
                image = Image.open(image_path)
                if image.format not in ['JPEG', 'JPG']:
                    image = image.convert('RGB')
                    new_image_path = os.path.splitext(image_path)[0] + ".jpg"
                    image.save(new_image_path, "JPEG")
                    image_path = new_image_path

                # Remove the question from the data
                self.remove_used_question(question)
                
                return question["question"], image_path

        print("No questions under 70 characters")
        sys.exit()

    
    def remove_used_question(self, question_to_remove):
        self.question_data = [q for q in self.question_data if q != question_to_remove]
        self.save_question_data()


    
# File to store the question data
data_file = "question_data.json"
base_image_folder = "C:/Users/Alexa/Documents/TikTok Automation/Rather Automation/Images"  # Update this with your image folder path

# Initialize QuestionManager
question_manager = QuestionManager(data_file)

# Function to add a new question
def add_question():
    question = simpledialog.askstring("Input", "Enter the question:")
    if question:
        if len(question) > 40:
            print("Question exceeds 40 characters. Please enter a shorter question.")
            return
        
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if image_path:
            relative_image_path = os.path.relpath(image_path, base_image_folder)
            question_manager.add_question(question, relative_image_path, len(question_manager.question_data) % 2 + 1)
            question_manager.check_question_lengths()  # Check and prompt to change long questions
            update_question_count()

# Function to update the question count label
def update_question_count():
    question_count.set(f"Questions: {len(question_manager.question_data)}")


# Initialize the GUI
root = tk.Tk()
root.title("Question Entry")

question_count = tk.StringVar()
question_count_label = tk.Label(root, textvariable=question_count)
question_count_label.pack()

add_question_button = tk.Button(root, text="Add Question", command=add_question)
add_question_button.pack()

update_question_count()  # Initial update of the question count label

root.mainloop()
