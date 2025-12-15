import unittest
from datetime import datetime
from deck_box.models import Card, CardStatus, Mood, Quality

class TestCardModel(unittest.TestCase):
    def test_card_creation(self):
        """Test card creation"""
        card = Card("完成项目文档", 15, "work", "编写项目的技术文档")
        
        self.assertEqual(card.name, "完成项目文档")
        self.assertEqual(card.estimated_time, 15)
        self.assertEqual(card.tag, "work")
        self.assertEqual(card.description, "编写项目的技术文档")
        self.assertEqual(card.status, CardStatus.PENDING)
        self.assertIsNone(card.predecessor_id)
    
    def test_calculate_level(self):
        """Test card level calculation"""
        # Test level 1 (<=15 minutes)
        card1 = Card("简单任务", 10)
        self.assertEqual(card1.level, 1)
        
        # Test level 2 (16-30 minutes)
        card2 = Card("中等任务", 25)
        self.assertEqual(card2.level, 2)
        
        # Test level 3 (31-60 minutes)
        card3 = Card("复杂任务", 45)
        self.assertEqual(card3.level, 3)
        
        # Test level 4 (>60 minutes)
        card4 = Card("非常复杂的任务", 90)
        self.assertEqual(card4.level, 4)
    
    def test_complete_card(self):
        """Test card completion functionality"""
        card = Card("测试任务", 10)
        self.assertEqual(card.status, CardStatus.PENDING)
        self.assertIsNone(card.completed_at)
        self.assertIsNone(card.mood)
        self.assertIsNone(card.quality)
        
        # Mark card as completed
        card.complete(Mood.GOOD, 8, Quality.EXCELLENT)
        
        self.assertEqual(card.status, CardStatus.COMPLETED)
        self.assertIsInstance(card.completed_at, datetime)
        self.assertEqual(card.mood, Mood.GOOD)
        self.assertEqual(card.actual_time, 8)
        self.assertEqual(card.quality, Quality.EXCELLENT)
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        card = Card("测试任务", 10, "test", "测试描述")
        card_dict = card.to_dict()
        
        self.assertEqual(card_dict["name"], "测试任务")
        self.assertEqual(card_dict["estimated_time"], 10)
        self.assertEqual(card_dict["tag"], "test")
        self.assertEqual(card_dict["description"], "测试描述")
        self.assertEqual(card_dict["status"], "pending")
    
    def test_from_dict(self):
        """Test card creation from dictionary"""
        card_data = {
            "id": "test-id-123",
            "name": "测试任务",
            "description": "测试描述",
            "estimated_time": 15,
            "actual_time": 12,
            "tag": "work",
            "level": 1,
            "status": "completed",
            "created_at": "2023-01-01T10:00:00",
            "completed_at": "2023-01-01T10:12:00",
            "mood": "good",
            "quality": "excellent",
            "predecessor_id": None
        }
        
        card = Card.from_dict(card_data)
        
        self.assertEqual(card.id, "test-id-123")
        self.assertEqual(card.name, "测试任务")
        self.assertEqual(card.status, CardStatus.COMPLETED)
        self.assertEqual(card.mood, Mood.GOOD)
        self.assertEqual(card.quality, Quality.EXCELLENT)

if __name__ == '__main__':
    unittest.main()