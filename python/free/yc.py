import itertools
import time

# 定义所有集合
L1 = [11,15,16,21,23,24,28,29,31,33] #长冷
L2 = [3,4,5,8,9,10,12,13,19,25,27,30] #长温
L3 = [1,2,6,7,14,17,18,20,22,26,32] #长热

M1 = [5,20,26] #短冷
M2 = [1,3,8,13,21,23,27,28,29] #短温
M3 = [2,4,6,7,9,10,11,12,14,15,16,17,18,19,22,24,25,30,31,32,33] #短热

N1 = [1,2,3,4,5,6,7,8,9,10,11]
N2 = [12,13,14,15,16,17,18,19,20,21,22]
N3 = [23,24,25,26,27,28,29,30,31,32,33]

F = [1,2,5,8,9,10,14,20,26,28,29,32,33]  # 禁止集
R = [24,27,31]  # 必须包含恰好1个元素

def check_adjacent_numbers(numbers):
    """检查列表中是否有相邻的数"""
    sorted_nums = sorted(numbers)
    for i in range(len(sorted_nums) - 1):
        if sorted_nums[i+1] - sorted_nums[i] == 1:
            return True
    return False

def validate_combination(combo):
    """验证组合是否满足所有条件"""
    combo_set = set(combo)
    
    # 条件1: 检查禁止集F
    if any(num in F for num in combo):
        return False
    
    # 条件2: L1:L2:L3 = 2:2:2 主推4-1-1和2-3-1
    count_L1 = sum(1 for num in combo if num in L1)
    count_L2 = sum(1 for num in combo if num in L2)
    count_L3 = sum(1 for num in combo if num in L3)
    
    if count_L1 != 2 or count_L2 != 2 or count_L3 != 2:
        return False
    
    # 条件3: M1:M2:M3 = 0:2:4 主推1-1-4和1-0-5和0-1-5
    count_M1 = sum(1 for num in combo if num in M1)
    count_M2 = sum(1 for num in combo if num in M2)
    count_M3 = sum(1 for num in combo if num in M3)
    
    if count_M1 != 0 or count_M2 != 2 or count_M3 != 4:
        return False
    
    # 条件4: N1:N2:N3 = 2:2:2 #2026-4-2 主推1-3-2和1-2-3
    count_N1 = sum(1 for num in combo if num in N1)
    count_N2 = sum(1 for num in combo if num in N2)
    count_N3 = sum(1 for num in combo if num in N3)
    
    if count_N1 != 2 or count_N2 != 2 or count_N3 != 2:
        return False
    
    # 条件5: R集包含恰好1个元素
    count_R = sum(1 for num in combo if num in R)
    if count_R != 1:
        return False
    
    # 条件6: 不包含相邻的数
    if check_adjacent_numbers(combo):
        return False
    
    return True

def find_valid_combinations():
    """查找所有满足条件的组合"""
    start_time = time.time()
    valid_combinations = []
    total_count = 0
    valid_count = 0
    
    # 生成所有可能的6个数的组合（1-33）
    all_numbers = list(range(1, 34))
    
    print("开始搜索满足条件的组合...")
    print(f"总组合数: {len(list(itertools.combinations(all_numbers, 6)))}")
    
    for combo in itertools.combinations(all_numbers, 6):
        total_count += 1
        
        # 进度显示（每10万次显示一次）
        if total_count % 100000 == 0:
            elapsed_time = time.time() - start_time
            print(f"已检查: {total_count:,} 个组合, 有效: {valid_count}, 耗时: {elapsed_time:.2f}秒")
        
        if validate_combination(combo):
            valid_combinations.append(combo)
            valid_count += 1
    
    elapsed_time = time.time() - start_time
    print(f"\n搜索完成!")
    print(f"总检查组合数: {total_count:,}")
    print(f"有效组合数: {valid_count}")
    print(f"总耗时: {elapsed_time:.2f}秒")
    
    return valid_combinations

def save_to_file(combinations, filename="valid_combinations.txt"):
    """将结果保存到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"总有效组合数: {len(combinations)}\n")
        f.write("=" * 50 + "\n")
        
        for i, combo in enumerate(combinations, 1):
            f.write(f"组合 {i}: {sorted(combo)}\n")
            
            # 验证信息
            combo_set = set(combo)
            count_L1 = sum(1 for num in combo if num in L1)
            count_L2 = sum(1 for num in combo if num in L2)
            count_L3 = sum(1 for num in combo if num in L3)
            
            count_M1 = sum(1 for num in combo if num in M1)
            count_M2 = sum(1 for num in combo if num in M2)
            count_M3 = sum(1 for num in combo if num in M3)
            
            count_N1 = sum(1 for num in combo if num in N1)
            count_N2 = sum(1 for num in combo if num in N2)
            count_N3 = sum(1 for num in combo if num in N3)
            
            count_R = sum(1 for num in combo if num in R)
            has_adjacent = check_adjacent_numbers(combo)
            
        #    f.write(f"  L1:L2:L3 = {count_L1}:{count_L2}:{count_L3}\n")
        #    f.write(f"  M1:M2:M3 = {count_M1}:{count_M2}:{count_M3}\n")
        #    f.write(f"  N1:N2:N3 = {count_N1}:{count_N2}:{count_N3}\n")
        #    f.write(f"  R集元素数: {count_R}\n")
        #    f.write(f"  有相邻数: {'是' if has_adjacent else '否'}\n")
        #    f.write("\n")
        
        print(f"\n结果已保存到文件: {filename}")
        print(f"文件包含 {len(combinations)} 个有效组合")

def main():
    """主函数"""
    print("=== 组合条件验证程序 ===")
    print()
    
    # 查找有效组合
    valid_combinations = find_valid_combinations()
    
    # 保存结果到文件
    if valid_combinations:
        save_to_file(valid_combinations)
        
        # 显示前几个组合
        print("\n输出10个有效组合:")
        for i, combo in enumerate(valid_combinations[:10], 1):
            print(f"{i}. {sorted(combo)}")
    else:
        print("\n未找到满足所有条件的组合！")

if __name__ == "__main__":
    main()
