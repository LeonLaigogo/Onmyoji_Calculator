# -*- coding: utf-8 -*-
from SoulsHandler import *
from OptimizationCalculator import *


class OptimizationHanlder:
    def __init__(self):
        self.souls_handler = SoulsHandler()
        self.opt_calculator = OptimizationCalculator(self.souls_handler)
        self.opt_result = []
        
    def get_opt_result(self, data):

        # 1. 取得最佳化所需資料
        Shikigami_data = self.souls_handler.get_shikigami_data(data.columns)
        target_soul_name = self.souls_handler.get_target_soul_name()
        candidate_souls_idx = self.souls_handler.get_sorted_candidate_idx(data)

        # 2. 計算結果
        self.opt_result = self.opt_calculator.get_optimization_soul_combination(Shikigami_data, data, candidate_souls_idx, target_soul_name)
        
        return self.opt_result

    def get_used_idx_set(self, used_rank):
        idx_set_idx = 3
        return self.opt_result[used_rank - 1][idx_set_idx]