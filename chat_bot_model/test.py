import os
import requests
import time
import dotenv

dotenv.load_dotenv()

def main():
    input_path = "./test.txt"
    output_path = "./test_result.txt"
    url = "http://127.0.0.1:8000/chat"
    token = os.environ.get("CHAT_BOT_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for idx, line in enumerate(fin):
            question = line.strip()
            if not question:
                continue
            try:
                resp = requests.post(url, json={"input": question}, headers=headers)
                data = resp.json()
                answer = data.get("response", data)
            except Exception as e:
                answer = f"[ERROR] {e}"
            fout.write(f"Q{idx+1}: {question}\nA{idx+1}: {answer}\n\n")
            fout.flush()
            time.sleep(0.5)  # 防止请求过快

if __name__ == "__main__":
    main()
