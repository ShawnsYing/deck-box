import click
from colorama import Fore, Style
from .models import Card, Mood, Quality, CardStatus
from .storage import Storage
from .divination import Divination
from .utils import TaskAnalyzer, VisualEffects

@click.group()
def cli():
    """🧙‍♀️ Deck Box - 一个基于抽卡的任务管理工具"""
    pass

@cli.command()
@click.option('--name', '-n', required=True, help='卡片名称')
@click.option('--time', '-t', type=int, required=True, help='预计执行时间（分钟）')
@click.option('--tag', '-g', help='卡片标签')
@click.option('--description', '-d', help='卡片描述')
@click.option('--predecessor', '-p', help='前置卡片ID')
def add(name, time, tag, description, predecessor):
    """添加一张新卡片到卡盒"""
    storage = Storage()
    
    # 检查前置卡片是否存在
    if predecessor:
        predecessor_card = storage.get_card_by_id(predecessor)
        if not predecessor_card:
            click.echo(f"{Fore.RED}❌ 前置卡片ID不存在！{Style.RESET_ALL}")
            return
    
    # 分析任务
    warnings, suggestions = TaskAnalyzer.analyze_task(name, time)
    
    # 创建新卡片
    card = Card(name, time, tag, description, predecessor)
    storage.add_card(card)
    
    # 显示添加结果
    click.echo(f"\n{Fore.GREEN}✅ 成功添加卡片！{Style.RESET_ALL}")
    click.echo(f"   ID: {card.id}")
    click.echo(f"   名称: {card.name}")
    click.echo(f"   预计时间: {card.estimated_time}分钟")
    click.echo(f"   级别: {card.level}")
    click.echo(f"   标签: {card.tag if card.tag else '无'}")
    
    # 显示任务分析结果
    if warnings:
        click.echo(f"\n{Fore.YELLOW}📋 任务分析建议：{Style.RESET_ALL}")
        for warning in warnings:
            click.echo(f"   {warning}")
        
        for suggestion in suggestions:
            click.echo(f"   {suggestion}")

@cli.command()
@click.option('--min', type=int, default=90, help='最小总执行时间（分钟）')
@click.option('--max', type=int, default=150, help='最大总执行时间（分钟）')
def divination(min, max):
    """从卡盒中抽取卡片（占卜）"""
    divination = Divination()
    
    # 显示女巫占卜效果
    VisualEffects.show_witch_intro()
    
    # 执行抽卡
    selected_cards = divination.perform_divination(min_time=min, max_time=max)
    
    if not selected_cards:
        click.echo(f"\n{Fore.RED}❌ 无法找到合适的卡片组合！{Style.RESET_ALL}")
        click.echo(f"   请尝试调整时间范围或添加更多卡片。")
        return
    
    # 保存占卜结果
    from .models import DivinationResult
    result = DivinationResult(selected_cards)
    divination.storage.save_divination(result)
    
    # 显示抽取结果
    click.echo(f"\n{Fore.PURPLE}🔮 今日占卜结果：{Style.RESET_ALL}")
    click.echo(f"   共 {len(selected_cards)} 张卡片，总时长: {result.total_time} 分钟")
    click.echo(f"   {Fore.CYAN}────────────────────────────────────{Style.RESET_ALL}")
    
    for i, card in enumerate(selected_cards, 1):
        # 显示闪光效果
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
    """显示卡片或占卜结果"""
    storage = Storage()
    
    if what == 'cards':
        # 显示所有卡片
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
        # 显示最近一次占卜结果
        divinations = storage.load_divinations()
        if not divinations:
            click.echo(f"{Fore.YELLOW}🔮 还没有进行过占卜！{Style.RESET_ALL}")
            return
        
        last_divination = max(divinations, key=lambda d: d.created_at)
        
        click.echo(f"{Fore.PURPLE}🔮 最近一次占卜结果：{Style.RESET_ALL}")
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
@click.option('--mood', '-m', type=click.Choice([m.value for m in Mood], case_sensitive=False), required=True, help='完成心情')
@click.option('--actual-time', '-t', type=int, required=True, help='实际执行时间（分钟）')
@click.option('--quality', '-q', type=click.Choice([q.value for q in Quality], case_sensitive=False), required=True, help='完成质量')
def complete(card_id, mood, actual_time, quality):
    """标记卡片为已完成"""
    storage = Storage()
    
    # 查找卡片
    card = storage.get_card_by_id(card_id)
    if not card:
        click.echo(f"{Fore.RED}❌ 卡片ID不存在！{Style.RESET_ALL}")
        return
    
    if card.status == CardStatus.COMPLETED:
        click.echo(f"{Fore.YELLOW}⚠️  这张卡片已经完成了！{Style.RESET_ALL}")
        return
    
    # 完成卡片
    mood_enum = Mood[mood.upper()]
    quality_enum = Quality[quality.upper()]
    card.complete(mood_enum, actual_time, quality_enum)
    
    # 更新卡片
    cards = storage.load_cards()
    for i, c in enumerate(cards):
        if c.id == card.id:
            cards[i] = card
            break
    storage.save_cards(cards)
    
    # 显示完成结果
    click.echo(f"\n{Fore.GREEN}✅ 成功完成卡片！{Style.RESET_ALL}")
    click.echo(f"   卡片名称: {card.name}")
    click.echo(f"   预计时间: {card.estimated_time}分钟")
    click.echo(f"   实际时间: {card.actual_time}分钟")
    click.echo(f"   心情: {Fore.YELLOW}{card.mood.value}{Style.RESET_ALL}")
    click.echo(f"   质量: {Fore.BLUE}{card.quality.value}{Style.RESET_ALL}")
    click.echo(f"   完成时间: {card.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    cli()