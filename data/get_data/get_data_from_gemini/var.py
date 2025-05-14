def remove_blank_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if line.strip():  # Chỉ ghi lại những dòng không rỗng
                outfile.write(line)

    print(f"Đã loại bỏ các dòng trống. Kết quả lưu tại: {output_file}")

input_path = 'result.txt'   # Thay bằng đường dẫn tệp của bạn
output_path = '../../lora/clear_res_comment/cleaned_file.txt'  # Tạo file mới hoặc ghi đè file cũ nếu cần
remove_blank_lines(input_path, output_path)