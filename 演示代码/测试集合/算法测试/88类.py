import tkinter as tk
import openai

openai.api_key = "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"

def generate_text(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )

    message = response.choices[0].text
    return message.strip()

def get_response():
    prompt = input_text.get()
    response = generate_text(prompt)
    output_text.config(state="normal")
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, response)
    output_text.config(state="disabled")

# 创建主窗口
window = tk.Tk()
window.title("Chatbot")

# 创建输入框
input_text = tk.Entry(window, width=50)
input_text.pack(padx=10, pady=10)

# 创建按钮
button = tk.Button(window, text="Send", command=get_response)
button.pack(padx=10, pady=10)

# 创建输出框
output_text = tk.Text(window, width=50, height=10, state="disabled")
output_text.pack(padx=10, pady=10)

# 运行主循环
window.mainloop()
