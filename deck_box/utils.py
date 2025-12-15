import re
import time
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init()

class TaskAnalyzer:
    @staticmethod
    def analyze_task(task_name, estimated_time):
        """Analyze if task is too complex or vague"""
        suggestions = []
        warnings = []
        
        # Check if task duration is too long
        if estimated_time > 60:
            warnings.append(f"⚠️  任务时长({estimated_time}分钟)过长，建议拆分为更小的任务")
            suggestions.extend(TaskAnalyzer._suggest_decomposition(task_name))
        
        # Check if task description is vague
        if TaskAnalyzer._is_vague(task_name):
            warnings.append("⚠️  任务描述可能过于模糊，建议更具体")
            suggestions.append("💡  建议添加具体的任务内容，例如：'完成项目文档'可以拆分为'编写项目概述'、'整理功能模块'等")
        
        # Check if task contains multiple actions
        if TaskAnalyzer._has_multiple_actions(task_name):
            warnings.append("⚠️  任务可能包含多个子任务，建议拆分")
            suggestions.extend(TaskAnalyzer._suggest_decomposition(task_name))
        
        return warnings, suggestions
    
    @staticmethod
    def _is_vague(task_name):
        """Determine if task description is vague"""
        vague_words = ["处理", "完成", "整理", "学习", "研究", "了解", "熟悉", "掌握"]
        # If the task consists only of vague words without specific content
        task_name_lower = task_name.lower()
        return any(word in task_name_lower for word in vague_words) and len(task_name_lower) < 10
    
    @staticmethod
    def _has_multiple_actions(task_name):
        """Determine if task contains multiple actions"""
        # Find Chinese verb phrases
        action_pattern = r"[完成|编写|整理|学习|研究|了解|熟悉|掌握|创建|修改|更新|删除][^，,；;。.！!？?]*"
        actions = re.findall(action_pattern, task_name)
        return len(actions) >= 2
    
    @staticmethod
    def _suggest_decomposition(task_name):
        """Suggest decomposition based on task name"""
        suggestions = []
        
        # Simple example decomposition suggestion
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
        """Show gold sparkle effect based on card level"""
        if level == 1:
            # Level 1, simple sparkles
            VisualEffects._simple_sparkles()
        elif level == 2:
            # Level 2, medium sparkles
            VisualEffects._medium_sparkles()
        elif level == 3:
            # Level 3, complex sparkles
            VisualEffects._complex_sparkles()
        else:
            # Level 4, advanced sparkles
            VisualEffects._advanced_sparkles()
    
    @staticmethod
    def _simple_sparkles():
        """Simple sparkle effect"""
        sparkles = ["✨", "✨", "✨"]
        for sparkle in sparkles:
            print(f"{Fore.YELLOW}{sparkle}{Style.RESET_ALL}", end=" ")
            time.sleep(0.2)
        print()
    
    @staticmethod
    def _medium_sparkles():
        """Medium sparkle effect"""
        sparkles = ["✨", "🌟", "✨", "🌟", "✨"]
        for sparkle in sparkles:
            print(f"{Fore.YELLOW}{sparkle}{Style.RESET_ALL}", end=" ")
            time.sleep(0.15)
        print()
    
    @staticmethod
    def _complex_sparkles():
        """Complex sparkle effect"""
        sparkles = ["✨", "🌟", "💫", "✨", "🌟", "💫", "✨"]
        for sparkle in sparkles:
            print(f"{Fore.YELLOW}{sparkle}{Style.RESET_ALL}", end=" ")
            time.sleep(0.1)
        print()
    
    @staticmethod
    def _advanced_sparkles():
        """Advanced sparkle effect"""
        print(f"{Fore.YELLOW}")
        for i in range(3):
            print("✨ 🌟 💫 ✨ 🌟 💫 ✨")
            time.sleep(0.1)
        print(f"{Style.RESET_ALL}")
    
    @staticmethod
    def show_witch_intro():
        """Show witch divination intro effect"""
        intro = "🧙‍♀️  女巫正在进行占卜... 🧙‍♀️"
        for char in intro:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print()
        time.sleep(0.5)