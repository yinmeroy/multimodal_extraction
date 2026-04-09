"""Gradio主应用 - 多模态信息抽取平台"""
import gradio as gr
import tempfile
import os
from PIL import Image
import json
import time

from config import DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS
from models import ModelFactory
from utils import PromptRouter, JsonValidator

prompt_router = PromptRouter()
json_validator = JsonValidator()


def process_image(image, scenario, model_name, temperature, max_tokens):
    """处理上传的图片并进行信息抽取"""
    if image is None:
        return {}, '请上传图片'
    
    try:
        print(f"\n{'='*60}")
        print(f" 开始处理图片 - 场景: {scenario}, 模型: {model_name}")
        print(f"{'='*60}")
        
        if isinstance(image, Image.Image):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            image.save(temp_file.name, format='JPEG')
            image_path = temp_file.name
            print(f"💾 [DEBUG] 图片已保存到临时文件: {image_path}")
        else:
            image_path = image
            print(f"💾 [DEBUG] 使用已有文件路径: {image_path}")
        
        prompt = prompt_router.get_prompt(scenario)
        print(f"📝 [DEBUG] Prompt长度: {len(prompt)} 字符")
        
        model = ModelFactory.create_model(model_name, temperature=float(temperature), max_tokens=int(max_tokens))
        print(f"🤖 [DEBUG] 模型实例创建成功")
        
        start_time = time.time()
        raw_result = model.extract(image_path, prompt)
        processing_time = time.time() - start_time
        
        print(f"⏱️ [DEBUG] 处理耗时: {processing_time:.2f}秒")
        print(f"📄 [DEBUG] 原始返回内容前200字符: {raw_result[:200] if raw_result else 'EMPTY'}")
        
        if not raw_result or len(raw_result.strip()) == 0:
            raise ValueError("模型返回了空内容，请检查API密钥和网络连接")
        
        json_str = json_validator.extract_json_from_text(raw_result)
        if not json_str:
            print(f"⚠️ [DEBUG] 未找到JSON格式，使用原始内容")
            json_str = raw_result
        
        success, structured_result, error_msg = json_validator.validate_and_repair(json_str, scenario)
        
        print(f"📦 [DEBUG] validate_and_repair返回的structured_result类型: {type(structured_result)}")
        print(f"📦 [DEBUG] validate_and_repair返回的structured_result内容: {structured_result}")
        print(f"📦 [DEBUG] success状态: {success}")
        
        # 确保返回的是字典对象，且不为None或空
        if structured_result is None:
            structured_result = {}
        elif isinstance(structured_result, str):
            # 如果是字符串，尝试解析为字典
            try:
                structured_result = json.loads(structured_result)
                print(f"📦 [DEBUG] 已将JSON字符串转换为字典")
            except json.JSONDecodeError as e:
                print(f"⚠️ [DEBUG] JSON字符串解析失败: {e}，使用空字典")
                structured_result = {}
        
        if success:
            status = f'✅ 抽取成功！耗时: {processing_time:.2f}秒 | 模型: {model_name}'
        else:
            status = f'⚠️ 抽取完成但校验失败: {error_msg}'
        
        print(f"📦 [DEBUG] 最终返回structured_result类型: {type(structured_result)}")
        print(f"📦 [DEBUG] 最终返回structured_result内容: {structured_result}")
        
        # 安全地删除临时文件
        if isinstance(image, Image.Image) and os.path.exists(image_path):
            try:
                # 等待一小段时间确保文件不再被占用
                time.sleep(0.1)
                os.unlink(image_path)
                print(f"🗑️ [DEBUG] 临时文件已删除")
            except PermissionError as e:
                # 如果删除失败，记录日志但不影响主流程
                print(f"⚠️ [DEBUG] 临时文件删除失败（将被系统自动清理）: {e}")
            except Exception as e:
                print(f"⚠️ [DEBUG] 临时文件清理异常: {e}")
        
        return structured_result, status
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {}, f'处理失败: {str(e)}'


def create_interface():
    """创建Gradio界面"""
    with gr.Blocks() as demo:
        gr.Markdown('# 基于多模态大模型的结构化信息抽取平台\n支持海报、图表、UI界面等多种场景的智能信息抽取')
        
        with gr.Tabs():
            with gr.TabItem('信息抽取'):
                with gr.Row():
                    with gr.Column(scale=1):
                        image_input = gr.Image(type='pil', label='上传图片')
                        
                        with gr.Row():
                            scenario_dropdown = gr.Dropdown(choices=['poster', 'chart', 'ui'], value='poster', label='场景类型')
                        
                        with gr.Row():
                            model_dropdown = gr.Dropdown(
                                choices=ModelFactory.list_available_models(), 
                                value=DEFAULT_MODEL, 
                                label='选择模型',
                                allow_custom_value=True,
                                info='可从列表选择或手动输入任意模型（如：qwen-vl-max、gpt-4o、gpt-4等）'
                            )

                        with gr.Row():
                            temp_slider = gr.Slider(minimum=0, maximum=1, value=TEMPERATURE, step=0.1, label='Temperature')
                            max_tokens_input = gr.Number(value=MAX_TOKENS, label='Max Tokens', precision=0)
                        
                        extract_btn = gr.Button('开始抽取', variant='primary')
                    
                    with gr.Column(scale=1):
                        status_output = gr.Textbox(label='状态', lines=2)
                        structured_output = gr.JSON(label='结构化结果')
                
                extract_btn.click(fn=process_image, inputs=[image_input, scenario_dropdown, model_dropdown, temp_slider, max_tokens_input], outputs=[structured_output, status_output])
            
            with gr.TabItem('使用说明'):
                gr.Markdown("""
## 功能介绍

### 信息抽取
- 上传图片并选择场景类型（海报/图表/UI界面）
- 选择使用的模型（GPT-4o等）
- 调整温度和最大Token参数
- 查看结构化JSON结果

## 场景说明

### 海报场景 (poster)
提取：标题、品牌、价格、促销信息、核心卖点等

### 图表场景 (chart)
提取：图表类型、坐标轴、数据点、趋势分析等

### UI界面场景 (ui)
提取：页面标题、组件列表、布局描述、交互元素等

## API配置
使用前需要在 .env 文件中配置API密钥
""")
    
    return demo


if __name__ == '__main__':
    demo = create_interface()
    demo.launch(server_name='127.0.0.1', server_port=7860, share=False)
