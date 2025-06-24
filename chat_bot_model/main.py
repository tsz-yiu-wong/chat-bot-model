"""
主程序入口
"""
from modelscope import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers.utils.quantization_config import BitsAndBytesConfig

def load_model():
    """加载模型和tokenizer"""
    try:
        model_dir = './Qwen3-1.7B_quantized'  # 替换为你 snapshot_download 得到的路径
        
        print("正在加载tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
        
        print("正在加载模型...")

        # 新增：bnb 4bit 配置
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True,
        )
        
        return tokenizer, model
    except Exception as e:
        print(f"模型加载失败: {e}")
        return None, None

def generate_response(tokenizer, model, input_text, max_new_tokens=500):
    """生成回复"""
    try:
        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
        input_len = inputs['input_ids'].shape[1]
        outputs = model.generate(
            **inputs, 
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.2,
        )
        # 只decode新生成的部分
        response = tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)
        return response
    except Exception as e:
        print(f"生成失败: {e}")
        return None

def main():
    """主函数"""
    # 加载模型
    tokenizer, model = load_model()
    
    if tokenizer is None or model is None:
        print("模型加载失败，请检查模型路径和依赖包")
        exit(1)
    
    # 推理
    input_text = "嘿你好啊，今天怎么样？"
    print(f"输入: {input_text}")
    
    response = generate_response(tokenizer, model, input_text)
    if response:
        print(f"输出: {response}")
    else:
        print("生成失败")

if __name__ == "__main__":
    main() 