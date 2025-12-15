import click
from colorama import Fore, Style
from .models import Card, Mood, Quality, CardStatus
from .storage import Storage
from .divination import Divination
from .utils import TaskAnalyzer, VisualEffects

@click.group()
def cli():
    """🧙‍♀️ Deck Box - A card-based task management tool for overcoming executive dysfunction
    
    Transform your tasks into a card game! Deck Box helps you manage your to-do list by breaking 
    tasks into manageable "cards" with different levels based on estimated time. Use the divination 
    feature to randomly draw cards from your deck, making task selection feel like a fun game 
    rather than an overwhelming chore.
    """
    pass

@cli.command()
@click.option('--name', '-n', required=True, help='The name/title of the task card')
@click.option('--time', '-t', type=int, required=True, help='Estimated time needed to complete the task (in minutes)')
@click.option('--tag', '-g', help='Optional tag to categorize the card (e.g., work, personal, study)')
@click.option('--description', '-d', help='Optional detailed description of the task')
@click.option('--predecessor', '-p', help='Optional ID of a prerequisite task that must be completed first')
def add(name, time, tag, description, predecessor):
    """Add a new task card to your deck box
    
    Creates a new task card with the specified details. The card will be automatically assigned
    a level (1-4) based on its estimated time, and analyzed for potential improvements. If the
    task is complex, suggestions will be provided for breaking it down into smaller tasks.
    """
    storage = Storage()
    
    # Check if predecessor card exists
    if predecessor:
        predecessor_card = storage.get_card_by_id(predecessor)
        if not predecessor_card:
            click.echo(f"{Fore.RED}❌ 前置卡片ID不存在！{Style.RESET_ALL}")
            return
    
    # Analyze task
    warnings, suggestions = TaskAnalyzer.analyze_task(name, time)
    
    # Create new card
    card = Card(name, time, tag, description, predecessor)
    storage.add_card(card)
    
    # Display addition result
    click.echo(f"\n{Fore.GREEN}✅ 成功添加卡片！{Style.RESET_ALL}")
    click.echo(f"   ID: {card.id}")
    click.echo(f"   名称: {card.name}")
    click.echo(f"   预计时间: {card.estimated_time}分钟")
    click.echo(f"   级别: {card.level}")
    click.echo(f"   标签: {card.tag if card.tag else '无'}")
    
    # Display task analysis result
    if warnings:
        click.echo(f"\n{Fore.YELLOW}📋 任务分析建议：{Style.RESET_ALL}")
        for warning in warnings:
            click.echo(f"   {warning}")
        
        for suggestion in suggestions:
            click.echo(f"   {suggestion}")

@cli.command()
@click.option('--min', type=int, default=90, help='Minimum total execution time for all drawn cards (in minutes)')
@click.option('--max', type=int, default=150, help='Maximum total execution time for all drawn cards (in minutes)')
@click.option('--single', is_flag=True, help='Draw only one card')
def divination(min, max, single):
    """Perform a divination to randomly draw task cards from your deck
    
    Experience the magic of divination as the system randomly selects cards from your deck that
    match the specified time range. The cards are selected using a weighted probability system
    that ensures a balanced mix of task levels. The result is saved for future reference.
    
    Example: deck-box divination --min 60 --max 120
    Example: deck-box divination --single
    """
    divination = Divination()
    
    # Display witch divination effect
    VisualEffects.show_witch_intro()
    
    # Perform card drawing
    if single:
        card = divination.draw_single_card()
        selected_cards = [card] if card else None
    else:
        selected_cards = divination.perform_divination(min_time=min, max_time=max)
    
    if not selected_cards:
        click.echo(f"\n{Fore.RED}❌ 无法找到合适的卡片组合！{Style.RESET_ALL}")
        click.echo(f"   请尝试调整时间范围或添加更多卡片。")
        return
    
    # Save divination result
    from .models import DivinationResult
    result = DivinationResult(selected_cards)
    divination.storage.save_divination(result)
    
    # Display drawing result
    click.echo(f"\n{Fore.MAGENTA}🔮 今日占卜结果：{Style.RESET_ALL}")
    click.echo(f"   共 {len(selected_cards)} 张卡片，总时长: {result.total_time} 分钟")
    click.echo(f"   {Fore.CYAN}────────────────────────────────────{Style.RESET_ALL}")
    
    for i, card in enumerate(selected_cards, 1):
        # Display sparkle effect
        VisualEffects.show_gold_sparkles(card.level)
        
        level_color = {
            1: Fore.GREEN,
            2: Fore.BLUE,
            3: Fore.YELLOW,
            4: Fore.RED
        }[card.level]
        
        click.echo(f"   {i}. {Fore.WHITE}{card.name}{Style.RESET_ALL}")
        click.echo(f"      {level_color}级别: {card.level}{Style.RESET_ALL} | 时长: {card.estimated_time}分钟 | 标签: {card.tag if card.tag else '无'}")
        if card.description:
            click.echo(f"      描述: {card.description}")
    
    click.echo(f"   {Fore.CYAN}────────────────────────────────────{Style.RESET_ALL}")
    click.echo(f"   {Fore.YELLOW}💡 提示：完成卡片后使用 'deck-box complete <card_id>' 记录完成情况{Style.RESET_ALL}")

@cli.command()
@click.argument('what', type=click.Choice(['cards', 'divination'], case_sensitive=False))
def show(what):
    """Display information about your cards or divination history
    
    Choose between two options:
    - cards: Show all task cards in your deck box, including status, level, and details
    - divination: Show the results of your most recent card divination session
    
    Example: deck-box show cards
    Example: deck-box show divination
    """
    storage = Storage()
    
    if what == 'cards':
        # Display all cards
        cards = storage.load_cards()
        if not cards:
            click.echo(f"{Fore.YELLOW}📦 卡盒中还没有卡片！{Style.RESET_ALL}")
            return
        
        click.echo(f"{Fore.BLUE}📋 所有卡片 ({len(cards)}):{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}────────────────────────────────────────────────────────────────────{Style.RESET_ALL}")
        
        for card in cards:
            status_color = Fore.GREEN if card.status == CardStatus.COMPLETED else Fore.RED
            status_icon = "✅" if card.status == CardStatus.COMPLETED else "⏳"
            
            level_color = {
                1: Fore.GREEN,
                2: Fore.BLUE,
                3: Fore.YELLOW,
                4: Fore.RED
            }[card.level]
            
            click.echo(f"{status_icon} {Fore.WHITE}{card.name}{Style.RESET_ALL}")
            click.echo(f"   ID: {card.id}")
            click.echo(f"   {status_color}状态: {card.status.value}{Style.RESET_ALL}")
            click.echo(f"   {level_color}级别: {card.level}{Style.RESET_ALL} | 预计时间: {card.estimated_time}分钟")
            if card.actual_time:
                click.echo(f"   实际时间: {card.actual_time}分钟")
            click.echo(f"   标签: {card.tag if card.tag else '无'}")
            if card.predecessor_id:
                click.echo(f"   前置卡片: {card.predecessor_id}")
            click.echo(f"{Fore.CYAN}────────────────────────────────────────────────────────────────────{Style.RESET_ALL}")
    
    elif what == 'divination':
        # Display latest divination result
        divinations = storage.load_divinations()
        if not divinations:
            click.echo(f"{Fore.YELLOW}🔮 还没有进行过占卜！{Style.RESET_ALL}")
            return
        
        last_divination = max(divinations, key=lambda d: d.created_at)
        
        click.echo(f"{Fore.MAGENTA}🔮 最近一次占卜结果：{Style.RESET_ALL}")
        click.echo(f"   占卜时间: {last_divination.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(f"   共 {len(last_divination.cards)} 张卡片，总时长: {last_divination.total_time} 分钟")
        click.echo(f"   {Fore.CYAN}────────────────────────────────────{Style.RESET_ALL}")
        
        for i, card in enumerate(last_divination.cards, 1):
            level_color = {
                1: Fore.GREEN,
                2: Fore.BLUE,
                3: Fore.YELLOW,
                4: Fore.RED
            }[card.level]
            
            click.echo(f"   {i}. {Fore.WHITE}{card.name}{Style.RESET_ALL}")
            click.echo(f"      {level_color}级别: {card.level}{Style.RESET_ALL} | 时长: {card.estimated_time}分钟 | 标签: {card.tag if card.tag else '无'}")
        
        click.echo(f"   {Fore.CYAN}────────────────────────────────────{Style.RESET_ALL}")

@cli.command()
@click.argument('card_id')
@click.option('--mood', '-m', type=click.Choice([m.value for m in Mood], case_sensitive=False), required=True, help='How you felt after completing the task (good, average, bad)')
@click.option('--actual-time', '-t', type=int, required=True, help='Actual time taken to complete the task (in minutes)')
@click.option('--quality', '-q', type=click.Choice([q.value for q in Quality], case_sensitive=False), required=True, help='Quality of the completed work (excellent, good, average, poor)')
def complete(card_id, mood, actual_time, quality):
    """Mark a task card as completed and record your experience
    
    Update a task card's status to completed and provide feedback about your experience:
    - Mood: How you felt after completing the task
    - Actual Time: The real time it took (may differ from estimate)
    - Quality: How well you think you completed the task
    
    Example: deck-box complete card_123 --mood good --actual-time 15 --quality excellent
    """
    storage = Storage()
    
    # Find card
    card = storage.get_card_by_id(card_id)
    if not card:
        click.echo(f"{Fore.RED}❌ 卡片ID不存在！{Style.RESET_ALL}")
        return
    
    if card.status == CardStatus.COMPLETED:
        click.echo(f"{Fore.YELLOW}⚠️  这张卡片已经完成了！{Style.RESET_ALL}")
        return
    
    # Complete card
    mood_enum = Mood[mood.upper()]
    quality_enum = Quality[quality.upper()]
    card.complete(mood_enum, actual_time, quality_enum)
    
    # Update card
    cards = storage.load_cards()
    for i, c in enumerate(cards):
        if c.id == card.id:
            cards[i] = card
            break
    storage.save_cards(cards)
    
    # Display completion result
    click.echo(f"\n{Fore.GREEN}✅ 成功完成卡片！{Style.RESET_ALL}")
    click.echo(f"   卡片名称: {card.name}")
    click.echo(f"   预计时间: {card.estimated_time}分钟")
    click.echo(f"   实际时间: {card.actual_time}分钟")
    click.echo(f"   心情: {Fore.YELLOW}{card.mood.value}{Style.RESET_ALL}")
    click.echo(f"   质量: {Fore.BLUE}{card.quality.value}{Style.RESET_ALL}")
    click.echo(f"   完成时间: {card.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")

@cli.command()
@click.argument('card_id')
@click.option('-t', '--task', help='New task content (optional)')
@click.option('-p', '--predecessor', help='New predecessor card ID (optional)')
@click.option('--completed/--not-completed', default=None, help='Mark card as completed or not completed (optional)')
def modify(card_id, task, predecessor, completed):
    """Modify an existing card.
    
    This command allows you to update the task content, predecessor, or completion status of an existing card.
    Only the specified fields will be updated.
    
    Example:
        deck-box modify 123 -t "New task description" --completed
        deck-box modify 456 -p 789
        deck-box modify 789 -p ''  # Clear predecessor
    """
    storage = Storage()
    card = storage.get_card_by_id(card_id)
    if not card:
        click.echo(f"{Fore.RED}❌ 卡片ID不存在！{Style.RESET_ALL}")
        return
    
    # Show current card info
    click.echo("Current card information:")
    click.echo(f"ID: {card.id}")
    click.echo(f"Task: {card.name}")
    click.echo(f"Level: {card.level}")
    click.echo(f"Predecessor: {card.predecessor_id or 'None'}")
    click.echo(f"Completed: {card.status == CardStatus.COMPLETED}")
    click.echo(f"Created at: {card.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    click.echo(f"Completed at: {card.completed_at.strftime('%Y-%m-%d %H:%M:%S') if card.completed_at else 'None'}")
    click.echo()
    
    # Update fields if provided
    updated = False
    
    if task:
        card.name = task
        updated = True
    
    if predecessor is not None:
        # Allow clearing predecessor with empty string
        if predecessor == '':
            card.predecessor_id = None
        else:
            # Check if predecessor card exists
            predecessor_card = storage.get_card_by_id(predecessor)
            if not predecessor_card:
                click.echo(f"{Fore.RED}❌ 前置卡片ID不存在！{Style.RESET_ALL}")
                return
            card.predecessor_id = predecessor
        updated = True
    
    if completed is not None:
        if completed and card.status != CardStatus.COMPLETED:
            # Mark as completed with default values
            card.complete(Mood.GOOD, card.estimated_time, Quality.GOOD)
            updated = True
        elif not completed and card.status == CardStatus.COMPLETED:
            # Reset completion status
            card.status = CardStatus.PENDING
            card.completed_at = None
            card.mood = None
            card.actual_time = None
            card.quality = None
            updated = True
    
    if not updated:
        click.echo(f"{Fore.YELLOW}⚠️  没有指定任何更改！{Style.RESET_ALL}")
        return
    
    # Update card in storage
    cards = storage.load_cards()
    for i, c in enumerate(cards):
        if c.id == card.id:
            cards[i] = card
            break
    storage.save_cards(cards)
    
    click.echo(f"{Fore.GREEN}✅ 卡片更新成功！{Style.RESET_ALL}")
    click.echo("Updated card information:")
    click.echo(f"ID: {card.id}")
    click.echo(f"Task: {card.name}")
    click.echo(f"Level: {card.level}")
    click.echo(f"Predecessor: {card.predecessor_id or 'None'}")
    click.echo(f"Completed: {card.status == CardStatus.COMPLETED}")

@cli.command()
@click.argument('card_id')
def delete(card_id):
    """Delete an existing card.
    
    This command permanently removes a card from the deck.
    
    Example:
        deck-box delete 123
    """
    storage = Storage()
    card = storage.get_card_by_id(card_id)
    if not card:
        click.echo(f"{Fore.RED}❌ 卡片ID不存在！{Style.RESET_ALL}")
        return
    
    # Show card info before deletion
    click.echo("Card to be deleted:")
    click.echo(f"ID: {card.id}")
    click.echo(f"Task: {card.name}")
    click.echo(f"Level: {card.level}")
    click.echo(f"Completed: {card.status == CardStatus.COMPLETED}")
    click.echo()
    
    # Confirm deletion
    if click.confirm("Are you sure you want to delete this card? This action cannot be undone."):
        # Delete card from storage
        cards = storage.load_cards()
        cards = [c for c in cards if c.id != card_id]
        storage.save_cards(cards)
        click.echo(f"{Fore.GREEN}✅ 卡片已删除！{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.YELLOW}⚠️  删除已取消！{Style.RESET_ALL}")

if __name__ == '__main__':
    cli()