import tkinter as tk
from tkinter import messagebox
import json

# Tải câu hỏi từ file JSON
def load_questions(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Chuyển đổi danh sách câu hỏi thành cấu trúc theo chủ đề
def categorize_by_topic(questions):
    topics = {}
    for topic, qlist in questions.items():
        topics[topic] = qlist
    return topics

# Lớp ứng dụng Quiz GUI
class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ứng dụng Quiz Trắc Nghiệm")
        self.master.geometry("600x400")

        self.questions_by_topic = categorize_by_topic(load_questions("questions.json"))
        self.topic = None
        self.questions = []
        self.current_question_index = 0
        self.score = 0

        self.setup_topic_selection()

    # Giao diện chọn chủ đề
    def setup_topic_selection(self):
        self.clear_window()
        tk.Label(self.master, text="Chọn một chủ đề:", font=("Arial", 16)).pack(pady=10)

        for topic in self.questions_by_topic.keys():
            tk.Button(self.master, text=topic, font=("Arial", 14),
                      command=lambda t=topic: self.start_quiz(t)).pack(pady=5)

    # Bắt đầu quiz
    def start_quiz(self, topic):
        self.topic = topic
        self.questions = self.questions_by_topic[topic]
        self.current_question_index = 0
        self.score = 0
        self.show_question()

    # Hiển thị từng câu hỏi
    def show_question(self):
        self.clear_window()

        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            tk.Label(self.master, text=f"Câu {self.current_question_index + 1}: {question['question']}",
                     font=("Arial", 14), wraplength=500, justify="left").pack(pady=10)

            self.answer_var = tk.StringVar()

            for key, value in question['options'].items():
                tk.Radiobutton(self.master, text=f"{key}. {value}", variable=self.answer_var,
                               value=key, font=("Arial", 12)).pack(anchor="w")

            tk.Button(self.master, text="Gửi đáp án", command=self.submit_answer).pack(pady=20)
        else:
            self.show_result()

    # Xử lý câu trả lời
    def submit_answer(self):
        selected = self.answer_var.get()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đáp án!")
            return

        correct = self.questions[self.current_question_index]['answer']
        if selected.upper() == correct.upper():
            self.score += 1

        self.current_question_index += 1
        self.show_question()

    # Kết quả cuối cùng
    def show_result(self):
        self.clear_window()
        total = len(self.questions)
        percent = (self.score / total) * 100

        result_text = f"Kết thúc!\nBạn trả lời đúng {self.score}/{total} câu\nĐiểm: {percent:.2f}%"
        tk.Label(self.master, text=result_text, font=("Arial", 16)).pack(pady=30)

        tk.Button(self.master, text="Chơi lại", command=self.setup_topic_selection).pack()
        tk.Button(self.master, text="Thoát", command=self.master.quit).pack(pady=10)

    # Dọn sạch màn hình trước mỗi lần render
    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()


# Khởi động ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
