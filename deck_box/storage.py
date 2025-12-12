import json
import os
from pathlib import Path
from .models import Card, DivinationResult

class Storage:
    def __init__(self):
        # 获取用户主目录，创建应用数据目录
        self.app_dir = Path.home() / ".deck_box"
        self.app_dir.mkdir(exist_ok=True)
        
        # 定义数据文件路径
        self.cards_file = self.app_dir / "cards.json"
        self.divination_file = self.app_dir / "divination.json"
        
        # 初始化数据文件
        self._init_files()
    
    def _init_files(self):
        """初始化数据文件"""
        if not self.cards_file.exists():
            with open(self.cards_file, "w", encoding="utf-8") as f:
                json.dump([], f)
        
        if not self.divination_file.exists():
            with open(self.divination_file, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    def save_cards(self, cards):
        """保存所有卡片到文件"""
        cards_data = [card.to_dict() for card in cards]
        with open(self.cards_file, "w", encoding="utf-8") as f:
            json.dump(cards_data, f, ensure_ascii=False, indent=2)
    
    def load_cards(self):
        """从文件加载所有卡片"""
        with open(self.cards_file, "r", encoding="utf-8") as f:
            cards_data = json.load(f)
        return [Card.from_dict(data) for data in cards_data]
    
    def add_card(self, card):
        """添加一张新卡片"""
        cards = self.load_cards()
        cards.append(card)
        self.save_cards(cards)
    
    def get_card_by_id(self, card_id):
        """根据ID获取卡片"""
        cards = self.load_cards()
        for card in cards:
            if card.id == card_id:
                return card
        return None
    
    def update_card(self, updated_card):
        """更新卡片信息"""
        cards = self.load_cards()
        for i, card in enumerate(cards):
            if card.id == updated_card.id:
                cards[i] = updated_card
                self.save_cards(cards)
                return True
        return False
    
    def save_divination(self, divination):
        """保存占卜结果"""
        divinations = self.load_divinations()
        divinations.append(divination)
        # 只保留最近10次占卜记录
        if len(divinations) > 10:
            divinations = divinations[-10:]
        
        divinations_data = [d.to_dict() for d in divinations]
        with open(self.divination_file, "w", encoding="utf-8") as f:
            json.dump(divinations_data, f, ensure_ascii=False, indent=2)
    
    def load_divinations(self):
        """加载所有占卜结果"""
        with open(self.divination_file, "r", encoding="utf-8") as f:
            divinations_data = json.load(f)
        return [DivinationResult.from_dict(data) for data in divinations_data]
    
    def get_last_divination(self):
        """获取最近一次的占卜结果"""
        divinations = self.load_divinations()
        if divinations:
            return max(divinations, key=lambda d: d.created_at)
        return None