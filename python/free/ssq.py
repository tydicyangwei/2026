import random
from itertools import combinations

def parse_bets(bet_string):
    """
    解析用户输入的下注字符串，将其转换为标准的彩票号码列表。

    支持格式:
    - 单式: "1,2,3,4,5,6,7"
    - 多注单式: "1,2,3,4,5,6,7;8,9,10,11,12,13,14"
    - 复式: "1,2,3,4,5,6,7,8,9|15,16" (红球复式)
    - 胆拖: "1,2,3|4,5,6,7,8,9|15" (胆码3个, 拖码6个, 蓝球1个)
      (胆拖玩法在此实现中被视为一种特殊的复式)

    Args:
        bet_string (str): 用户输入的原始字符串。

    Returns:
        list: 一个包含所有有效投注组合的列表，每个组合是 (red_balls_list, blue_ball_int)。
    """
    all_bets = []
    # 使用分号或竖线作为分割符，以区分不同的"票"
    tickets = bet_string.replace(';', '|').split('|')

    # 如果只有一个部分，则是单式或复式
    if len(tickets) == 1:
        numbers = list(map(int, tickets[0].split(',')))
        if len(numbers) == 7: # 单式
            red_balls = sorted(numbers[:6])
            blue_ball = numbers[6]
            all_bets.append((red_balls, blue_ball))
        else: # 复式
            red_pool = sorted(list(set(numbers[:-1])))
            blue_pool = [numbers[-1]]
            if len(red_pool) >= 6:
                for red_combo in combinations(red_pool, 6):
                    for blue_num in blue_pool:
                        all_bets.append((list(red_combo), blue_num))
    # 如果有两部分，可能是"红球复式|蓝球复式"或"胆码|拖码|蓝球"
    elif len(tickets) == 2:
        red_part = list(map(int, tickets[0].split(',')))
        blue_part = list(map(int, tickets[1].split(',')))

        # 如果第一部分大于等于6个号，第二部分大于等于1个号，则为复式
        if len(red_part) >= 6 and len(blue_part) >= 1:
            red_pool = sorted(list(set(red_part)))
            blue_pool = sorted(list(set(blue_part)))
            for red_combo in combinations(red_pool, 6):
                for blue_num in blue_pool:
                    all_bets.append((list(red_combo), blue_num))
        # 否则，如果第一部分小于6个号，第二部分大于等于(6-len(第一部分))个号，则为胆拖
        elif len(red_part) < 6 and len(red_part) + len(blue_part) >= 6:
            # 此处简化处理，假设第一部分是胆码，第二部分是拖码
            # 例如 "1,2|3,4,5,6,7,8|9" 在原输入中会被分为三段，这里无法处理
            # 为了兼容，我们约定胆拖用两个分隔符，如 "1,2|3,4,5,6,7,8|9"
            # 如果只有两个部分，则按复式处理
            # 这里按最常见理解：前半部分红球池，后半部分蓝球池
            pass # 已在上面处理

    # 如果有三部分，则是"胆码|拖码|蓝球"格式
    elif len(tickets) == 3:
        danma = list(map(int, tickets[0].split(',')))
        tuoma = list(map(int, tickets[1].split(',')))
        blue_part = list(map(int, tickets[2].split(',')))

        if len(danma) > 0 and len(danma) < 6 and len(tuoma) >= (6 - len(danma)):
            red_pool = sorted(list(set(tuoma)))
            blue_pool = sorted(list(set(blue_part)))

            # 从拖码中选出剩余的红球
            remaining_count = 6 - len(danma)
            for tuoma_combo in combinations(red_pool, remaining_count):
                full_red_combo = sorted(danma + list(tuoma_combo))
                for blue_num in blue_pool:
                    all_bets.append((full_red_combo, blue_num))
        else:
            raise ValueError("胆拖格式错误，请检查号码数量。")

    # 其他情况，如多注单式
    else:
        for ticket in tickets:
            numbers = list(map(int, ticket.split(',')))
            if len(numbers) == 7:
                red_balls = sorted(numbers[:6])
                blue_ball = numbers[6]
                all_bets.append((red_balls, blue_ball))

    return all_bets

def generate_lottery_numbers():
    """生成一组随机的双色球开奖号码。"""
    red_balls = sorted(random.sample(range(1, 34), 6))
    blue_ball = random.randint(1, 16)
    return red_balls, blue_ball

def check_prize(bet_red, bet_blue, draw_red, draw_blue):
    """判断给定的投注号码与开奖号码的匹配情况，并返回对应的奖项。"""
    red_matches = len(set(bet_red).intersection(set(draw_red)))
    blue_match = (bet_blue == draw_blue)

    if red_matches == 6 and blue_match:
        return "一等奖"
    elif red_matches == 6 and not blue_match:
        return "二等奖"
    elif red_matches == 5 and blue_match:
        return "三等奖"
    elif (red_matches == 5 and not blue_match) or (red_matches == 4 and blue_match):
        return "四等奖"
    elif (red_matches == 4 and not blue_match) or (red_matches == 3 and blue_match):
        return "五等奖"
    elif (red_matches == 2 and blue_match) or (red_matches == 1 and blue_match) or (red_matches == 0 and blue_match):
        return "六等奖"
    elif red_matches == 3 and not blue_match:
        return "福运奖"
    else:
        return "未中奖"

def get_prize_amount(prize_type):
    """获取各奖项对应的奖金金额"""
    prize_amounts = {
        "一等奖": 8000000,  # 800万元
        "二等奖": 300000,   # 30万元
        "三等奖": 3000,     # 3000元
        "四等奖": 200,      # 200元
        "五等奖": 10,       # 10元
        "六等奖": 5,        # 5元
        "福运奖": 5         # 5元
    }
    return prize_amounts.get(prize_type, 0)

def calculate_bet_cost(bet_string):
    """计算投注所需的总金额"""
    all_bets = parse_bets(bet_string)
    # 每注2元
    return len(all_bets) * 2

def main():
    """主函数，处理用户输入、运行模拟并输出结果。"""
    print("--- 双色球开奖模拟系统 (支持多注/复式/胆拖) ---")

    try:
        num_draws = int(input("请输入要模拟的开奖次数: "))
        if num_draws <= 0:
            print("开奖次数必须是正整数！")
            return

        print("\n请输入您的下注号码，支持以下格式:")
        print("单式: 1,2,3,4,5,6,7")
        print("多注单式: 1,2,3,4,5,6,7;8,9,10,11,12,13,14")
        print("红球复式: 1,2,3,4,5,6,7,8|15 (从8个红球中选6个，从1个蓝球中选1个)")
        print("蓝球复式: 1,2,3,4,5,6,7|15,16")
        print("红蓝复式: 1,2,3,4,5,6,7,8|15,16")
        print("胆拖: 1,2,3|4,5,6,7,8,9|15 (2胆4拖1蓝)")
        print("-" * 50)

        bet_input = input("请输入您的号码 (可包含多个注，用';'或'|'分隔): ")

        all_bets = parse_bets(bet_input)
        if not all_bets:
            print("未能解析出任何有效号码，请检查输入格式。")
            return

        print(f"\n解析成功，共生成 {len(all_bets)} 注彩票。")

        # 计算投注成本
        bet_cost = calculate_bet_cost(bet_input)
        print(f"每期投注金额: {bet_cost} 元")
        total_investment = bet_cost * num_draws
        print(f"总投注金额: {total_investment} 元")

        # 验证所有号码的有效性
        for red, blue in all_bets:
            for num in red:
                if num < 1 or num > 33:
                    raise ValueError(f"红球号码 {num} 不在有效范围 [1, 33] 内！")
            if blue < 1 or blue > 16:
                raise ValueError(f"蓝球号码 {blue} 不在有效范围 [1, 16] 内！")

    except ValueError as e:
        print(f"输入格式错误！{e}")
        return

    print("\n开始模拟开奖...\n")

    # 初始化计数器
    prize_counts = {
        "一等奖": 0, "二等奖": 0, "三等奖": 0, "四等奖": 0,
        "五等奖": 0, "六等奖": 0, "福运奖": 0, "未中奖": 0
    }

    total_prize_money = 0  # 总中奖金额

    # 进行指定次数的开奖模拟
    for i in range(num_draws):
        draw_red, draw_blue = generate_lottery_numbers()

        # 对每一注都进行开奖检查
        for bet_red, bet_blue in all_bets:
            result = check_prize(bet_red, bet_blue, draw_red, draw_blue)
            
            # 统计奖项
            prize_counts[result] += 1
            
            # 计算中奖金额
            if result != "未中奖":
                prize_amount = get_prize_amount(result)
                total_prize_money += prize_amount

    # 输出最终统计结果
    print("--- 模拟开奖结束，中奖统计结果如下 ---")
    print(f"您总共投入了 {len(all_bets)} 注 * {num_draws} 期 = {len(all_bets) * num_draws} 次投注机会")
    print(f"总投注金额: {total_investment} 元")
    print("-" * 40)

    total_wins = sum(v for k, v in prize_counts.items() if k != "未中奖")
    print(f"总中奖次数: {total_wins}")
    print(f"总中奖金额: {total_prize_money} 元")
    
    if total_investment > 0:
        profit = total_prize_money - total_investment
        print(f"盈亏情况: {'盈利' if profit > 0 else '亏损'} {abs(profit)} 元")
        if total_investment > 0:
            roi = (profit / total_investment) * 100
            print(f"投资回报率: {roi:.2f}%")
    
    print("-" * 40)

    # 按照奖项等级顺序打印
    for prize in ["一等奖", "二等奖", "三等奖", "四等奖", "五等奖", "六等奖", "福运奖"]:
        count = prize_counts[prize]
        prize_amount = get_prize_amount(prize)
        prize_total = count * prize_amount
        print(f"{prize}: {count} 次 (单次{prize_amount}元, 小计{prize_total}元)")

if __name__ == "__main__":
    main()