import socket
import cv2
import numpy
import time
import sys
from PIL import Image, ImageDraw, ImageFont
from Serial_match import combination
from matplotlib import pyplot
def Connect(sock):
    try:
        sock.connect(address)
    except socket.error as msg:
        print(msg)

def SendVideo(frame, sock):
    # 停止0.1S 防止发送过快服务的处理不过来
    time.sleep(0.10)
    # cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中，'.jpg'表示将图片按照jpg格式编码
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)

    data = numpy.array(imgencode)  # 建立矩阵
    stringData = data.tostring()  # 将numpy矩阵转换成字符形式，以便在网络中传输

    # 先发送要发送的数据的长度
    sock.send(str.encode(str(len(stringData)).ljust(16)))
    # 发送图片数据
    sock.send(stringData)

    # 读取服务器返回值
    receive = sock.recv(1024)
    if len(receive): print(str(receive, encoding='utf-8'))
    return receive
def UI_draw1(img):
    o1, o2, o3 = img.shape;
    bound_1, bound_2, bound_3, bound_4 = o2 - 250, o2 - 1, 1, 250;
    cv2.rectangle(img, (bound_1, bound_3),
                  (bound_2, bound_4),
                  (0, 255, 255), 3)
    return img
def pipei(s):
    if s=='0a-1a-1a-1a-1':
        return numpy.array([-1])
    else:
        n = numpy.array([])
        i = 0;
        i1 = ''
        while i < len(s):
            if s[i] == 'a':
                n = numpy.append(n, int(i1))
                i1 = ''
                i = i + 1
            else:
                i1 = i1 + str(s[i])
                i = i + 1
        n = numpy.append(n, int(i1))
    return n
if __name__ == '__main__':

    address = ('218.194.36.185', 9002)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 压缩参数，15代表图像质量，越高代表图像质量越好为 0-100，默认95
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
    solution=combination()
    Connect(sock)
    index_2=-1;
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()  # ret=1 frame=读取到的一帧图像；ret=0读取失败
    matrix=numpy.array([])
    while ret:
        receive=SendVideo(frame, sock)
        receive=str(receive, encoding='utf-8')
        receive=pipei(receive)
        # print(receive[1])
        ret, frame = capture.read()  # ret=1 frame=读取到的一帧图像；ret=0读取失败
        # if len(receive)==1:
        #     UI_draw1(frame)
        #     cv2.imshow("camera", frame)
        #     print('certain')
        if len(receive)!=1:
            cv2.rectangle(frame, (int(receive[1]) - 10, int(receive[2]) - 10),
                          (int(receive[1]) + int(receive[3]) + 10, int(receive[2]) + int(receive[4]) + 10),
                          (0, 255, 0), 2)
            UI_draw1(frame)
            if receive[0]==97+22 and numpy.size(matrix)!=0:
                index_2=solution.print_2(matrix)
                frame = solution.UI_2(frame, index_2)
                matrix=numpy.array([])
            elif receive[0] == 97+22 and numpy.size(matrix) == 0:
                frame = solution.UI_2(frame, index_2)
                # pyplot.imshow(img)
                # pyplot.show()
                matrix = numpy.array([])
            else:
                matrix = numpy.append(matrix, receive[0])
            # pyplot.imshow(frame)
            # pyplot.show()
            # print(receive[3])
            cv2.imshow("camera", frame)
            time.sleep(0.02)
        if cv2.waitKey(10) == 27:
            break
            sock.close()
