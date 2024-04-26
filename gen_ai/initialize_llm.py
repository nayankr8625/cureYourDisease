from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from fuzzywuzzy import process
from gen_ai.prompt_template import chat_template, classify_symptomps, main_symptom_list


GROQ_API_KEY = "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"

class llm:

    def __init__(self, model_temperature=0.1, model_name="mixtral-8x7b-32768",
                 max_tokens=4096):
        self._model_temp = model_temperature
        self._model_name = model_name
        self._maxtoken = max_tokens
        self._llm = ChatGroq(temperature=self._model_temp, groq_api_key=GROQ_API_KEY,
                        model_name=self._model_name,max_tokens=self._maxtoken)

    def chat(self):
        
        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"], template=chat_template
        )
        self._memory = ConversationBufferWindowMemory(memory_key="chat_history", ai_prefix="ai",
                                                human_prefix="human",k=8)
        llm_chain = LLMChain(
            llm=self._llm,
            prompt=prompt,
            verbose=False,
            memory=self._memory,
        )
        return llm_chain, self._memory
    
    def classify_symptomps(self):
        response = self._llm.predict(classify_symptomps.format(chat_history = self._memory))
        return response
    
    def find_similar_symptom(self,user_symptom, main_symptom_list=main_symptom_list):
        return process.extractOne(user_symptom, main_symptom_list)[0]
    

