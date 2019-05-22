import pandas as pd

class SoulsHandler:
    def __init__(self):
        pass     
        
    def get_candidate_souls(self, data):
        self.souls_dict = dict({'1':[], '2':[], '3':[], '4':[], '5':[], '6':[]})
        for idx, row in data.iterrows():
            self.souls_dict[str(row['御魂位置'])].append(soul(row['御魂名稱'], row['攻擊'], row['攻擊加成%'], row['爆擊%'], row['爆擊傷害%'], row['速度'], 0))
        return self.souls_dict    
    
    def get_sorted_candidate_idx(self, data):
        sorted_data = data.sort_values(by=['御魂位置'])
        return [sorted_data[sorted_data['御魂位置'] == location + 1].index.values for location in range(6)]
        
    def souls_tier_effect(self, dict_soul_count, col_names):
        p_atk = 0
        crit = 0
        p_ttl_damage = 0
        for soul_name, soul_count in dict_soul_count.items():
            if soul_count < 2:
                pass
            elif 2 <= soul_count <= 6:
                if soul_name in ['破勢', '針女', '網切', '三味']:
                    crit += 15
                elif soul_name in ['陰摩羅', '心眼', '鳴屋', '猙', '輸入道', '蝠翼', '狂骨']:
                    p_atk += 15
                elif soul_name == '荒骷髏':
                    p_ttl_damage += 10
                else:
                    raise Exception('目前不支援該御魂。')
            else:
                print('設定檔案中的 ', soul_name, '有 ', soul_count, '顆。')
                raise Exception('御魂數量不該超過七顆。')
                
        return pd.DataFrame([['套裝加成', 0, 0, p_atk, crit, 0, 0, p_ttl_damage]], columns=col_names)