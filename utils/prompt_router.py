"""Prompt路由器 - 根据场景自动选择对应的Prompt模板"""
from typing import Dict
from prompts import POSTER_PROMPT, CHART_PROMPT, UI_PROMPT


class PromptRouter:
    """Prompt路由器"""
    
    def __init__(self):
        self.prompt_templates: Dict[str, str] = {
            "poster": POSTER_PROMPT,
            "chart": CHART_PROMPT,
            "ui": UI_PROMPT
        }
    
    def get_prompt(self, scenario: str) -> str:
        """根据场景获取对应的Prompt"""
        scenario_lower = scenario.lower()
        if scenario_lower not in self.prompt_templates:
            raise ValueError(f"不支持的场景类型: {scenario}。支持的场景: {list(self.prompt_templates.keys())}")
        return self.prompt_templates[scenario_lower]
    
    def list_scenarios(self) -> list:
        """列出所有支持的场景"""
        return list(self.prompt_templates.keys())
