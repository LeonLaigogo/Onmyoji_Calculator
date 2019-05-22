import pandas as pd
from SoulsHandler import *
from OptimizationCalculator import *
from DisplayHandler import *

data = pd.read_csv('soul_list.csv', encoding='big5')
data['總傷害加成%'] = pd.Series(0 * data.shape[0], index = data.index)

candidate_souls_name_list = ['針女', '破勢']
candidate_shikigami_name_list = ['鬼切', '茨木', '酒吞', '玉藻前']

shikigami_1 = [['鬼切', 0, 3350, 100, 11, 160, 117, 0]]
shikigami_2 = [['茨木', 0, 3216, 100, 10, 150, 112, 0]]
shikigami_3 = [['酒吞', 0, 3136, 100, 10, 150, 113, 0]]
shikigami_4 = [['玉藻前', 0, 3350, 100, 12, 160, 110, 0]]

shikigami_list = [shikigami_1, shikigami_2, shikigami_3, shikigami_4]
Shikigami = [['未選擇', 0, 0, 0, 0, 0, 0, 0]]

if __name__ == "__main__":

    print('=====簡易版御魂最佳化傷害計算機=====\n')
    print('Author: 聚星樓-五行化翠雨')
    print('Version: 1.0.1')
    print('Release Date: 2019-05-22\n')
    print('===================================')
   
    target_shikigami_idx = int(input('請選擇此次想使用的式神 \n 1. 鬼切\n 2. 茨木\n 3. 酒吞\n 4. 玉藻前\n 5. 其他\n'))
    if target_shikigami_idx > len(shikigami_list) + 1:
        raise Exception('輸入錯誤!\n')
    elif target_shikigami_idx == len(shikigami_list) + 1:
        print('請輸入式神自身機體資訊')
        atk = int(input('攻擊力: '))
        crit = int(input('爆擊%: '))
        critd = int(input('爆擊傷害%: '))
        speed = int(input('速度: '))
        Shikigami = [['未選擇', 0, atk, 100, crit, critd, speed, 0]]
    else:
        Shikigami = shikigami_list[target_shikigami_idx - 1]
      
    Shikigami_data = pd.DataFrame(data = Shikigami, columns=data.columns)
    souls_handler = SoulsHandler()
    opt_calculator = OptimizationCalculator(souls_handler)

    target_soul_name_idx = int(input('請選擇此次想配置的御魂套裝編號 \n 1. 針女\n 2. 破勢\n 3. 猙\n 4. 輸入道\n'))
    
    print('分析開始...\n')
    candidate_souls_idx = souls_handler.get_sorted_candidate_idx(data)
    opt_result = opt_calculator.get_optimization_soul_combination(Shikigami_data, data, candidate_souls_idx, candidate_souls_name_list[target_soul_name_idx - 1])
    
    print('分析完畢^___^...\n')
    print('共有', len(opt_result), '筆結果，')
            
    display = DisplayHandler()
    check_flag = 2
    
    while check_flag == 2:
        rank_count = int(input('你想要看前幾名?\n'))
        if rank_count > len(opt_result):
            raise Exception('沒有這麼多結果喔~\n')
        
        for idx in range(rank_count):
            display.display_target_overview(idx, opt_result[idx][0], opt_result[idx][1])
            display.display_align_result(opt_result[idx][2].iloc[:,[0,1,2,3,4,5,6]], )
    
        check_flag = int(input('此次結果有你要的組合嗎? 還是想要看更多的結果?\n 1. 不了，我找到我要的組合了，謝謝 ^_^! \n 2. 我想再看更多的結果。\n'))
    

    input('請按任意鍵結束...')
    
