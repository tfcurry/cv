import numpy as np

float_formatter = lambda x: "%.2f" % x
np.set_printoptions(formatter={'float_kind': float_formatter})

class TimeSerial:
    def TimeSeriesSimilarityImprove(self,s1, s2):
        # 取较大的标准差
        sdt = np.std(s1, ddof=1) if np.std(s1, ddof=1) > np.std(s2, ddof=1) else np.std(s2, ddof=1)
        # print("两个序列最大标准差:" + str(sdt))
        l1 = len(s1)
        l2 = len(s2)
        paths = np.full((l1 + 1, l2 + 1), np.inf)  # 全部赋予无穷大
        sub_matrix = np.full((l1, l2), 0)  # 全部赋予0
        max_sub_len = 0

        paths[0, 0] = 0
        for i in range(l1):
            for j in range(l2):
                d = s1[i] - s2[j]
                cost = d ** 2
                paths[i + 1, j + 1] = cost + min(paths[i, j + 1], paths[i + 1, j], paths[i, j])
                if np.abs(s1[i] - s2[j]) < sdt:
                    if i == 0 or j == 0:
                        sub_matrix[i][j] = 1
                    else:
                        sub_matrix[i][j] = sub_matrix[i - 1][j - 1] + 1
                        max_sub_len = sub_matrix[i][j] if sub_matrix[i][j] > max_sub_len else max_sub_len

        paths = np.sqrt(paths)
        s = paths[l1, l2]
        return s, paths.T, [max_sub_len]


    def calculate_attenuate_weight(self,seqLen1, seqLen2, com_ls):
        weight = 0
        for comlen in com_ls:
            weight = weight + comlen / seqLen1 * comlen / seqLen2
        return 1 - weight
