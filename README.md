I struggle with severe executive dysfunction and procrastination. I often overestimate my emotional capacity, assigning myself too many tasks, and feel extremely frustrated when I can't complete them. Traditional task management tools often don't solve this problem - instead, the overwhelming display of tasks fills me with dread.

That's why I created this card drawing "game" - to help myself complete work step by step, making task management fun and less intimidating.

# 🎴 Deck Box

A unique card-based task management tool that transforms your to-do list into an engaging card game experience! 🎮✨

Deck Box helps you break down large, overwhelming tasks into smaller, manageable "cards" and uses a divination (card drawing) mechanism to select tasks for you, making task management fun and motivating.

## ✨ Key Features

### 📝 Add Cards

Create task cards with detailed information:

- **Task Content**: Clear description of what needs to be done
- **Time Estimate**: Expected duration in minutes
- **Tags**: Categorize tasks (work, personal, study, etc.)
- **Dependencies**: Link cards to track prerequisite tasks

### 🔧 Manage Cards

Update or remove cards as your tasks evolve:

- **Modify Cards**: Update task content, dependencies, or completion status
- **Clear Dependencies**: Remove prerequisite links when needed
- **Delete Cards**: Permanently remove cards with confirmation prompt
- **Status Management**: Mark cards as completed or not completed

### 🔮 Divination (Card Drawing)

- Randomly draws cards with total execution time between **1.5h~2.5h** by default
- Customizable time range: Set your own minimum and maximum total time
- Single card drawing option available
- **Smart Probability System**: Longer tasks have lower chance of being drawn

### 📊 Track Progress

- Mark cards as completed with:
  - **Mood**: How you felt while completing the task (good, neutral, bad)
  - **Actual Duration**: Real time spent on the task
  - **Quality Rating**: How well the task was completed (excellent, good, fair, poor)

### 🧠 Task Analysis

- **Automatic Analysis**: Detects if tasks are too vague or complex
- **Decomposition Suggestions**: Provides recommendations on how to break down large tasks
- **Encouragement System**: Motivates you to create short, focused cards

## 🚀 Installation

### Development Installation

```bash
# Using uv (recommended for development)
uv sync
```

### Regular Installation

```bash
# Install from source (editable mode)
pip install -e .
```

## 🎮 Usage

### Add a Card

```bash
# Basic card with name and time
deck-box add --name "Write project report" --time 15 --tag work

# Card with dependency
deck-box add --name "Review project report" --time 10 --tag work --predecessor <card_id>
```

**Parameters:**

- `--name`: Card name/description (required)
- `--time`: Time estimate in minutes (required)
- `--tag`: Optional tag for categorization
- `--predecessor`: Optional ID of prerequisite card

### Divination (Draw Cards)

```bash
# Default divination (total time 90-150 minutes)
deck-box divination

# Custom time range (50-70 minutes)
deck-box divination --min 50 --max 70

# Draw a single card
deck-box divination --single
```

**Parameters:**

- `--min`: Minimum total execution time in minutes (default: 90)
- `--max`: Maximum total execution time in minutes (default: 150)
- `--single`: Draw only one card

### Show Cards

```bash
# Show all cards
deck-box show cards

# Show only pending cards
deck-box show cards --pending

# Show only completed cards
deck-box show cards --completed
```

### Show Divination Results

```bash
# Show last divination result
deck-box show divination

# Show all divination history
deck-box show divination --all
```

### Complete a Card

```bash
deck-box complete <card_id> --mood good --actual-time 12 --quality excellent
```

**Parameters:**

- `<card_id>`: ID of the card to complete (required)
- `--mood`: Your mood (awesome, good, neutral, bad, terrible)
- `--actual-time`: Actual time spent in minutes
- `--quality`: Quality rating (excellent, good,medium, poor)

### Modify a Card

```bash
# Update card name and mark as completed
deck-box modify <card_id> --name "Revised project report" --completed

# Update predecessor and clear it
deck-box modify <card_id> --predecessor <new_predecessor_id>
deck-box modify <card_id> --predecessor ''  # Clear predecessor
```

**Parameters:**

- `<card_id>`: ID of the card to modify (required)
- `--name`: New task content (optional)
- `--predecessor`: New predecessor card ID or empty string to clear (optional)
- `--completed/--not-completed`: Mark card as completed or not completed (optional)

### Delete a Card

```bash
# Delete a card
deck-box delete <card_id>
```

**Parameters:**

- `<card_id>`: ID of the card to delete (required)

The delete command will show the card details and ask for confirmation before permanently removing it.

## 📊 Card Level System

Cards are automatically assigned levels based on their estimated duration:

| Level               | Duration (minutes) | Probability Weight | Description           |
| ------------------- | ------------------ | ------------------ | --------------------- |
| 🟢**Level 1** | ≤ 15              | Highest            | Quick, focused tasks  |
| 🟡**Level 2** | 16-30              | High               | Short to medium tasks |
| 🟠**Level 3** | 31-60              | Medium             | Medium to large tasks |
| 🔴**Level 4** | > 60               | Lowest             | Large, complex tasks  |

### 🎲 Probability Mechanism

The divination system uses a probability algorithm:

- **Inverse Probability**: Longer tasks (higher levels) have lower chance of being drawn
- **Level-based Weights**: Each level has specific probability weights (adjustable)
- **Balanced Drawing**: Ensures total time stays within your specified range

## 📁 Project Structure

```
deck-box/
├── deck_box/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # CLI command interface
│   ├── models.py         # Data models (Card, DivinationResult)
│   ├── storage.py        # Local JSON storage
│   ├── divination.py     # Card drawing algorithm
│   └── utils.py          # Utility functions (task analysis, visual effects)
├── tests/                # Test files
│   └── test_models.py    # Card model tests
├── setup.py              # Package configuration
├── README.md             # This file
└── LICENSE               # MIT License
```

## 🎯 Core Mechanisms

### Card Data Model

Each card contains:

- **Metadata**: ID, name, creation time, status
- **Execution Info**: Time estimate, actual time, quality rating
- **Organizational Info**: Tags, dependencies
- **Progress Info**: Status, completion time, mood

### Storage System

- **Local JSON**: Stores all data in a local JSON file
- **Data Persistence**: Automatic saving after each operation
- **Backup-friendly**: Easy to backup and transfer between devices

### Divination Algorithm

1. **Filter Cards**: Only pending cards with no uncompleted dependencies
2. **Level Calculation**: Determine level based on duration
3. **Probability Assignment**: Apply level-based weights
4. **Card Selection**: Randomly select cards until total time is within range
5. **Visual Effects**: Display sparkling animations based on card level

## 📄 License

MIT License - feel free to use and modify!

# TODO

* [ ] code review
* [ ] Be able to configure the API key and use AI for task analysis and disassembly recommendations.
* [ ] Be able to specify specific cards using the first few digits of the card ID.

---

**Happy Tasking!** 🎉🎴
