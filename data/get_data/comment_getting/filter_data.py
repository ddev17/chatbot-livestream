def remove_duplicate_lines(lines):
    seen = set()
    unique = []
    for line in lines:
        if line not in seen:
            unique.append(line)
            seen.add(line)
    return unique

def remove_lines_containing_phrase(data, phrase):
    return [line for line in data if phrase not in line]

def read_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        return f.readlines()

def save_output(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(data)

if __name__ == "__main__":
    data = read_data("data/output.txt")
    data = remove_duplicate_lines(data)
    data = remove_lines_containing_phrase(data, "Vui lòng giới thiệu sản phẩm số")
    save_output(data, "../get_data_from_gemini/update1_clear_res.txt")
    print("Đã xóa tất cả các dòng chứa chuỗi 'Vui lòng giới thiệu sản phẩm số' khỏi file đầu vào.")
