import random
from .models import Card, CardStatus
from .storage import Storage

class Divination:
    def __init__(self):
        self.storage = Storage()
        # 定义不同级别的概率权重（级别越高，权重越低）
        self.level_weights = {
            1: 4,   # 15分钟以内，最高概率
            2: 3,   # 16-30分钟，较高概率
            3: 2,   # 31-60分钟，较低概率
            4: 1    # 60分钟以上，最低概率
        }
    
    def _get_available_cards(self):
        """获取所有可用的卡片（未完成且前置已完成）"""
        cards = self.storage.load_cards()
        available_cards = []
        
        for card in cards:
            if card.status != CardStatus.PENDING:
                continue
            
            # 检查前置卡片是否存在且已完成
            if card.predecessor_id:
                predecessor = self.storage.get_card_by_id(card.predecessor_id)
                if not predecessor or predecessor.status != CardStatus.COMPLETED:
                    continue
            
            available_cards.append(card)
        
        return available_cards
    
    def _select_card_by_probability(self, available_cards):
        """根据概率权重选择一张卡片"""
        if not available_cards:
            return None
        
        # 计算总权重
        total_weight = sum(self.level_weights[card.level] for card in available_cards)
        if total_weight == 0:
            return random.choice(available_cards)
        
        # 根据权重随机选择
        random_value = random.uniform(0, total_weight)
        current_weight = 0
        
        for card in available_cards:
            current_weight += self.level_weights[card.level]
            if random_value <= current_weight:
                return card
        
        # 防止计算误差
        return random.choice(available_cards)
    
    def perform_divination(self, min_time=90, max_time=150):
        """执行占卜，抽取总时间在指定范围内的卡片组合"""
        available_cards = self._get_available_cards()
        if not available_cards:
            return None
        
        # 如果只有一张卡片且时间在范围内，直接返回
        if len(available_cards) == 1:
            card = available_cards[0]
            if min_time <= card.estimated_time <= max_time:
                return [card]
            else:
                return None
        
        max_attempts = 1000
        best_combination = None
        best_time_diff = float('inf')
        
        for _ in range(max_attempts):
            # 随机选择卡片数量（1-5张）
            num_cards = random.randint(1, min(5, len(available_cards)))
            
            # 基于概率选择卡片
            selected_cards = []
            available_pool = available_cards.copy()
            total_time = 0
            
            for _ in range(num_cards):
                if not available_pool:
                    break
                    
                card = self._select_card_by_probability(available_pool)
                selected_cards.append(card)
                total_time += card.estimated_time
                available_pool.remove(card)
            
            # 检查总时间是否在范围内
            if min_time <= total_time <= max_time:
                return selected_cards
            
            # 如果不在范围内，记录最接近的组合
            if abs(total_time - (min_time + max_time) / 2) < best_time_diff:
                best_time_diff = abs(total_time - (min_time + max_time) / 2)
                best_combination = selected_cards
        
        # 如果没有找到完全匹配的组合，返回最接近的
        return best_combination
    
    def draw_single_card(self):
        """抽取一张卡片"""
        available_cards = self._get_available_cards()
        if not available_cards:
            return None
        
        return self._select_card_by_probability(available_cards)