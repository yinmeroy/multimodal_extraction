# 基于多模态大模型的结构化信息抽取平台

## 📖 项目简介

这是一个基于多模态大模型（GPT-4o、Qwen-VL等）的智能信息抽取平台，支持从图片中自动提取结构化数据。系统支持通过OpenAI兼容API调用任意多模态模型，提供海报、图表、UI界面等多种场景的智能化信息抽取能力，并配备友好的Gradio Web交互界面。

### ✨ 核心特性

- 🎯 **多场景支持**: 海报、图表、UI界面三大场景的场景化Prompt路由
- 🤖 **多模型接入**: 支持任意OpenAI兼容API的多模态模型（GPT-4o、Qwen-VL-Max等），支持用户自定义输入模型名称
- ✅ **高可靠性**: Few-Shot示例 + JSON Schema约束 + json-repair + Pydantic双重校验
- 🎨 **友好界面**: Gradio交互式Web界面，支持参数实时调节和可视化结果展示
- 🌐 **API兼容**: 支持OpenAI官方API和任意OpenAI兼容的中转API
- 🔧 **简洁架构**: 通用适配器模式，代码清晰易维护

## 🚀 快速开始

### 前置要求

- **Python**: 3.10 或更高版本
- **API密钥**: OpenAI API密钥或兼容的第三方API密钥
- **网络**: 稳定的互联网连接以调用多模态大模型API

### 1. 安装依赖

```bash
# 克隆项目（如果尚未克隆）
cd multimodal_extraction

# 推荐创建虚拟环境
conda create -n multimodal_env python=3.10
conda activate multimodal_env

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 复制配置文件模板
cp .env.example .env

# 编辑.env文件，填写你的API密钥和API地址
```

**配置文件示例（.env）：**

```env
# 使用OpenAI官方API或使用中转API（推荐，支持更多模型）
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. 启动应用

```bash
python app.py
```

启动成功后，终端会显示：

```
Running on http://127.0.0.1:7860
```

在浏览器中访问：**http://127.0.0.1:7860**

## 📸 功能演示

### 支持的场景类型

#### 1️⃣ 海报场景 (poster)
- **提取内容**: 标题、品牌、价格、促销信息、核心卖点等
- **适用场景**: 电商海报、广告图片、宣传物料

#### 2️⃣ 图表场景 (chart)
- **提取内容**: 图表类型、坐标轴标签、数据点、趋势分析、关键洞察
- **适用场景**: 折线图、柱状图、饼图、散点图等数据可视化图表

#### 3️⃣ UI界面场景 (ui)
- **提取内容**: 页面标题、组件列表、布局描述、交互元素、颜色方案
- **适用场景**: 网页截图、App界面、设计稿

### 使用步骤

1. **上传图片**: 点击"上传图片"按钮选择图片文件（支持JPG、PNG格式）
2. **选择场景**: 从下拉框选择对应的场景类型（poster/chart/ui）
3. **选择模型**: 
   - 从预设列表选择：`gpt-4o`、`gpt-4o-mini`
   - 或手动输入任意模型名称，如：`qwen-vl-max`、`gpt-4`、`gpt-4-turbo`
4. **调整参数**（可选）:
   - **Temperature**: 控制输出随机性（0-1，推荐0.1以保证一致性）
   - **Max Tokens**: 限制最大输出长度（默认2000）
5. **开始抽取**: 点击"开始抽取"按钮，等待处理完成
6. **查看结果**: 在"结构化结果"区域查看提取的JSON数据

## 🏗️ 项目架构

```
multimodal_extraction/
├── app.py                      # Gradio主应用入口
├── config.py                   # 全局配置管理（API密钥、默认参数）
├── requirements.txt            # Python依赖列表
├── .env.example                # 环境变量配置模板
│
├── models/                     # 模型层
│   ├── __init__.py             # 模块导出
│   └── model_factory.py        # 模型工厂 + 通用OpenAI兼容适配器
│
├── prompts/                    # 场景化Prompt模板
│   ├── __init__.py
│   ├── poster_prompt.py        # 海报场景Prompt（含Few-Shot示例）
│   ├── chart_prompt.py         # 图表场景Prompt（含Few-Shot示例）
│   └── ui_prompt.py            # UI场景Prompt（含Few-Shot示例）
│
├── schemas/                    # Pydantic数据模型
│   ├── __init__.py
│   └── extraction_schema.py    # 所有场景的数据结构定义
│
└── utils/                      # 工具类
    ├── __init__.py
    ├── prompt_router.py        # Prompt路由器（根据场景选择Prompt）
    └── json_validator.py       # JSON提取、校验与修复器
```

### 核心组件说明

#### 1. 模型工厂 ([model_factory.py](models/model_factory.py))

**OpenAICompatibleModel** - 通用OpenAI兼容适配器
- 支持所有通过OpenAI兼容接口调用的多模态模型
- 自动处理图片base64编码和API调用
- 通过[ModelFactory.create_model()](models/model_factory.py)统一创建

```python
# 使用预设模型
model = ModelFactory.create_model("gpt-4o")

# 使用自定义模型
model = ModelFactory.create_model("qwen-vl-max")
```

#### 2. Prompt路由 ([prompt_router.py](utils/prompt_router.py))

根据场景类型自动选择对应的Prompt模板：

```python
prompt = prompt_router.get_prompt("chart")  # 返回图表专用Prompt
```

#### 3. JSON校验 ([json_validator.py](utils/json_validator.py))

三重保障确保JSON格式正确：
1. **正则提取**: 从模型返回文本中提取JSON内容
2. **json-repair**: 自动修复常见格式错误
3. **Pydantic校验**: 强类型数据结构验证

## 🔧 配置说明

### 环境变量配置 (.env)

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `OPENAI_API_KEY` | API密钥 | `sk-xxxxx` |
| `OPENAI_BASE_URL` | API基础地址 | `https://api.openai.com/v1` |

### 代码配置 (config.py)

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `DEFAULT_MODEL` | `gpt-4o` | 默认使用的模型 |
| `TEMPERATURE` | `0.1` | 输出随机性（0-1） |
| `MAX_TOKENS` | `2000` | 最大输出长度 |

## 🤖 支持的模型

### 工作原理

项目使用**通用OpenAI兼容适配器**，只要你的API支持OpenAI的聊天接口格式，就可以使用任意模型名称。


##  数据结构示例

### 海报抽取结果

```json
{
  "title": "春季大促销",
  "brand": "Nike",
  "product_name": "Air Max 2024",
  "price": "¥899",
  "promotion_info": "满500减100",
  "key_features": ["透气网面", "缓震科技", "时尚设计"],
  "visual_elements": ["运动鞋特写", "春季花卉背景"],
  "color_scheme": "蓝色+白色+粉色"
}
```

### 图表抽取结果

```json
{
  "chart_type": "折线图",
  "title": "2023年销售额趋势",
  "x_axis_label": "月份",
  "y_axis_label": "销售额（万元）",
  "data_points": [
    {"label": "1月", "value": 120.5, "unit": "万元"},
    {"label": "2月", "value": 135.2, "unit": "万元"}
  ],
  "trend_description": "整体呈上升趋势",
  "key_insights": ["Q2增长最快", "12月达到峰值"],
  "time_range": "2023年1月-12月"
}
```

### UI界面抽取结果

```json
{
  "page_title": "用户中心",
  "page_type": "个人中心页",
  "components": [
    {"component_type": "头像", "text_content": null, "position": "顶部居中"},
    {"component_type": "按钮", "text_content": "编辑资料", "position": "头像下方"}
  ],
  "layout_description": "垂直居中布局",
  "color_theme": "白色背景+蓝色主题色",
  "navigation_elements": ["返回按钮", "设置图标"],
  "interactive_elements": ["编辑资料按钮", "退出登录按钮"]
}
```


