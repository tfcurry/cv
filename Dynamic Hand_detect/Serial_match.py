import numpy as np
import cv2
from Serial_similarity import TimeSerial
from PIL import Image, ImageDraw, ImageFont
#上四指头E，下四指头V，大拇指97-1
gesture_1=np.array([97+3,97]);  #指，大拇指
gesture_2=np.array([97+24,97+1,97+21,97+3]);  #6,
gesture_3=np.array([97+24,97-1,97+11]); #6，比心，八
gesture_4=np.array([97+4,97]); #E，大拇指
table=["你好","很高兴认识你","去医院怎么走","谢谢你"]
class combination:
    def print_2(self,s1):
        if np.size(s1)!=0:
            # 原始算法
            self.similarity=TimeSerial()
            distance12, paths12, max_sub12 = self.similarity.TimeSeriesSimilarityImprove((s1-97)/25,(gesture_1-97)/25)
            distance13, paths13, max_sub13 = self.similarity.TimeSeriesSimilarityImprove((s1-97)/25,(gesture_2-97)/25)
            distance14, paths14, max_sub14 = self.similarity.TimeSeriesSimilarityImprove((s1-97)/25, (gesture_3-97)/25)
            distance15, paths15, max_sub15 = self.similarity.TimeSeriesSimilarityImprove((s1-97)/25, (gesture_4-97)/25)
            # # 衰减系数
            # weight12 = self.similarity.calculate_attenuate_weight(len(s1), len(gesture_1), max_sub12)
            # weight13 = self.similarity.calculate_attenuate_weight(len(s1), len(gesture_2), max_sub13)
            # weight14 = self.similarity.calculate_attenuate_weight(len(s1), len(gesture_3), max_sub14)
            # weight15 = self.similarity.calculate_attenuate_weight(len(s1), len(gesture_4), max_sub15)
            matrix=np.array([distance12,distance13,distance14,distance15])
            print(s1)
            if 121 in s1 and np.size(s1)!=0:
                index=np.argmin(matrix)
            elif 100 in s1 and np.size(s1)!=0:
                index=0;
            elif np.size(s1)!=0:
                index=3;
            return index
        else:
            return -1
    def UI_2(self,img,index):
        if index==-1:
            return img
        else:
            o1, o2, o3 = img.shape;
            bound_1, bound_2, bound_3, bound_4 = o2 - 250, o2 - 1, 1, 250;
            cv2.rectangle(img, (bound_1, bound_3),
                          (bound_2, bound_4),
                          (0, 255, 255), 3)
            bound_5, bound_6= o2 - 248, 30;
            textSize = 15;
            textColor = (0, 255, 0);
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            # 创建一个可以在给定图像上绘图的对象
            draw = ImageDraw.Draw(img)
            # 字体的格式
            fontStyle = ImageFont.truetype(
                "simsun.ttc", textSize, encoding="utf-8")
            # 绘制文本
            draw.text((bound_5, bound_6), "手语识别:", textColor, font=fontStyle)
            draw.text((bound_5+80, bound_6), table[index]+'。', textColor, font=fontStyle)
            # 转换回OpenCV格式
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            return img
