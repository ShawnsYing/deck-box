import json
import os
from pathlib import Path
from .models import Card, DivinationResult

class Storage:
    """Storage management class, responsible for persistent storage of cards and divination results"""
    def __init__(self):
        # Get user home directory and create application data directory
        self.app_dir = Path.home() / ".deck_box"
        self.app_dir.mkdir(exist_ok=True)
        
        # Define data file paths
        self.cards_file = self.app_dir / "cards.json"
        self.divination_file = self.app_dir / "divination.json"
        
        # Initialize data files
        self._init_files()
    
    def _init_files(self):
        """Initialize data files"""
        if not self.cards_file.exists():
            with open(self.cards_file, "w", encoding="utf-8") as f:
                json.dump([], f)
        
        if not self.divination_file.exists():
            with open(self.divination_file, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    def save_cards(self, cards):
        """Save all cards to file"""
        cards_data = [card.to_dict() for card in cards]
        with open(self.cards_file, "w", encoding="utf-8") as f:
            json.dump(cards_data, f, ensure_ascii=False, indent=2)
    
    def load_cards(self):
        """Load all cards from file"""
        with open(self.cards_file, "r", encoding="utf-8") as f:
            cards_data = json.load(f)
        return [Card.from_dict(data) for data in cards_data]
    
    def add_card(self, card):
        """Add a new card"""
        cards = self.load_cards()
        cards.append(card)
        self.save_cards(cards)
    
    def get_card_by_id(self, card_id):
        """Get card by ID"""
        cards = self.load_cards()
        for card in cards:
            if card.id == card_id:
                return card
        return None
    
    def update_card(self, updated_card):
        """Update card information"""
        cards = self.load_cards()
        for i, card in enumerate(cards):
            if card.id == updated_card.id:
                cards[i] = updated_card
                self.save_cards(cards)
                return True
        return False
    
    def delete_card(self, card_id):
        """Delete card by ID"""
        cards = self.load_cards()
        original_length = len(cards)
        cards = [card for card in cards if card.id != card_id]
        if len(cards) < original_length:
            self.save_cards(cards)
            return True
        return False
    
    def save_divination(self, divination):
        """Save divination result"""
        divinations = self.load_divinations()
        divinations.append(divination)
        # Keep only the last 10 divination records
        if len(divinations) > 10:
            divinations = divinations[-10:]
        
        divinations_data = [d.to_dict() for d in divinations]
        with open(self.divination_file, "w", encoding="utf-8") as f:
            json.dump(divinations_data, f, ensure_ascii=False, indent=2)
    
    def load_divinations(self):
        """Load all divination results"""
        with open(self.divination_file, "r", encoding="utf-8") as f:
            divinations_data = json.load(f)
        return [DivinationResult.from_dict(data) for data in divinations_data]
    
    def get_last_divination(self):
        """Get the most recent divination result"""
        divinations = self.load_divinations()
        if divinations:
            return max(divinations, key=lambda d: d.created_at)
        return None