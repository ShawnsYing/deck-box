import re
import time
from colorama import Fore, Style, init

# 初始化colorama以支持跨平台彩色输出
init()

class TaskAnalyzer:
    @staticmethod
    def analyze_task(task_name, estimated_time):
        """分析任务是否过于复杂或模糊"""
        suggestions = []
        warnings = []
        
        # 检查任务时长是否过长
        if estimated_time > 60:
            warnings.append(f"⚠️  任务时长({estimated_time}分钟)过长，建议拆分为更小的任务")
            suggestions.extend(TaskAnalyzer._suggest_decomposition(task_name))
        
        # 检查任务描述是否模糊
        if TaskAnalyzer._is_vague(task_name):
            warnings.append("⚠️  任务描述可能过于模糊，建议更具体")
            suggestions.append("💡  建议添加具体的任务内容，例如：'完成项目文档'可以拆分为'编写项目概述'、'整理功能模块'等")
        
        # 检查任务是否包含多个动作
        if TaskAnalyzer._has_multiple_actions(task_name):
            warnings.append("⚠️  任务可能包含多个子任务，建议拆分")
            suggestions.extend(TaskAnalyzer._suggest_decomposition(task_name))
        
        return warnings, suggestions
    
    @staticmethod
    def _is_vague(task_name):
        """判断任务描述是否模糊"""
        vague_words = ["处理", "完成", "整理", "学习", "研究", "了解", "熟悉", "掌握"]
        # 如果任务仅由模糊词汇组成，没有具体内容
        task_name_lower = task_name.lower()
        return any(word in task_name_lower for word in vague_words) and len(task_name_lower) < 10
    
    @staticmethod
    def _has_multiple_actions(task_name):
        """判断任务是否包含多个动作"""
        # 查找中文动词短语
        action_pattern = r"[完成|编写|整理|学习|研究|了解|熟悉|掌握|创建|修改|更新|删除][^，,；;。.！!？?]*"
        actions = re.findall(action_pattern, task_name)
        return len(actions) >= 2
    
    @staticmethod
    def _suggest_decomposition(task_name):
        """根据任务名称建议拆分"""
        suggestions = []
        
        # 简单示例拆分建议
        if "文档" in task_name:
            suggestions.extend([
                "💡  建议拆分为：编写文档大纲",
                "💡  建议拆分为：完成文档内容",
                "💡  建议拆分为：审阅并修改文档"
            ])
        elif "代码" in task_name:
            suggestions.extend([
                "💡  建议拆分为：编写核心功能",
                "💡  建议拆分为：添加测试代码",
                "💡  建议拆分为：调试并修复bug"
            ])
        elif "学习" in task_name:
            suggestions.extend([
                "💡  建议拆分为：阅读相关资料",
                "💡  建议拆分为：实践示例代码",
                "💡  建议拆分为：总结学习笔记"
            ])
        else:
            suggestions.append("💡  建议根据任务的不同阶段进行拆分，每个子任务控制在15分钟以内")
        
        return suggestions

class VisualEffects:
    @staticmethod
    def show_gold_sparkles(level):
        """根据卡片级别显示金色闪光效果"""
        if level == 1:
            # 级别1，简单闪光
            VisualEffects._simple_sparkles()
        elif level == 2:
            # 级别2，中等闪光
            VisualEffects._medium_sparkles()
        elif level == 3:
            # 级别3，复杂闪光
            VisualEffects._complex_sparkles()
        else:
            # 级别4，高级闪光
            VisualEffects._advanced_sparkles()
    
    @staticmethod
    def _simple_sparkles():
        """简单的闪光效果"""
        sparkles = ["✨", "✨", "✨"]
        for sparkle in sparkles:
            print(f"{Fore.YELLOW}{sparkle}{Style.RESET_ALL}", end=" ")
            time.sleep(0.2)
        print()
    
    @staticmethod
    def _medium_sparkles():
        """中等的闪光效果"""
        sparkles = ["✨", "🌟", "✨", "🌟", "✨"]
        for sparkle in sparkles:
            print(f"{Fore.YELLOW}{sparkle}{Style.RESET_ALL}", end=" ")
            time.sleep(0.15)
        print()
    
    @staticmethod
    def _complex_sparkles():
        """复杂的闪光效果"""
        sparkles = ["✨", "🌟", "💫", "✨", "🌟", "💫", "✨"]
        for sparkle in sparkles:
            print(f"{Fore.YELLOW}{sparkle}{Style.RESET_ALL}", end=" ")
            time.sleep(0.1)
        print()
    
    @staticmethod
    def _advanced_sparkles():
        """高级的闪光效果"""
        print(f"{Fore.YELLOW}")
        for i in range(3):
            print("✨ 🌟 💫 ✨ 🌟 💫 ✨")
            time.sleep(0.1)
        print(f"{Style.RESET_ALL}")
    
    @staticmethod
    def show_witch_intro():
        """显示女巫占卜的intro效果"""
        intro = "🧙‍♀️  女巫正在进行占卜... 🧙‍♀️"
        for char in intro:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print()
        time.sleep(0.5)