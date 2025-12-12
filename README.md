# Deck Box

A card deck game for task management, designed to help you break down large tasks into smaller, manageable pieces.

## Features

- **Add Cards**: Create task cards with execution content, time estimates, and optional dependencies
- **Divination**: Randomly draw cards with total execution time between 1.5h~2.5h (default)
- **Track Progress**: Mark cards as completed with mood, duration, and quality ratings
- **Smart Probability**: Longer tasks have lower chance of being drawn, encouraging task decomposition
- **Task Analysis**: Get suggestions for task decomposition if tasks are too vague or complex
- **Visual Effects**: Gold sparkling effects during card drawing based on card level

## Installation

```bash
pip install deck-box
```

## Usage

### Add a Card

```bash
deck-box add --name "完成项目文档" --time 15 --tag work
```

### Draw Cards (Divination)

```bash
# Draw cards with total time between 50-70 minutes
deck-box divination --min 50 --max 70

# Draw a single card (default)
deck-box divination
```

### Show All Cards

```bash
deck-box show cards
```

### Show Last Divination Result

```bash
deck-box show divination
```

### Complete a Card

```bash
deck-box complete <card_id> --mood good --actual-time 12 --quality excellent
```

## Card Levels

- **Level 1** (<= 15 minutes): Most likely to be drawn
- **Level 2** (16-30 minutes): Medium probability
- **Level 3** (31-60 minutes): Lower probability
- **Level 4** (> 60 minutes): Least likely to be drawn

## Project Structure

```
deck-box/
├── deck_box/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── storage.py
│   ├── divination.py
│   └── utils.py
├── setup.py
├── README.md
└── LICENSE
```

## License

MIT