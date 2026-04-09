"""海报场景Prompt模板"""

POSTER_FEW_SHOT = """示例1：
输入：[海报图片 - Nike运动鞋促销海报]
输出：
{
    "title": "春季大促销",
    "brand": "Nike",
    "product_name": "Air Max运动鞋",
    "price": "￥599",
    "promotion_info": "买一送一，限时优惠",
    "key_features": ["透气舒适", "轻便耐用", "时尚设计"],
    "contact_info": "www.nike.com",
    "visual_elements": ["红色背景", "产品大图", "折扣标签"],
    "color_scheme": "红白黑配色"
}
"""

POSTER_PROMPT = f"""你是一个专业的海报信息抽取助手。请分析提供的海报图片，提取关键信息并以JSON格式返回。

要求：
1. 必须严格按照JSON Schema返回结果
2. 如果某个字段信息不存在，使用null或空列表
3. 保持简洁准确，不要添加额外解释
4. 确保返回的是有效的JSON格式

{POSTER_FEW_SHOT}

请分析当前海报图片，返回JSON格式的结果：
"""
