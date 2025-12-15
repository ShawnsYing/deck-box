import random
from .models import Card, CardStatus
from .storage import Storage

class Divination:
    """Divination class, responsible for drawing cards from the deck box"""
    def __init__(self):
        """Initialize divination class"""
        self.storage = Storage()
        # Define probability weights for different levels (higher level has lower weight)
        self.level_weights = {
            1: 4,   # Within 15 minutes, highest probability
            2: 3,   # 16-30 minutes, higher probability
            3: 2,   # 31-60 minutes, lower probability
            4: 1    # Over 60 minutes, lowest probability
        }
    
    def _get_available_cards(self):
        """Get all available cards (pending and predecessors completed)"""
        cards = self.storage.load_cards()
        available_cards = []
        
        for card in cards:
            if card.status != CardStatus.PENDING:
                continue
            
            # Check if predecessor cards exist and are completed
            if card.predecessor_id:
                predecessor = self.storage.get_card_by_id(card.predecessor_id)
                if not predecessor or predecessor.status != CardStatus.COMPLETED:
                    continue
            
            available_cards.append(card)
        
        return available_cards
    
    def _select_card_by_probability(self, available_cards):
        """Select a card based on probability weights"""
        if not available_cards:
            return None
        
        # Calculate total weight
        total_weight = sum(self.level_weights[card.level] for card in available_cards)
        if total_weight == 0:
            return random.choice(available_cards)
        
        # Select randomly based on weights
        random_value = random.uniform(0, total_weight)
        current_weight = 0
        
        for card in available_cards:
            current_weight += self.level_weights[card.level]
            if random_value <= current_weight:
                return card
        
        # Prevent calculation errors
        return random.choice(available_cards)
    
    def perform_divination(self, min_time=90, max_time=150):
        """Perform divination to draw a combination of cards within specified time range"""
        available_cards = self._get_available_cards()
        if not available_cards:
            return None
        
        # If only one card and time is within range, return directly
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
            # Randomly select number of cards (1-5)
            num_cards = random.randint(1, min(5, len(available_cards)))
            
            # Select cards based on probability
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
            
            # Check if total time is within range
            if min_time <= total_time <= max_time:
                return selected_cards
            
            # If not in range, record the closest combination
            if abs(total_time - (min_time + max_time) / 2) < best_time_diff:
                best_time_diff = abs(total_time - (min_time + max_time) / 2)
                best_combination = selected_cards
        
        # If no exact matching combination found, return the closest one
        return best_combination
    
    def draw_single_card(self):
        """Draw a single card"""
        available_cards = self._get_available_cards()
        if not available_cards:
            return None
        
        return self._select_card_by_probability(available_cards)