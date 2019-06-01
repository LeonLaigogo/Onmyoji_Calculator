import pandas as pd

class DisplayHandler:
    def __init__(self):
        self.name_idx = 0
        self.position_idx = 1
        self.atk_idx = 2
        self.p_atk_idx = 3
        self.p_crit_idx = 4
        self.p_critd_idx = 5
        self.speed_idx = 6
    
    def display_target_overview(self, idx, expected_damage, ttl_status_data):
        print('\n第 ' + str(idx + 1) + ' 名結果: ')
        print('期望傷害: ', round(expected_damage, 6))
        print('總爆擊%: ', ttl_status_data['爆擊%'])
        print('總爆擊傷害%: ', ttl_status_data['爆擊傷害%'])
        print('總速度: ', ttl_status_data['速度'])
        
    def display_align_result(self, data): 
        print('\n御魂組合:')        
        print(data.columns.values[self.name_idx], ' ', data.columns.values[self.position_idx], ' ', data.columns.values[self.atk_idx], ' ', 
              data.columns.values[self.p_atk_idx], ' ', data.columns.values[self.p_crit_idx], ' ', 
              data.columns.values[self.p_critd_idx], ' ', data.columns.values[self.speed_idx])
        
        for i in range(6):
            print('{:6s} {:7d} {:8.2f} {:8d} {:8d} {:8d} {:8d}'.format(
                   data.iloc[i,self.name_idx], data.iloc[i,self.position_idx], 
                   data.iloc[i,self.atk_idx], data.iloc[i,self.p_atk_idx], 
                   data.iloc[i,self.p_crit_idx], data.iloc[i,self.p_critd_idx], data.iloc[i,self.speed_idx]))

    def is_satisfy_result_type(self, ttl_status_data, result_type):
        if result_type == 1:
            return ttl_status_data['爆擊%'] >= 100
        elif result_type == 2:
            return ttl_status_data['速度'] > 128
        else:
            return True
                   
    def display_result(self, opt_result):
        rank_count = int(input('你想要看前幾名?\n'))
        result_type = int(input('特殊要求:\n 1. 我只看滿爆擊的 \n 2. 我只看超星的(速度>128) \n 3. 我全部都要(握拳)\n'))
                
        if rank_count > len(opt_result):
            raise Exception('沒有這麼多結果喔~\n')
            
        display_count = 0
        idx = 0
        while display_count < rank_count:
            if self.is_satisfy_result_type(opt_result[idx][1], result_type):
                display_count += 1
                self.display_target_overview(idx, opt_result[idx][0], opt_result[idx][1])
                self.display_align_result(opt_result[idx][2].iloc[:,[0,1,2,3,4,5,6]].sort_values(by=['御魂位置']))
                 
            idx +=1

             
             
             