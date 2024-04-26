from initialize_llm import llm


def main():
    llm_ob = llm()
    chat = llm_ob.chat()
    query = input("Enter Your Query: ")
    while query.lower() != "thanks":
        response = chat.predict(human_input=query)
        print("Response:", response)
        query = input("Enter Your Query: ")
    symp = llm_ob.classify_symptomps()
    cls = llm_ob.find_similar_symptom(user_symptom=symp)
    print(cls)
    

if __name__=="__main__":
    main()