from gen_ai import llm
from predict_disease import PredictDisease

def main():
    llm_ob = llm()
    chat, memory = llm_ob.chat()
    print(f" Previous memory is {memory.buffer_as_messages}")
    memory.clear()
    query = input("Enter Your Query: ")
    while query.lower() != "thanks":
        response = chat.predict(human_input=query)
        print("Response:", response)
        query = input("Enter Your Query: ")
    symp = llm_ob.classify_symptomps()
    cls = llm_ob.find_similar_symptom(user_symptom=symp)
    print(cls)
    disease_ob = PredictDisease(conditions=cls)
    disease = disease_ob.predictDisease()
    print(disease["final_prediction"])

if __name__=="__main__":
    main()