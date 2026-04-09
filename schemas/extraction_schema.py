"""Pydantic数据模型 - 定义结构化抽取结果的Schema"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PosterExtractionResult(BaseModel):
    """海报信息抽取结果"""
    title: str = Field(..., description='海报标题')
    brand: Optional[str] = Field(None, description='品牌名称')
    product_name: Optional[str] = Field(None, description='产品名称')
    price: Optional[str] = Field(None, description='价格信息')
    promotion_info: Optional[str] = Field(None, description='促销信息')
    key_features: List[str] = Field(default_factory=list, description='核心卖点')
    contact_info: Optional[str] = Field(None, description='联系方式')
    visual_elements: List[str] = Field(default_factory=list, description='视觉元素描述')
    color_scheme: Optional[str] = Field(None, description='配色方案')


class ChartDataPoint(BaseModel):
    """图表数据点"""
    label: str = Field(..., description='数据点标签')
    value: float = Field(..., description='数值')
    unit: Optional[str] = Field(None, description='单位')


class ChartExtractionResult(BaseModel):
    """图表信息抽取结果"""
    chart_type: str = Field(..., description='图表类型')
    title: Optional[str] = Field(None, description='图表标题')
    x_axis_label: Optional[str] = Field(None, description='X轴标签')
    y_axis_label: Optional[str] = Field(None, description='Y轴标签')
    data_points: List[ChartDataPoint] = Field(default_factory=list, description='数据点列表')
    trend_description: Optional[str] = Field(None, description='趋势描述')
    key_insights: List[str] = Field(default_factory=list, description='关键洞察')
    time_range: Optional[str] = Field(None, description='时间范围')


class UIComponent(BaseModel):
    """UI组件"""
    component_type: str = Field(..., description='组件类型')
    text_content: Optional[str] = Field(None, description='文本内容')
    position: Optional[str] = Field(None, description='位置描述')
    style_info: Optional[str] = Field(None, description='样式信息')


class UIExtractionResult(BaseModel):
    """UI界面信息抽取结果"""
    page_title: Optional[str] = Field(None, description='页面标题')
    page_type: Optional[str] = Field(None, description='页面类型')
    components: List[UIComponent] = Field(default_factory=list, description='UI组件列表')
    layout_description: Optional[str] = Field(None, description='布局描述')
    color_theme: Optional[str] = Field(None, description='色彩主题')
    navigation_elements: List[str] = Field(default_factory=list, description='导航元素')
    interactive_elements: List[str] = Field(default_factory=list, description='交互元素')


class ExtractionResponse(BaseModel):
    """通用抽取响应"""
    success: bool = Field(..., description='是否成功')
    scenario: str = Field(..., description='场景类型')
    model_used: str = Field(..., description='使用的模型')
    result: Optional[Dict[str, Any]] = Field(None, description='抽取结果')
    error_message: Optional[str] = Field(None, description='错误信息')
    confidence: Optional[float] = Field(None, description='置信度')
    processing_time: Optional[float] = Field(None, description='处理时间（秒）')
