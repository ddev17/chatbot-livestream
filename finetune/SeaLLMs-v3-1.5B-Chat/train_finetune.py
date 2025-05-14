import os
import torch
import glob
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    GenerationConfig,
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from safetensors.torch import load_file, save_file

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Đường dẫn tới các tệp tin cần thiết
    model_dir = "finetune/SeaLLMs-v3-1.5B-Chat"  # Thư mục chứa config và trọng số
    config_path = f"{model_dir}/config.json"  # Đường dẫn tới config.json
    tokenizer_path = model_dir  # Thư mục chứa tokenizer
    train_data_path = "data/lora/clear_res_comment"  # Thư mục chứa dữ liệu huấn luyện

    # Kiểm tra sự tồn tại của các tệp tin và thư mục
    if not os.path.exists(config_path):
        print(f"Error: config.json not found at {config_path}")
        return
    if not os.path.exists(tokenizer_path):
        print(f"Error: Tokenizer directory not found at {tokenizer_path}")
        return
    if not os.path.isdir(train_data_path):
        print(f"Error: Training data directory not found at {train_data_path}")
        return

    # Kiểm tra các tệp tin JSONL trong thư mục dữ liệu huấn luyện
    jsonl_files = glob.glob(f"{train_data_path}/*.jsonl")
    if not jsonl_files:
        print(f"Error: No JSONL files found in {train_data_path}")
        return
    print(f"Found JSONL files: {jsonl_files}")

    # Tìm tất cả các tệp tin safetensors trong thư mục mô hình
    model_weights_paths = glob.glob(f"{model_dir}/*.safetensors")
    if not model_weights_paths:
        print(f"Error: No safetensors files found in {model_dir}")
        return
    print(f"Found safetensors files: {model_weights_paths}")

    # Tải cấu hình và khởi tạo mô hình
    config = AutoConfig.from_pretrained(config_path)
    model = AutoModelForCausalLM.from_config(config)
    model.config.tie_word_embeddings = True

    # Tải và hợp nhất trọng số từ các tệp tin safetensors
    if len(model_weights_paths) == 1:
        # Trường hợp chỉ có một tệp tin safetensors
        state_dict = load_file(model_weights_paths[0])
        
        print("Các khóa trong state_dict:", list(state_dict.keys()))
        model.load_state_dict(state_dict,strict=False)
        # if model.config.tie_word_embeddings:  # Lưu ý: có thể cần kiểm tra tên chính xác, ví dụ "tie_word embeddings"
        #     model.lm_head.weight = model.embed_tokens.weight
    else:
        # Trường hợp có nhiều tệp tin safetensors
        state_dict = {}
        for path in model_weights_paths:
            partial_state_dict = load_file(path)
            state_dict.update(partial_state_dict)
        model.load_state_dict(state_dict,strict=False)

    # Tải tokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Tải generation config (nếu có)
    try:
        gen_config = GenerationConfig.from_pretrained(model_dir)
        model.generation_config = gen_config
        print("Tải generation_config thành công.")
    except Exception as e:
        print("Không tải được generation_config.json, sử dụng cấu hình mặc định.", e)

    # Chuyển mô hình sang thiết bị và cấu hình huấn luyện
    model.to(device)
    model.config.use_cache = False
    model.gradient_checkpointing_enable()

    # Cấu hình LoRA
    lora_config = LoraConfig(
        r=32,
        lora_alpha=64,
        lora_dropout=0.05,
        bias="none",
        target_modules=["q_proj", "v_proj","o_proj","k_proj"],
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)
    print("LoRA config applied.")

    # Tải và xử lý dữ liệu huấn luyện (JSONL)
    dataset = load_dataset("json", data_files={"train": jsonl_files}, split="train", cache_dir="./cache")

    def preprocess_function(example):
        prompt = f"{example['system']}\nUser: {example['question']}\nAssistant: {example['response']}"
        tokenized = tokenizer(prompt, truncation=True, padding="max_length", max_length=512)
        labels = tokenized["input_ids"].copy()
        labels = [token if token != tokenizer.pad_token_id else -100 for token in labels]
        tokenized["labels"] = labels
        return tokenized

    tokenized_dataset = dataset.map(preprocess_function, batched=False)
    print("Batch size = 16")

    # Cấu hình tham số huấn luyện
    training_args = TrainingArguments(
        output_dir="./lora_finetuned_model_SeaLLMs-v3-1.5B-Chat",
        per_device_train_batch_size=16,
        num_train_epochs=10,
        learning_rate=1e-3,
        save_steps=1000,
        logging_steps=200,
        bf16=True,
        eval_strategy="no",
        gradient_accumulation_steps=1,
        remove_unused_columns=False
    )

    # Tạo Trainer và bắt đầu huấn luyện
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )
    trainer.train()

    # Lưu mô hình và tokenizer đã tinh chỉnh
    model.save_pretrained("./lora_finetuned_model_SeaLLMs-v3-1.5B-Chat", safe_serialization=True)
    tokenizer.save_pretrained("./lora_finetuned_model_SeaLLMs-v3-1.5B-Chat")
    save_file(model.state_dict(), "./lora_finetuned_model_SeaLLMs-v3-1.5B-Chat/model.safetensors")

    print("Huấn luyện hoàn tất và mô hình đã được lưu tại './lora_finetuned_model_SeaLLMs-v3-1.5B-Chat' dưới dạng safetensors.")

if __name__ == "__main__":
    main()