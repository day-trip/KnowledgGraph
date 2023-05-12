import openai

openai.organization = "org-ts0ZGZJ0sMImE295wod1O2i8"
openai.api_key = "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"

content = """
John Locke FRS (/lɒk/; 29 August 1632 – 28 October 1704) was an English philosopher and physician, widely regarded as one of the most influential of Enlightenment thinkers and commonly known as the "father of liberalism".[14][15][16] Considered one of the first of the British empiricists, following the tradition of Francis Bacon, Locke is equally important to social contract theory. His work greatly affected the development of epistemology and political philosophy. His writings influenced Voltaire and Jean-Jacques Rousseau, and many Scottish Enlightenment thinkers, as well as the American Revolutionaries. His contributions to classical republicanism and liberal theory are reflected in the United States Declaration of Independence.[17] Internationally, Locke's political-legal principles continue to have a profound influence on the theory and practice of limited representative government and the protection of basic rights and freedoms under the rule of law.[18]
""".strip()

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
    {"role": "system", "content": "You are an AI system that generates information for a knowledge graph based on data"},
    {"role": "user", "content": f"Generate as many knowledge triples as possible from the following data in the format of (parent, child, relation, content), where content is of the child and can be a longer multiline string.\n\n${content}"}
])
print(completion.choices[0].message.content)
