
# Tạo môi trường 
python -m venv venv
# Bật môi trường 
source venv/bin/activate
# Cài đặt môi tường 
pip install -r requirements.txt 
# Để  finetune (sử dụng lora) 
    python ./finetune/SeaLLMs-v3-1.5B-Chat/train_finetune.py
# Để chạy 
python main.py