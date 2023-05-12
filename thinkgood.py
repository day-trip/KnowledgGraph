import os
import inspect
from thinkgpt.llm import ThinkGPT
import json5


os.environ["OPENAI_API_KEY"] = "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"

llm = ThinkGPT(model_name="gpt-3.5-turbo", openai_api_key="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")

previous_action = "This will be your first action"
result = "null"
while True:
    llm_result = llm.predict(f"""
Your name is ChefGPT. You are a fully autonomous AI agent that uses memory and tasks to complete goals.
Goals
1). Find an interesting upcoming holiday
2). Come up with a unique recipe based on that holiday
3). Email the recipe to jainitaigiri@gmail.com
Goals must be completed in order, and can be completed via any tool avaliable to you. Make sure to use specific details from your memory and don't repeat instructions.

Your previous action: {previous_action}
The result of your previous action:
{result}

You must perform an action relevant to completing your next goal. You must invoke an action as a python function in the format of action(**kwargs). All arguments are strings.
Avaliable actions:
exit() - Exit out if all goals are completed or there is a major issue
search_google(query)
browse_website(url, question) - Answer a question by browsing a website
send_email(recipient, subject, content)
remember(question) - Try to remember useful observations from memory to answer a question

The final result must be in VALID JSON format. Expected schema: {{observations: string (observations about the result of your previous action, null if N/A), action: string (the action you want to perform in the function format specified earlier; action(**kwargs))}}. Your result must match the scheme exactly. No extra fields.
{{
""")

    print(llm_result)
    parsed = json5.loads("{" + llm_result)
    previous_action = parsed["action"]
    if previous_action == "null":
        print("Null action!")
        break
    result = "400 - No internet connection; please connect to the wifi"
    if input("Continue: ") != "y":
        break
