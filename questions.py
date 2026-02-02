import os
import json
import random
import requests
from dotenv import load_dotenv

class Question:
    """
    A class to control the formating of the questions as well as
    getting the questions, choices, answers along with checking them.
    """
    def __init__(self, question_text, answers, correct_answer, weighting):
        self._question_text = question_text
        self._answers = answers
        self._correct_answer = answers[ord(correct_answer.lower()) - ord('a')]
        self.weighting = weighting

    def get_question_text(self):
        return self._question_text

    def get_answers(self):
        return self._answers
    
    def get_correct_answer(self):
        return self._correct_answer
    
    def remove_two_incorrect(self):
        """
        Correlated with the fifty-fifty function wherein by using the corresponding lifeline,
        two wrong answers will be eliminated
        """
        idx = self._answers.index(self._correct_answer)
        idxs = list({0, 1, 2, 3} - {idx})
        remove = random.sample(idxs, 2)
        self._answers[remove[0]] = None
        self._answers[remove[1]] = None

    def check_answer(self, selected_answer):
        return selected_answer == self._correct_answer
    
class QuestionGenerator:
    def __init__(self, subject = "Who wants to be a millionaire", difficulty = "easy", n = 15, url = None, apikey = None):
        if url is None:
            self.url = (
                "https://cuhk-api-dev1-apim1.azure-api.net/openai/"
                "deployments/gpt-35-turbo/chat/completions?api-version=2023-05-15"
            )
        else:
            self.url = url
        if apikey is None:
            load_dotenv()
            self.apikey = os.getenv("APIM_SUBSCRIPTION_KEY")
        else:
            self.apikey = apikey

        if subject == "General Knowledge":
            self.subject = "Who wants to be a millionaire"
        else:
            self.subject = subject
        self.difficulty = difficulty
        self.questions = []
        self.n = n
        while True:
            try:
                self.__get()
            except:
                continue
            break

    def __get(self):
        payload = json.dumps({
            "model": "gpt-35-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello!"
                },
                {
                    "role": "assistant",
                    "content": "Hello! How can I assist you today?"            
                },
                {
                    "role": "user",
                    "content": f"We have a total of three difficulties: easy, medium and difficult. Give me only {self.n} different multiple choice {self.difficulty} question (who wants to be a millionaire level) about {self.subject} alone with its answer. The easy level should be around junior high school topic, the medium level should be around senior high school topic, and the hard level should be around university level topic. Output only {self.n} question. Outputting more questions or fewer questions will be not be tolerated. The choices must include the correct answer."
                },
                {
                    "role": "user",
                    "content": "I want you to give an answer that contains only the question, the options, and the letters corresponding to the answers; I don't need the words for everything else. I do not want any text accompanying your reply."
                },
                #{
                #    "role": "user",
                #    "content": f"I'd like your output to be formatted like: texts that you feel confident in answering this question, only the content of question, choices, only the letter of answer. Please make sure to always provide 4 choices of answer"
                #},
                {
                    "role": "user",
                    "content": f"Output only a JSON array without any additional text containing {self.n} dictionaries that have keys named 'question', 'choices', and 'answer' with questions being a string that contains only the content of the question, choices being a JSON array that contains only the answer options for the questions with A being the first element, B being the second element, C being the third element, and D being the fourth element, and the string answer which contains the letter corresponding to the index of the correct answer in the choices array (e.g. output A if the correct answer lies in the first index of the choices array). Do not include the letter in the choices array."
                },
                {
                    "role": "user",
                    "content": f"Your task is to only output only one JSON array containing only {self.n} dictionaries. The JSON dictionaries can only contain the keys named 'question', 'choices', and 'answer'; any other dictionary keys are not tolerated and are incorrect. Any other output, including English plaintext or JSON dictionaries, is not tolerated. Only valid JSON is accepted. You must not reply to my prompt in english plaintext or with anything that does not constitute valid JSON. Please only output a plain JSON string"
                },
            ]
        })

        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': self.apikey
        }

        response = requests.request("POST", self.url, headers = headers, data = payload)

        data = response.json()
        for question in json.loads(data["choices"][0]["message"]["content"]):
            self.questions.append(Question(question["question"], question["choices"], question["answer"], 100000))

    def __next__(self):
        """
        To get the next item in the iterator
        """
        if len(self.questions) == 0:
            raise StopIteration
        return self.questions.pop(0)
    
    def __iter__(self):
        """ Function defining the object as iterator"""
        return self

"""def answer_output(field: str, difficulty: str, n: int):
    if field == "General Knowledge":
        field = "Who wants to be a millionaire"

    load_dotenv()

    URL = (
        "https://cuhk-api-dev1-apim1.azure-api.net/openai/"
        "deployments/gpt-35-turbo/chat/completions?api-version=2023-05-15"
    )

    payload = json.dumps({
        "model": "gpt-35-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Hello!"
            },
            {
                "role": "assistant",
                "content": "Hello! How can I assist you today?"            
            },
            {
                "role": "user",
                "content": f"We have a total of three difficulties: easy, medium and difficult. Give me only {n} different multiple choice {difficulty} question (who wants to be a millionaire level) about {field} alone with its answer. The easy level should be around junior high school topic, the medium level should be around senior high school topic, and the hard level should be around university level topic. Output only {n} question. Outputting more questions or fewer questions will be not be tolerated. The choices must include the correct answer."
            },
            {
                "role": "user",
                "content": "I want you to give an answer that contains only the question, the options, and the letters corresponding to the answers; I don't need the words for everything else. I do not want any text accompanying your reply."
            },
            #{
            #    "role": "user",
            #    "content": f"I'd like your output to be formatted like: texts that you feel confident in answering this question, only the content of question, choices, only the letter of answer. Please make sure to always provide 4 choices of answer"
            #},
            {
                "role": "user",
                "content": f"Output only a JSON array without any additional text containing {n} dictionaries that have keys named 'question', 'choices', and 'answer' with questions being a string that contains only the content of the question, choices being a JSON array that contains only the answer options for the questions with A being the first element, B being the second element, C being the third element, and D being the fourth element, and the string answer which contains the letter corresponding to the index of the correct answer in the choices array (e.g. output A if the correct answer lies in the first index of the choices array). Do not include the letter in the choices array."
            },
            {
                "role": "user",
                "content": f"Your task is to only output only one JSON array containing only {n} dictionaries. The JSON dictionaries can only contain the keys named 'question', 'choices', and 'answer'; any other dictionary keys are not tolerated and are incorrect. Any other output, including English plaintext or JSON dictionaries, is not tolerated. Only valid JSON is accepted. You must not reply to my prompt in english plaintext or with anything that does not constitute valid JSON. Please only output a plain JSON string"
            },
        ]
    })

    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': os.getenv("APIM_SUBSCRIPTION_KEY")
    }

    response = requests.request("POST", URL, headers=headers, data=payload)

    print(response.text)

    data = response.json()
    res = json.loads(data["choices"][0]["message"]["content"])
    return res
    # return (res["questions"], res["choices"], res["answer"])
    ####
    print(data['choices'][0]['message']['content'])
    
    item = data['choices'][0]['message']['content']

    item = item.splitlines()

    for i in range(len(item)-1,-1,-1):
        if item[i]=='':
            item.remove(item[i])

    question = item[1].lstrip("Qquestion: Title")

    choices=[item[2],item[3],item[4],item[5]]

    for i in range(len(choices)):
        choices_list=choices[i].split()
        choices[i]=" ".join(choices_list[1:])

    answer=item[6].lstrip("Aanswer: ")

    if answer:
        answer=answer[0]
    else:
        answer='A'

    return question, choices, answer"""


# if __name__=="__main__":
    # fie=input("field: ")
    # dif=input("difficulty: ")
    #ques, cho, ans = answer_output(fie,dif)
    # print(answer_output("maths", "easy", 15))