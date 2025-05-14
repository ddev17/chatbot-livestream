import os
from time import sleep
import re
import google.generativeai as genai
from dotenv import  load_dotenv
load_dotenv()
# genai.configure(api_key=os.environ["AIzaSyDPWvPiLYeQvKcJrc68pULjrv7Z33D-R2w"])

key = input("Key: ").strip()
print(key)
genai.configure(api_key=key)

input_path = input("INPUT PATH: ").strip()


instructions = (
    "Đọc kỹ  các câu hỏi ở bên dưới và thực hiện đúng và kỹ  với các quy tắc sau:\n"
    "1. Ngữ cảnh: Bạn đang trả lời comment về sản phẩm trong một buổi livestream bán hàng online trên sàn thương mại điện tử Shopee\n"
    "2. Viết lại cho đúng chính tả các câu hỏi và viết câu trả lời, câu trả lời ở dạng chung chung sao cho tất cả các shop với nhiều mặt hàng có thể trả lời được\n"
    '3. Phản hồi bằng file jsonl có cấu trúc như sau: \n{"system": "Bạn đang trả lời comment về sản phẩm trong một buổi livestream bàn hàng online trên sàn thương mại điện tử Shopee", "question": "Nam m7,70kg size j b", "response": "Dạ, với chiều cao 1m7 và cân nặng 70kg, bạn mặc size L hoặc XL là vừa đẹp đó ạ. Bạn thích mặc thoải mái hay vừa người hơn để shop tư vấn kỹ hơn nha?"}\n'
    "4. Nếu có các câu hỏi về kích thước, kích cỡ mà có thông tin khá đầy đủ thì có thể trả lời chính xác kích thước, kích cỡ phù hợp\n"
    "5. Các câu hỏi về voucher thì trả lời với ý là shop có nhiều voucher cần vào trang chủ để biết thêm chi tiết\n"
    "6. Các câu hỏi về tư vấn thì trả lời ngắn gọn\n"
    "7. Các câu chào hỏi thì trả lời ngắn gọn và tình cảm\n"
    "8. Các câu hỏi về số lượng hàng thì bảo check số lượng ở giỏ hàng hoặc nhắn tin trực tiếp để biết thêm chi tiết\n"
    "9. Các câu hỏi về kiểm tra tin nhắn hay kiểm tra đơn hàng thì sẽ trả lời với ý là shop sẽ nhắn tin cho bạn ngay\n"
    "10. Các câu hỏi về còn hàng hay không hoặc số lượng hàng thì luôn trả lời là còn hàng\n"
    "11. Các câu hỏi yêu cầu lên mã hoặc xem sản phẩm thì trả lời với ý là sản phẩm sẽ lên ngay cho khách hàng\n"
    "đây là các câu hỏi\n"
)

def read_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines, len(lines)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain"
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp-01-21",
    generation_config=generation_config
)

chat_session = model.start_chat(history=[])

data, line_count = read_data(input_path)
chunk_size = 50
epochs = (line_count + chunk_size - 1) // chunk_size
output_path = "result.txt"

with open(output_path, "a", encoding="utf-8") as out_file:
    for i in range(epochs):
        print("LOADING:", i)
        chunk = data[i * chunk_size : (i + 1) * chunk_size]
        message = instructions + "".join(chunk)
        try:
            response = chat_session.send_message(message)
            cleaned_response = re.sub(r'```jsonl|```', '', response.text).strip()

            out_file.write(cleaned_response + "\n\n")
            print(cleaned_response)
        except Exception as e:
            out_file.write(f"Lỗi chunk {i}: {str(e)}\n\n")
            print(f"Lỗi chunk {i}: {str(e)}")

        print("COMPLETE", i)
        sleep(10)
