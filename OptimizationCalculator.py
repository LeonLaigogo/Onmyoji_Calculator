from collections import Counter
import math

soul_name_idx = 0
progress_threhold = 50000

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
    
    def get_optimization_soul_combination(self, Shikigami_data, data, candidate_souls_idx, target_soul_name):
        result = []       
        ttl_count = 1
        done_count = 0

        for i in range(len(candidate_souls_idx)):
            ttl_count *= len(candidate_souls_idx[i])
        
        for idx_1 in candidate_souls_idx[0]:
            for idx_2 in candidate_souls_idx[1]:
                for idx_3 in candidate_souls_idx[2]:
                    for idx_4 in candidate_souls_idx[3]:
                        for idx_5 in candidate_souls_idx[4]:
                            for idx_6 in candidate_souls_idx[5]:
                                                                                             
                                # 1. 顯示進度
                                if ttl_count >= progress_threhold:
                                    done_count += 1
                                    if done_count % math.ceil((ttl_count / 10)) == 0:
                                        print('已完成', done_count / math.ceil((ttl_count / 10)) * 10, '%')
                                
                                # 2. 取得此次御魂組合。
                                candidate_data = data.iloc[[idx_1, idx_2, idx_3, idx_4, idx_5, idx_6],]

                                name_list = [data.iloc[idx_1, soul_name_idx], data.iloc[idx_2, soul_name_idx]
                                , data.iloc[idx_3, soul_name_idx], data.iloc[idx_4, soul_name_idx]
                                , data.iloc[idx_5, soul_name_idx], data.iloc[idx_6, soul_name_idx]]
                                
                                souls_name_count_dict = self.get_souls_name_count_dict(name_list)
                                
                                # 2-1. 檢查此次組合主御魂是否為目標御魂
                                if target_soul_name not in souls_name_count_dict or souls_name_count_dict[target_soul_name] < 4:
                                    break
                                
                                # 3. 加入式神資料
                                candidate_data = candidate_data.append(Shikigami_data, ignore_index=True, sort=False)
                                
                                # 4. 加入御魂套裝效果
                                candidate_data = candidate_data.append(self.souls_handler.souls_tier_effect(souls_name_count_dict, candidate_data.columns))
                                
                                # 5. 計算期望傷害
                                sum_candidate_data = candidate_data.sum()
                                expected_damage = self.calculate_expected_damage(sum_candidate_data, Shikigami_data['攻擊'][0])
                                
                                # 6. 包裝結果
                                result.append([expected_damage, sum_candidate_data, candidate_data.iloc[[0,1,2,3,4,5],]])                            
                                
        sorted_result = sorted(result, key=lambda x: x[0], reverse=True)
        
        return sorted_result