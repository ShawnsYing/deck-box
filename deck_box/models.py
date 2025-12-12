import uuid
from datetime import datetime
from enum import Enum

class CardStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Mood(Enum):
    AWESOME = "awesome"
    GOOD = "good"
    NEUTRAL = "neutral"
    BAD = "bad"
    TERRIBLE = "terrible"

class Quality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    MEDIUM = "medium"
    POOR = "poor"

class Card:
    def __init__(self, name, estimated_time, tag=None, description=None, predecessor_id=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.estimated_time = estimated_time
        self.actual_time = None
        self.tag = tag
        self.level = self._calculate_level()
        self.status = CardStatus.PENDING
        self.created_at = datetime.now()
        self.completed_at = None
        self.mood = None
        self.quality = None
        self.predecessor_id = predecessor_id

    def _calculate_level(self):
        """根据预计时间计算卡片级别"""
        if self.estimated_time <= 15:
            return 1
        elif self.estimated_time <= 30:
            return 2
        elif self.estimated_time <= 60:
            return 3
        else:
            return 4

    def complete(self, mood, actual_time, quality):
        """标记卡片为已完成"""
        self.status = CardStatus.COMPLETED
        self.completed_at = datetime.now()
        self.mood = mood
        self.actual_time = actual_time
        self.quality = quality

    def to_dict(self):
        """转换为字典格式以便存储"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "estimated_time": self.estimated_time,
            "actual_time": self.actual_time,
            "tag": self.tag,
            "level": self.level,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "mood": self.mood.value if self.mood else None,
            "quality": self.quality.value if self.quality else None,
            "predecessor_id": self.predecessor_id
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建Card实例"""
        card = cls(
            name=data["name"],
            estimated_time=data["estimated_time"],
            tag=data.get("tag"),
            description=data.get("description"),
            predecessor_id=data.get("predecessor_id")
        )
        card.id = data["id"]
        card.actual_time = data.get("actual_time")
        card.level = data["level"]
        card.status = CardStatus(data["status"])
        card.created_at = datetime.fromisoformat(data["created_at"])
        card.completed_at = datetime.fromisoformat(data["completed_at"]) if data["completed_at"] else None
        card.mood = Mood(data["mood"]) if data["mood"] else None
        card.quality = Quality(data["quality"]) if data["quality"] else None
        return card

class DivinationResult:
    def __init__(self, cards):
        self.id = str(uuid.uuid4())
        self.cards = cards
        self.total_time = sum(card.estimated_time for card in cards)
        self.created_at = datetime.now()

    def to_dict(self):
        """转换为字典格式以便存储"""
        return {
            "id": self.id,
            "cards": [card.to_dict() for card in self.cards],
            "total_time": self.total_time,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建DivinationResult实例"""
        cards = [Card.from_dict(card_data) for card_data in data["cards"]]
        result = cls(cards)
        result.id = data["id"]
        result.created_at = datetime.fromisoformat(data["created_at"])
        return result