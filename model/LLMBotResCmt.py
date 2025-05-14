import os
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
model_path = "SeaLLMs/SeaLLMs-v3-1.5B-Chat"


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
device = "cuda" if torch.cuda.is_available() else "cpu"
ADAPTER_PATH = os.path.join(PROJECT_ROOT, "checkpoint/checkpoint-3484-sea1.5")
context_prompt =  "Bạn đang tư vấn về sản phẩm trong một buổi livestream bàn hàng online trên sàn thương mại điện tử Shopee"

class LLMBotResCmt:
    def __init__(self):
        self.base_model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )

        print("Đang tải Adapter LoRA từ:", ADAPTER_PATH)
        self.model = PeftModel.from_pretrained(self.base_model, ADAPTER_PATH)

        self.model.eval().to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.generation_config = {
            "max_new_tokens": 64,
            "temperature": 0.7    ,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
            "do_sample": True
        }
        self.history_conversation = []
        
        self.system_prompt = "You are AI chatbot for support customer store in livestream Shopee. Sử  dụng tiếng việt. Shop của bạn chỉ hoạt động ở nền tảng shoppe. Phản hồi không có tên hay sự có mặt của các nền tảng khác. Shop không bán các mặt hàng bị cấm theo chính sách của shoppe và các sản phẩm vi phạm pháp luật như chất cấm hay các sản phẩm nhập lậu. Shop không bán hàng giả hàng kém chất lượng "
        self.history_conversation.append({"role": "system", "content": self.system_prompt})
        self.count = 1
        self.period = 1


    def format_conversation(self, messages):
        return self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

    def generate_response(self, messages):
        formatted_text = self.format_conversation(messages)
        inputs = self.tokenizer(formatted_text, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.generation_config["max_new_tokens"],
                temperature=self.generation_config["temperature"],
                top_p=self.generation_config["top_p"],
                repetition_penalty=self.generation_config["repetition_penalty"],
                do_sample=self.generation_config["do_sample"]
            )

        response_start = inputs.input_ids.shape[-1]
        response = self.tokenizer.decode(
            outputs[0][response_start:],
            skip_special_tokens=True
        )
        return response.strip()


    
    def predict(self, prompt):
        self.count += 1
        if self.count % self.period == 0:
            self.history_conversation = []
            self.history_conversation.append({"role": "system", "content": self.system_prompt})
        self.history_conversation.append({"role": "user", "content": prompt})
        response = self.generate_response(self.history_conversation)
        # self.history_conversation.append({"role": "assistant", "content": response})
        conversation_data = {
            "system": context_prompt,
            "question": prompt,
            "response": response
        }
        
        try:

            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reply_comment.jsonl")
            
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(conversation_data, ensure_ascii=False) + "\n")
                print(f"Write conversation log successfully to {file_path}")
        except IOError as e:
            self.logger.error(f"Failed to write conversation log: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error when writing conversation log: {str(e)}")
        return response









