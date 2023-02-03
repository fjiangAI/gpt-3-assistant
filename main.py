import datetime
import os
import tkinter as tk
import tkinter.simpledialog

import openai
import pygame
from gtts import gTTS


def save_history(chat_history):
    # 假设history_chat为一个包含有时间、用户对话、GPT-3的对话的元组的历史聊天记录
    with open("history_chat.txt", "a", encoding="utf-8") as f:
        chat = chat_history[-1]
        time = chat[0]
        user_dialogue = chat[1]
        gpt3_dialogue = chat[2]
        f.write("Time: " + str(time) + "\n")
        f.write("User Dialogue: " + user_dialogue + "\n")
        f.write("GPT-3 Dialogue: " + gpt3_dialogue + "\n")
        f.write("---------------------------------")
        f.close()


def on_click():
    user_input = user_entry.get()
    confirm_button.config(state="disabled")
    result = generate_string(user_input)
    result_text.delete("1.0", tk.END)
    result_text.insert("1.0", result)
    # read_content(result)
    chat_history.append(
        (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_input, result)
    )
    save_history(chat_history)
    confirm_button.config(state="normal")


def generate_string(user_input):
    openai.api_key = key
    prompt = user_input
    response = openai.Completion.create(
        engine="text-chat-davinci-002-20221122",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    generated_response = response["choices"][0]["text"]
    return generated_response


def read_content(text_content):
    def speak():
        # 初始化pygame
        pygame.init()
        # 加载要播放的语音文件
        pygame.mixer.music.load("temp.mp3")
        # 播放语音文件
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()

    def play_text(text):
        tts = gTTS(text=text, lang="zh")
        tts.save("temp.mp3")
        speak()

    play_text(text_content)


def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("历史记录")

    history_text = tk.Text(history_window, width=80, height=30)
    for date, user_input, result in chat_history:
        history_text.insert(tk.END, f"{date}\n", ("bold_text"))
        history_text.insert(tk.END, f"用户：", ("bold_text"))
        history_text.insert(tk.END, f"{user_input}\n")
        history_text.insert(tk.END, f"GPT-3：", ("bold_text"))
        history_text.insert(tk.END, f"{result}\n", ("bold_text"))
        history_text.insert(tk.END, "------------------\n")
    history_text.pack()


root = tk.Tk()
root.title("GPT-3助手")

key = tkinter.simpledialog.askstring("Key Input", "Enter your key:", show="*")

label = tk.Label(root, text="我是GPT-3，有什么可以帮助您?", wraplength=800)
label.pack()

user_entry = tk.Entry(root, width=80)
user_entry.pack()

result_text = tk.Text(root)
result_text.pack()

confirm_button = tk.Button(root, text="问问GPT-3", command=on_click)
confirm_button.pack()

chat_history = []

history_button = tk.Button(root, text="历史记录", command=show_history)
history_button.pack()

root.mainloop()
