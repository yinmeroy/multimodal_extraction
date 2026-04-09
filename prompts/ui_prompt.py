"""UI界面场景Prompt模板"""

UI_FEW_SHOT = """示例1：
输入：[UI界面图片 - 登录页面]
输出：
{
    "page_title": "用户登录",
    "page_type": "登录页",
    "components": [
        {"component_type": "输入框", "text_content": "请输入用户名", "position": "顶部", "style_info": "圆角边框"},
        {"component_type": "按钮", "text_content": "登录", "position": "底部", "style_info": "蓝色主色调"}
    ],
    "layout_description": "垂直居中布局",
    "color_theme": "蓝白配色",
    "navigation_elements": ["返回首页链接"],
    "interactive_elements": ["登录按钮", "忘记密码链接"]
}
"""

UI_PROMPT = f"""你是一个专业的UI界面分析助手。请分析提供的UI界面图片，提取界面结构和组件信息。

要求：
1. 必须严格按照JSON Schema返回结果
2. 准确识别所有UI组件及其属性
3. 描述布局和交互元素
4. 如果某个字段信息不存在，使用null或空列表
5. 确保返回的是有效的JSON格式

{UI_FEW_SHOT}

请分析当前UI界面图片，返回JSON格式的结果：
"""
