import pandas as pd
from OptimizationHandler import *
from DisplayHandler import *
import time

data = pd.read_csv('soul_list.csv', encoding='big5')
data['總傷害加成%'] = pd.Series(0 * data.shape[0], index = data.index)

if __name__ == "__main__":

    print('=====簡易版御魂最佳化傷害計算機=====\n')
    print('Author: 聚星樓-五行化翠雨')
    print('Version: 1.0.1')
    print('Release Date: 2019-05-22\n')
    print('===================================')
    
    print('分析開始...\n')
    
    start_time = time.time()

    opt_handler = OptimizationHanlder()
    opt_result = opt_handler.get_opt_result(data)
    
    print('分析完畢^___^...\n')
    print('共有', len(opt_result), '筆結果，')
    print('總耗時: %8.2f minutes ---' % ((time.time() - start_time) / 60))        

    check_flag = 2
    
    while check_flag == 2:
        disp_handler = DisplayHandler()
        disp_handler.display_result(opt_result)
    
        check_flag = int(input('此次結果有你要的組合嗎? 還是想要看更多的結果?\n 1. 不了，我找到我要的組合了，謝謝 ^_^! \n 2. 我想再看更多的結果。\n 3. 我想要用剩下的御魂，幫第二支式神搭配。\n'))

    if check_flag == 3:
        print('準備二次分析...')
        data = data.drop(opt_handler.get_used_idx_set((int(input('請問會用掉第幾名的結果? ')) - 1)))

        print('分析開始...\n')
        start_time = time.time()
        opt_result = opt_handler.get_opt_result(data)

        print('分析完畢^___^...\n')
        print('共有', len(opt_result), '筆結果，')
        print('總耗時: %8.2f minutes ---' % ((time.time() - start_time) / 60))        
            
        check_flag_1 = 2
    
        while check_flag_1 == 2:
            disp_handler.display_result(opt_result)
        
            check_flag_1 = int(input('此次結果有你要的組合嗎? 還是想要看更多的結果?\n 1. 不了，我找到我要的組合了，謝謝 ^_^! \n 2. 我想再看更多的結果。\n'))

    input('請按任意鍵結束...')
    
