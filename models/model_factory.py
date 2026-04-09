"""模型工厂 - 创建和管理模型实例"""
import base64
from openai import OpenAI
from typing import Dict, Any
from config import OPENAI_API_KEY, OPENAI_BASE_URL, TEMPERATURE, MAX_TOKENS


class OpenAICompatibleModel:
    """OpenAI兼容API的通用模型适配器
    
    支持所有通过OpenAI兼容接口调用的多模态模型，包括：
    - OpenAI官方模型: gpt-4o, gpt-4o-mini, gpt-4 等
    - 第三方中转模型: qwen-vl-max, qwen-vl-plus 等
    - 任何支持OpenAI API格式的模型
    """
    
    def __init__(self, api_key: str = OPENAI_API_KEY,
                 temperature: float = TEMPERATURE,
                 max_tokens: int = MAX_TOKENS,
                 model_version: str = "gpt-4o",
                 base_url: str = OPENAI_BASE_URL):
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model_version = model_version
        self.client = OpenAI(api_key=api_key, base_url=base_url)
    
    def extract(self, image_path: str, prompt: str) -> str:
        """使用多模态模型从图像中抽取信息"""
        print(f"🔧 [DEBUG] 开始调用API - 模型: {self.model_version}")
        print(f"🔧 [DEBUG] API Key前缀: {self.api_key[:10] if self.api_key else 'None'}...")
        print(f"🔧 [DEBUG] Base URL: {self.client.base_url}")
        
        try:
            with open(image_path, "rb") as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
            
            print(f"📤 [DEBUG] 发送请求到API...")
            response = self.client.chat.completions.create(
                model=self.model_version,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                            }
                        ]
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            content = response.choices[0].message.content
            print(f"✅ [DEBUG] API调用成功，返回内容长度: {len(content) if content else 0}")
            
            if not content or len(content.strip()) == 0:
                raise ValueError("API返回了空内容")
            
            return content
            
        except Exception as e:
            print(f"❌ [ERROR] API调用失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


class ModelFactory:
    """模型工厂类 - 简化版，直接使用通用适配器"""
    
    @classmethod
    def create_model(cls, model_name: str, **kwargs) -> OpenAICompatibleModel:
        """创建模型实例
        
        Args:
            model_name: 模型名称（如 gpt-4o, qwen-vl-max）
            **kwargs: 其他参数（temperature, max_tokens等）
            
        Returns:
            OpenAICompatibleModel 实例
        """
        model_name_lower = model_name.lower().strip()
        
        # 确保 model_version 参数正确传递
        if 'model_version' not in kwargs:
            kwargs['model_version'] = model_name_lower
        
        return OpenAICompatibleModel(**kwargs)
    
    @classmethod
    def list_available_models(cls) -> list:
        """列出预设的推荐模型"""
        return ["gpt-4o", "gpt-4o-mini"]