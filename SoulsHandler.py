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
    
    def get_shikigami_data(self, columns):
        candidate_shikigami_name_list = ['不知火', '鬼切', '茨木', '酒吞', '玉藻前', '奕']

        shikigami_0 = [['不知火', 0, 3457, 100, 10, 150, 117, 0]]
        shikigami_1 = [['鬼切', 0, 3350, 100, 11, 160, 117, 0]]
        shikigami_2 = [['茨木', 0, 3216, 100, 10, 150, 112, 0]]
        shikigami_3 = [['酒吞', 0, 3136, 100, 10, 150, 113, 0]]
        shikigami_4 = [['玉藻前', 0, 3350, 100, 12, 160, 110, 0]]
        shikigami_5 = [['奕', 0, 3002, 100, 8, 150, 106, 0]]

        shikigami_list = [shikigami_0, shikigami_1, shikigami_2, shikigami_3, shikigami_4, shikigami_5]
        Shikigami = [['未選擇', 0, 0, 0, 0, 0, 0, 0]]

        print('請選擇此次想使用的式神: ')
        print(pd.Series(candidate_shikigami_name_list, index = range(1, len(candidate_shikigami_name_list) + 1)))
        
        target_shikigami_idx = int(input())
        
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
          
        return pd.DataFrame(Shikigami, columns=columns)
    
    def get_target_soul_name(self):
        candidate_souls_name_list = ['針女', '破勢', '心眼', '猙', '狂骨']
        print('請選擇此次想配置的御魂套裝')
        print(pd.Series(candidate_souls_name_list, index = range(1, len(candidate_souls_name_list) + 1)))
        
        return candidate_souls_name_list[int(input()) - 1]
    