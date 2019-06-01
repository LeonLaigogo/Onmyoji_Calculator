from collections import Counter

progress_threhold = [1000, 10000]

class OptimizationCalculator:
    def __init__(self, souls_handler):
        self.souls_handler = souls_handler
    
    def get_souls_name_count_dict(self, name_list):
        return dict(Counter([name for name in name_list]))

    def calculate_expected_damage(self, data, shi_atk):
        soul_atk = data['攻擊'] - shi_atk
        if data.shape[0] == 1:
            raise Exception('輸入資料必須先經過加總。')
        else:
            crit = data['爆擊%'] / 100
            return (shi_atk * (data['攻擊加成%'] / 100) + soul_atk) * [crit if crit <= 1 else 1][0] * (data['爆擊傷害%'] / 100) * ((100 + data['總傷害加成%']) / 100)
    
    def update_target_dict(self, soul_dict, input_soul_name, count):
        if input_soul_name in soul_dict.keys():
            return soul_dict.update({input_soul_name: soul_dict[input_soul_name] + count})
        else:
            return soul_dict.update({input_soul_name: 1})
    
    def get_optimization_soul_combination(self, Shikigami_data, data, candidate_souls_idx, target_soul_name):
        result = []       
        ttl_count = 1
        done_count = 0

        for i in range(len(candidate_souls_idx)):
            ttl_count *= len(candidate_souls_idx[i])
            
        print('此次候選御魂共有', ttl_count, ' 種組合。')
                      
        # 排序candidate_souls_idx
        candidate_souls_idx.sort(key = lambda x: len(x))
        
        for idx_1 in candidate_souls_idx[0]:            
            for idx_2 in candidate_souls_idx[1]:
                check_dict = self.get_souls_name_count_dict(data.loc[[idx_1, idx_2]]['御魂名稱'])
                if len(check_dict) == 2 and target_soul_name not in check_dict.keys():
                    continue  
                              
                for idx_3 in candidate_souls_idx[2]:
                    check_dict = self.get_souls_name_count_dict(data.loc[[idx_1, idx_2, idx_3]]['御魂名稱'])
                    
                    if target_soul_name not in check_dict.keys():
                        continue
                    
                    if len(check_dict) == 3:
                        continue      
                    
                    for idx_4 in candidate_souls_idx[3]:    
                        check_dict = self.get_souls_name_count_dict(data.loc[[idx_1, idx_2, idx_3, idx_4]]['御魂名稱'])
                                               
                        if check_dict[target_soul_name] == 1 or len(check_dict) == 3:
                            continue
                        
                        for idx_5 in candidate_souls_idx[4]:
                            check_dict = self.get_souls_name_count_dict(data.loc[[idx_1, idx_2, idx_3, idx_4, idx_5]]['御魂名稱'])
                            if len(check_dict) > 2 or check_dict[target_soul_name] < 3:
                                continue
                                                        
                            for idx_6 in candidate_souls_idx[5]:
                                idx_set = [idx_1, idx_2, idx_3, idx_4, idx_5, idx_6]
                                souls_name_count_dict = self.get_souls_name_count_dict(data.loc[idx_set]['御魂名稱'])
                                if len(souls_name_count_dict) > 2 or souls_name_count_dict[target_soul_name] < 4:
                                    continue
                                
                                candidate_data = data.loc[idx_set,]
                                done_count += 1                              
                                
                                # 3. 加入式神資料
                                candidate_data = candidate_data.append(Shikigami_data, ignore_index=True, sort=False)
                                
                                # 4. 加入御魂套裝效果
                                candidate_data = candidate_data.append(self.souls_handler.souls_tier_effect(souls_name_count_dict, candidate_data.columns), ignore_index=True)
                                
                                # 5. 計算期望傷害
                                sum_candidate_data = candidate_data.sum()
                                expected_damage = self.calculate_expected_damage(sum_candidate_data, Shikigami_data['攻擊'][0])
                                
                                # 6. 包裝結果
                                result.append([expected_damage, sum_candidate_data, candidate_data.loc[[0,1,2,3,4,5]], idx_set])   
                                
        sorted_result = sorted(result, key=lambda x: x[0], reverse=True)

        return sorted_result
