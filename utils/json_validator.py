"""JSON校验与修复工具"""
import json
import time
from typing import Dict, Any, Optional, Tuple
from json_repair import repair_json
from pydantic import ValidationError
from schemas import PosterExtractionResult, ChartExtractionResult, UIExtractionResult


class JsonValidator:
    """JSON校验与修复器"""
    
    SCHEMA_MAP = {
        "poster": PosterExtractionResult,
        "chart": ChartExtractionResult,
        "ui": UIExtractionResult
    }
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
    
    def validate_and_repair(self, json_str: str, scenario: str) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """验证并修复JSON字符串"""
        start_time = time.time()
        
        # 第1步：尝试直接解析
        try:
            data = json.loads(json_str)
            print("✓ JSON直接解析成功")
        except json.JSONDecodeError as e:
            print(f"⚠ JSON解析失败，尝试修复: {str(e)[:100]}")
            # 第2步：使用json-repair修复
            try:
                repaired_str = repair_json(json_str)
                data = json.loads(repaired_str)
                print("✓ JSON修复成功")
            except Exception as repair_error:
                error_msg = f"JSON修复失败: {str(repair_error)}"
                return False, {}, error_msg
        
        # 第3步：Pydantic校验
        try:
            schema_class = self.SCHEMA_MAP.get(scenario)
            if not schema_class:
                return False, {}, f"不支持的场景类型: {scenario}"
            
            validated_data = schema_class(**data)
            processing_time = time.time() - start_time
            print(f"✓ Pydantic校验成功 (耗时: {processing_time:.2f}s)")
            # 返回字典对象，供Gradio的gr.JSON组件使用
            return True, validated_data.model_dump(), None
            
        except ValidationError as ve:
            error_msg = f"Pydantic校验失败: {str(ve)}"
            return False, data, error_msg
        except Exception as e:
            error_msg = f"校验过程出错: {str(e)}"
            return False, data if data else {}, error_msg
    
    def extract_json_from_text(self, text: str) -> Optional[str]:
        """从文本中提取JSON字符串"""
        import re
        
        print(f"🔍 [DEBUG] 开始提取JSON，输入文本长度: {len(text)}")
        
        # 方法1: 匹配```
        # 使用`代替反引号避免编辑工具问题
        backtick = chr(96) * 3  # 三个反引号
        code_block_pattern = backtick + r'(?:json)?\s*([\s\S]*?)' + backtick
        matches = re.findall(code_block_pattern, text, re.IGNORECASE | re.DOTALL)
        if matches:
            json_str = matches[0].strip()
            print(f"✅ [DEBUG] 从代码块中提取到JSON，长度: {len(json_str)}")
            return json_str
        
        # 方法2: 查找花括号
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = text[start:end+1]
            print(f"✅ [DEBUG] 通过花括号提取JSON，长度: {len(json_str)}")
            return json_str
        
        # 方法3: 查找方括号
        start_arr = text.find("[")
        end_arr = text.rfind("]")
        if start_arr != -1 and end_arr != -1 and end_arr > start_arr:
            json_str = text[start_arr:end_arr+1]
            print(f"✅ [DEBUG] 通过方括号提取JSON数组，长度: {len(json_str)}")
            return json_str