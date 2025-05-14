from model.LLMBotResCmt import LLMBotResCmt

Chatbot_Res_CMT = LLMBotResCmt()

# Function to handle the conversation
def chat_with_bot():
    print("Xin chào! Tôi là chatbot, hãy hỏi tôi điều gì đó (gõ 'quit' để thoát):")
    
    while True:
        user_input = input("Khách hàng trên livestream: ")
        
        if user_input.lower() == 'quit':
            print("Tạm biệt!")
            break
        
        response = Chatbot_Res_CMT.predict(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chat_with_bot()