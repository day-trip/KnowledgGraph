import os
from thinkgpt.llm import ThinkGPT
import json5
from actions import Actions
from googlesearch import search
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver


os.environ["OPENAI_API_KEY"] = "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"
llm = ThinkGPT(model_name="gpt-3.5-turbo", openai_api_key="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")


def search_google(query) -> str:
    """
    Search results on google
    """
    print(query)
    sresults = []
    for sresult in search(query, num_results=5, advanced=True):
        print(sresult)
        sresults.append(f"{sresult.title} ({sresult.url})\n{sresult.description[:20]}")
    return '\n-----\n'.join(sresults)


def browse_website(url, question) -> str:
    """
    Browse a website in order to answer a question
    """
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    for s in soup(['style', 'script', 'head', 'title', 'meta', '[document]']):
        s.extract()
    for s in soup(['style', 'script', 'head', 'title', 'meta', '[document]']):
        s.extract()
    return s.getText()[:200]


ax = Actions()
ax.register_action(search_google)
ax.register_action(browse_website)
previous_action = None
result = None
reasoning = None
history = []
while True:
    llm_result = llm.predict(f"""
Your name is ChefGPT. You are a fully autonomous AI agent that uses memory and tasks to complete goals.
Goals
1). Find an interesting upcoming holiday
2). Come up with a unique recipe based on that holiday
3). Email the recipe to jainitaigiri@gmail.com
Goals must be completed in order, and can be completed via any tool avaliable to you. Make sure to use specific details from your memory and don't repeat instructions.

{"" if previous_action is None else "Previous actions:" + chr(10)}{"" if previous_action is None else f"{chr(10).join(history)}"}
Previous action: {previous_action if previous_action is not None else "This will be your first action"}
{"" if previous_action is None else "Result:"}
{"" if previous_action is None else result}
{"" if previous_action is None else f"Why you made your previous action: {reasoning}"}

Useful information:
Today is {str(datetime.now().strftime("%A, %B %d, %Y"))}

You must perform an action relevant to completing your next goal. You must invoke an action as a python function in the format of action(*args). All arguments are strings.
Avaliable actions:
{ax.context()}

The final result must be in VALID JSON format. Expected schema: {{observations: string (observations about the result of your previous action, including key details from the result, null if N/A), action: string (the action you want to perform in the function format specified earlier; action(*args)), reasoning: string (why you are making this action, null if N/A)}}. Your result must match the scheme exactly. No extra fields.
{{
""")
                             

    print(llm_result)
    TEMP = """
exit() - Exit out if all goals are completed or there is a major issue
search_google(query)
browse_website(url, question) - Answer a question by browsing a website
send_email(recipient, subject, content)
remember(question) - Try to remember useful observations from memory to answer a question
    """
    parsed = json5.loads("{" + llm_result)
    if previous_action and reasoning:
        history.append(previous_action + " - " + reasoning)
    previous_action = parsed["action"]
    # todo fix reasoning and observations
    reasoning = parsed["reasoning"]
    if previous_action == "null":
        print("Null action!")
        break
    result = ax.call(previous_action)
    print(result)
    if input("Continue: ") != "y":
        break
