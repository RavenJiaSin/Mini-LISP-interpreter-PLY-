import os
import ply.yacc as yacc
from final_lex import tokens  
from final_yacc import parser, evaluate  

# 輸入資料夾路徑
INPUT_FOLDER = "public_test_data"

def process_lsp_files(folder_path):
    # 確保資料夾存在
    if not os.path.exists(folder_path):
        print(f"資料夾 {folder_path} 不存在！")
        return
    
    # 列出資料夾中的所有檔案
    files = [f for f in os.listdir(folder_path) if f.endswith('.lsp')]
    if not files:
        print(f"資料夾 {folder_path} 中沒有 .lsp 檔案！")
        return
    
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        print(f"\n處理檔案：{file_name}")
        
        try:
            # 讀取檔案內容
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
            # print(f"檔案內容:\n{data}")
            # 解析檔案內容
            results = parser.parse(data)
            if results is None:
                #print(f"檔案 {file_name} 解析失敗！")
                continue
            
            # 執行解析結果
            for result in results:
                # print(f"解析結果:\n{result}")
                # print("evaluate結果:")
                evaluate(result)
            
        except Exception as e:
            print(e)
        print("-" * 40)

# 執行批次處理
if __name__ == "__main__":
    process_lsp_files(INPUT_FOLDER)
