import cv2 as cv
import numpy as np
import pandas as pd
from random import randint
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys
import time
import ast
# 处理字体问题
plt.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['axes.unicode_minus'] = False
print("by: Dennis Ning & Hao Xu")
print("导入操作：from trackerao import tracker as ao")
print("获取操作介绍请运行函数：ao.t_help()")
def t_help():
    print('如果想设置锚点，请将第一个点设置为锚点，个体0为锚点数据')
    print('函数功能介绍：')
    print('1. start(path) 运行该函数解析视频，path为视频相对路径，要首先运行')
    print('2. stitch(name) 进行数据拼接，name给保存的文件起个名字，不可与start()同时使用，要首先运行')
    print('3. count_length(dpi,figsize) 计算路径长度和速度，dpi 为图片像素，figsize为图片大小')
    print('4. map_heatmap(dpi, figsize) 绘制每个个体的热图')
    print('5. map_heatmap_v(dpi, figsize, vmax) 调整标尺后每个个体的热图，vmax 为标尺最大值')
    print('6. map_key(dpi, figsize) 绘制所有个体的热图')
    print('7. map_key_v(dpi, figsize, vmax) 调整标尺后所有个体的热图，vmax 为标尺最大值')
    print('8. touch(min_dis, dpi, figsize) 蚂蚁间接触数据绘图， min_dis为距离在多少以内判定为接触')
    print('9. anchor(dis) 绘制所有蚂蚁与锚点的距离图, dis 为距离小于多少时算作个体在锚点范围内')
    print('图文教程链接：https://shimo.im/docs/PXv68QRcyrKvYygY/ ')
    
    
# 追踪蚂蚁主函数
def start(path):
    # 创建文件夹
    global file_name,file_path
    file_name = path[2:-4] + "_信息记录"
    file_path = './'+ file_name
    isExists=os.path.exists(file_path)
    if not isExists:
        os.mkdir(file_path)
    
    global touch_path
    touch_path = file_path + '/距离与触碰'
    isExists=os.path.exists(touch_path)
    if not isExists:
        os.mkdir(touch_path)
    
    # 保存打印信息
    sys.stdout = open(file_path+'/'+file_name+'.txt','a',encoding='utf-8')
    
    # 打印当前时间
    localtime = time.asctime( time.localtime(time.time()) )
    print("*"*30)
    print(localtime)
    
    # 记录时间
    starttime = datetime.datetime.now()
    
    # 声明变量
    global number, vecPoints
    number = int(input('please input the number of objects:'))
    area = np.zeros((number, 4))
    ROI_area = []
    ROI_local = np.zeros((number, 4))
    roi_hist = []
    colors = []
    hsv_roi = []
    track_window = []
    vecPoints = []

    print("--------- Python OpenCV Tutorial ---------")
    # 读取视频
    path_video = path
    video_name = path_video[2:-4]
    cap = cv.VideoCapture(path_video)
    # 读取第一帧
    ret, frame = cap.read()
    fourcc = cv.VideoWriter_fourcc(*'XVID')  # 保存视频的编码

    # ROI_cricle = cv.selectROI("ROI frame", frame, True, False)
    imgbd = np.zeros((int(frame.shape[0]), int(frame.shape[1]), 3), np.uint8)

    # 选择ROI区域
    for i in range(number):
        gROI = cv.selectROI("ROI frame", frame, True, False)
        temp = []
        vecPoints.append(temp)
        x, y, w, h = gROI
        track_window.append((x, y, w, h))
        ROI_local[i] = [gROI[1], gROI[1] + gROI[3], gROI[0], gROI[0] + gROI[2]]
        area[i] = [0, frame.shape[1], 0, frame.shape[0]]
        ROI_area.append(frame[gROI[1]:gROI[1] + gROI[3], gROI[0]:gROI[0] + gROI[2]])
        cv.imshow("ROI{}".format(i), ROI_area[i])
        hsv_roi.append(cv.cvtColor(ROI_area[i], cv.COLOR_BGR2HSV))
        # 按照以下格式增加不同颜色的蚂蚁
        # 标注蚂蚁时按照下面颜色的顺序进行标注
#         if i == 0:
#             # 暗红
#             # 参数 hsv色域的roi，hsv色域内颜色的参数范围
#             mask1 = cv.inRange(hsv_roi[i], (0, 253, 126), (0, 255, 129))
#             roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask1, [180], [0, 180]))

#         if i == 0:
#             # 大红
#             mask2 = cv.inRange(hsv_roi[i], (0, 255, 255), (1, 255, 255))
#             roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask2, [180], [0, 180]))

        if i == 0:
            # 亮黄
            mask2 = cv.inRange(hsv_roi[i], (26, 254, 254), (34, 255, 255))
            roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask2, [180], [0, 180]))
            
#         if i == 0:
#             # 暗黄
#             mask2 = cv.inRange(hsv_roi[i], (26, 250, 124), (34, 255, 132))
#             roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask2, [180], [0, 180]))            

        if i == 1:
            # 亮绿
            mask2 = cv.inRange(hsv_roi[i], (57, 253, 253), (63, 255, 255))
            roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask2, [180], [0, 180]))

#         if i == 0:
#             # 暗绿色
#             mask3 = cv.inRange(hsv_roi[i], (58, 250, 120), (61, 255, 128))
#             roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask3, [180], [0, 180]))       

        if i == 2:
            # 亮青色
            mask2 = cv.inRange(hsv_roi[i], (84, 251, 251), (94, 255, 255))
            roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask2, [180], [0, 180]))
            
#         if i == 5:
#             # 暗青色
#             mask4 = cv.inRange(hsv_roi[i], (89, 255, 127), (91, 255, 129))
#             roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask4, [180], [0, 180]))

        if i == 3:
            # 蓝
            mask5 = cv.inRange(hsv_roi[i], (118, 255, 255), (122, 255, 255))
            roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask5, [180], [0, 180]))

        if i == 4:
            # 海蓝
            mask6 = cv.inRange(hsv_roi[i], (118, 240, 125), (122, 255, 132))
            roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask6, [180], [0, 180]))

        if i == 5:
            # 亮紫
            mask7 = cv.inRange(hsv_roi[i], (148, 253, 253), (152, 255, 255))
            roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask7, [180], [0, 180]))

        if i == 6:
            # 暗紫
            mask8 = cv.inRange(hsv_roi[i], (148, 253, 126), (152, 255, 130))
            roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask8, [180], [0, 180]))
            
#         if i == 0:
#             # 黑色
#             mask8 = cv.inRange(hsv_roi[i], (0, 0, 0), (1, 1, 1))
#             roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask8, [180], [0, 180]))
            
        
#         if i == 10:
#             # 灰色
#             mask8 = cv.inRange(hsv_roi[i], (0,0,127), (1,1,129))
#             roi_hist.append(cv.calcHist([hsv_roi[i]], [0], mask8, [180], [0, 180]))

        cv.normalize(roi_hist[i], roi_hist[i], 0, 255, cv.NORM_MINMAX)

    term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

    while True:
        # 每个标记框行驶路径列表
        dst = []
        ret, frame = cap.read()
        i = 0
        if ret is False:
            break;
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        for i in range(number):
            dst = cv.calcBackProject([hsv], [0], roi_hist[i], [0, 180], 1)
            # 搜索更新roi区域
            ret, track_box = cv.CamShift(dst, track_window[i], term_crit)
            # 可变角度的矩形框
            pts = cv.boxPoints(ret)
            pts = np.int0(pts)
            cv.polylines(frame, [pts], True, (0, 255, 0), 2)
            # 更新窗口
            track_window[i] = track_box
            vecPoints[i].append((int(track_box[0] + track_box[2] / 2), int(track_box[1] + track_box[3] / 2)))
            # 绘制窗口CAM，目标椭圆图
            cv.ellipse(frame, ret, (0, 0, 255), 3, 8)
        cv.imshow('Demo', frame)
        k = cv.waitKey(50) & 0xff
        if k == 27:
            break
        else:
            cv.imwrite(chr(k) + ".jpg", frame)

    for i in range(len(vecPoints)):
        print("蚂蚁-{}行动路径长度:".format(i), len(set(vecPoints[i])))
        print("蚂蚁-{}行动路径数据:".format(i), vecPoints[i])
        #  记录时间
        endtime = datetime.datetime.now()
        if len(vecPoints[i]) > 0:
            for j in range(len(vecPoints[i]) - 1):
                cv.line(imgbd, vecPoints[i][j], vecPoints[i][j + 1], (255, 255, 255), 1, 8, 1)
    print ("消耗时长：",(endtime - starttime).seconds)
    black_image_path = './'+ file_name + '/' + '轨迹图.jpg'
    cv.imwrite(black_image_path, imgbd)
    cv.imshow(video_name, imgbd)
    cv.waitKey(0)
    cv.destroyAllWindows()
    cap.release()
    
    # 关闭打印记录
    # sys.stdout.close()
    
# 数据拼接代码
def stitch(name): 
    global vecPoints
    vecPoints = []
    state = 1
    while state == 1:
        vecPoints.append(ast.literal_eval(input("请添加坐标数据，一次添加一只。如果有锚点，请在第一个添加。按回车完成添加")))
        print("已传入数据条数：",len(vecPoints))
        state = int(input("继续添加输入 1 ，结束添加输入 0 "))
    # 创建保存文件夹
    
    global file_name,file_path,touch_path,number
    file_name = str(name)+"信息记录"
    file_path = './'+ file_name
    isExists=os.path.exists(file_path)
    if not isExists:
        os.mkdir(file_path)

    touch_path = file_path + '/距离与触碰'
    isExists=os.path.exists(touch_path)
    if not isExists:
        os.mkdir(touch_path)

    number = len(vecPoints) 

    # 修改打印指向，保存打印信息
    sys.stdout = open(file_path+'/'+file_name+'.txt','a',encoding='utf-8')

    # 打印当前时间
    localtime = time.asctime( time.localtime(time.time()) )
    print("*"*30)
    print(localtime)

    for i in range(len(vecPoints)):
        print("蚂蚁-{}行动路径长度:".format(i), len(set(vecPoints[i])))
        print("蚂蚁-{}行动路径数据:".format(i), vecPoints[i])    
    
    
# 测算函数
def count_length(dpi,figsize):
    for i in range(number):
        print("第%d条路径长度："%i,len(set(vecPoints[i]))," 像素")
        print("第%d条路径用时："%i,len(vecPoints[i])," 帧" )
        print("第%d条路径速度："%i,len(set(vecPoints[i]))/len(vecPoints[i])," 像素/帧" )
        print("-"*30)

        
    # 速度，长度数据列表
    speed_list = []
    length_list = []
    name_list = []
    for i in range(number):
        length_list.append(len(set(vecPoints[i])))
        speed_list.append(len(set(vecPoints[i]))/len(vecPoints[i]))
        name_list.append('第'+ str(i) +'只')

    # 设置风格，seaborn有5种基本风格，context表示环境
    sns.set(style="white", context="notebook")
    # 处理中文问题
    sns.set_style('whitegrid', {'font.sans-serif':['simhei', 'Arial']})

    y_sp = speed_list
    y_len = length_list
    x = name_list

    # 绘制移动距离图

    plt.figure(dpi=dpi,figsize=figsize)
    ax = sns.barplot(x, y_len, palette="BuPu_r")
    title = '所有个体移动距离'
    ax.set_title(title)
    fig_sp_name = '移动长度'
    fig_sp_path = './' + file_name + '/' + fig_sp_name + '.jpg'
    plt.savefig(fig_sp_path)
    plt.show()
    
    
#  绘制分图函数
# 集成制图 100*100格图
def map_heatmap(dpi, figsize):
    for num in range(number):
        X_NUM = []
        Y_NUM = []
        # 建立空坐标系
        for n in vecPoints:
            for a in n:
                X_NUM.append(a[1])
                Y_NUM.append(a[0])
        # 缩小网格
        lenx = max(X_NUM)/100
        leny = max(Y_NUM)/100
        backg = np.zeros((100, 100))
        for a in vecPoints[num]:
            for b in range(100):
                for c in range(100):
                    # 打点
                    if (a[1] > (b-1)*lenx) and (a[1] <= b*lenx) and (a[0] > (c-1)*leny) and (a[0] <= c*leny):
                        backg[b,c] += 1
        plt.figure(dpi=dpi,figsize=figsize)
        title = '第%d只'%num
        ax = sns.heatmap(backg, cmap="Reds")
        ax.set_title(title)
        # 保存
        fig_name = "第%d只热图"%num
        fig_path = './'+ file_name + '/'+ fig_name + '.jpg'
        plt.savefig(fig_path)
        plt.show()

            
            
# 绘制总图函数
def map_key(dpi, figsize):
    X_NUM = []
    Y_NUM = []
    # 建立空坐标系
    for n in vecPoints:
        for a in n:
            X_NUM.append(a[1])
            Y_NUM.append(a[0])
    # 缩小网格
    lenx = max(X_NUM)/100
    leny = max(Y_NUM)/100
    backg = np.zeros((100, 100))
    for n in vecPoints:
        for a in n:
            for b in range(100):
                for c in range(100):
                    # 打点
                    if (a[1] > (b-1)*lenx) and (a[1] <= b*lenx) and (a[0] > (c-1)*leny) and (a[0] <= c*leny):
                        backg[b,c] += 1
    plt.figure(dpi=dpi,figsize=figsize)
    ax = sns.heatmap(backg, cmap="Reds")
    title = '总图'
    ax.set_title(title)
    # 保存
    fig_name = '总图'
    fig_path = './' + file_name + '/' + fig_name + '.jpg'
    plt.savefig(fig_path)
    plt.show()


# 可调标尺总图
def map_key_v(dpi, figsize, vmax):
    X_NUM = []
    Y_NUM = []
    # 建立空坐标系
    for n in vecPoints:
        for a in n:
            X_NUM.append(a[1])
            Y_NUM.append(a[0])
    # 缩小网格
    lenx = max(X_NUM)/100
    leny = max(Y_NUM)/100
    backg = np.zeros((100, 100))
    for n in vecPoints:
        for a in n:
            for b in range(100):
                for c in range(100):
                    # 打点
                    if (a[1] > (b-1)*lenx) and (a[1] <= b*lenx) and (a[0] > (c-1)*leny) and (a[0] <= c*leny):
                        backg[b,c] += 1
    plt.figure(dpi=dpi,figsize=figsize)
    ax = sns.heatmap(backg, vmax = vmax, cmap="Reds")
    title = '总图_标尺调整'
    ax.set_title(title)
    # 保存
    fig_name = '标尺调整_总图'
    fig_path = './' + file_name + '/' + fig_name + '.jpg'
    plt.savefig(fig_path)
    plt.show()


# 可调标尺分图
def map_heatmap_v(dpi, figsize, vmax):
    for num in range(number):
        X_NUM = []
        Y_NUM = []
        # 建立空坐标系
        for n in vecPoints:
            for a in n:
                X_NUM.append(a[1])
                Y_NUM.append(a[0])
        # 缩小网格
        lenx = max(X_NUM)/100
        leny = max(Y_NUM)/100
        backg = np.zeros((100, 100))
        for a in vecPoints[num]:
            for b in range(100):
                for c in range(100):
                    # 打点
                    if (a[1] > (b-1)*lenx) and (a[1] <= b*lenx) and (a[0] > (c-1)*leny) and (a[0] <= c*leny):
                        backg[b,c] += 1
        plt.figure(dpi=dpi,figsize=figsize)
        ax = sns.heatmap(backg, vmax = vmax, cmap="Reds")
        title = '第%d只_统一标尺'% num
        ax.set_title(title)
        # 保存
        fig_name = "第%d只 热图_统一标尺" % num
        fig_path = './'+ file_name + '/'+ fig_name + '.jpg'
        plt.savefig(fig_path)
        plt.show()

# 蚂蚁之间距离与触碰模块
def touch(min_dis, dpi, figsize):
    # 取出目标蚂蚁点
    for mnum in range(number):
        data_dis = pd.DataFrame(columns=('group','distance','time'))
        m_list = []
        # 与某只蚂蚁接触总时间列表
        touch_t_time = []
        touch_t_name = []

        # 将目标蚂蚁数据放入列表中
        for mi in vecPoints[mnum]:
            m_list.append([mi[0],mi[1]])
        # 计算该蚂蚁与其他蚂蚁的动态欧式距离
        for num in range(number):
            print('-'*20)
            if num != mnum:
                # 构建其他蚂蚁列表
                n_list = []
                # 与其他蚂蚁接触列表
                # 建立数值表
                touch_list = []
                # 持续时间列表
                touch_time_list = []
                for ni in vecPoints[num]:
                    n_list.append([ni[0],ni[1]])

                # 两个列表构建完成，开始计算欧式距离
                for i in range(len(m_list)):
                    m = np.array(m_list[i])
                    n = np.array(n_list[i])
                    dis = np.sqrt(np.sum((m - n) ** 2))

                    # 判断是否挨着
                    if dis < min_dis:
                        touch_list.append(1)
                    else:
                        touch_list.append(0)
                    # 将距离添加入表格
                    p_name = '%d'%mnum + '-' + '%d'%num
                    data_dis = data_dis.append([{'group':p_name,'distance':dis,'time':i}], ignore_index=True)

                # 向持续时间列表中添加数值
                tc = 0
                for i in touch_list:
                    if i == 1:
                        tc += 1
                    elif tc != 0 and i==0:
                        touch_time_list.append(tc)
                        tc = 0
#                 if len(touch_time_list) == 0:
#                     touch_time_list.append(0)

                # 绘制两只蚂蚁之间的接触次数时间图
                if len(touch_time_list) != 0:
                    plot_touch_name = []
                    for i in range(len(touch_time_list)):
                        plot_touch_name.append('第'+ str(i+1) +'次') 
                    plt.figure(dpi=dpi,figsize=figsize)
                    ax = sns.barplot(x= plot_touch_name, y=touch_time_list)
                    title = '第%d只 与第%d只 接触时间'%(mnum,num)
                    ax.set_title(title)
                    fig_touch_name = '第%d只 与第%d只 接触时间'%(mnum,num)
                    fig_touch_path = touch_path + '/' + fig_touch_name + '.jpg'
                    plt.savefig(fig_touch_path)
                    plt.show()

#                 print('第%d只与第%d只接触时间'%(mnum,num),touch_time_list)
#                 print('第%d只与第%d只接触总时间'%(mnum,num),sum(touch_time_list))
                print('第%d只 与第%d只 接触次数'%(mnum,num),len(touch_time_list))

                touch_t_time.append(sum(touch_time_list))
                touch_t_name.append(num)
        if number >= 2:
            # 绘制距离图
            plt.figure(dpi=dpi,figsize=figsize)
            ax = sns.lineplot(x='time',y='distance',hue='group',data = data_dis)
            title = '第%d只 与其他蚂蚁的距离'%(mnum)
            ax.set_title(title)
            fig_dis_name = '第%d只 与其他蚂蚁的距离'%mnum
            fig_dis_path = touch_path + '/' + fig_dis_name + '.jpg'
            plt.savefig(fig_dis_path)
            plt.show()


            # 绘制接触时间总图
            ax = sns.barplot(x= touch_t_name, y=touch_t_time)
            title = '第%d只 与其他蚂蚁接触总时间'%(mnum)
            ax.set_title(title)
            fig_touch_name = '第%d只 与其他蚂蚁接触总时间'%mnum
            fig_touch_path = touch_path + '/' + fig_touch_name + '.jpg'
            plt.savefig(fig_touch_path)
            plt.show()

def anchor(dis):
    ave_distance = []
    stay_time = []
    for num in range(number):

        if num != 0:
            atrack_list = []
            m = np.array([vecPoints[0][0][0],vecPoints[0][0][1]])
            
            # 得到距锚点距离列表
            for i in vecPoints[num]:
                n = np.array([i[0],i[1]])
                dis = np.sqrt(np.sum((m - n) ** 2))
                atrack_list.append(dis)

            # 绘制目标距离锚点距离动态图，获取x值列表
            x_list = []
            for c in range(len(atrack_list)):
                x_list.append(c+1)

            # 绘图
            ax = sns.lineplot(x=x_list, y=atrack_list)
            title = "第%d只 距离锚点距离"%(num)
            ax.set_title(title)

            # 保存图片
            fig_name = "第%d只 距离锚点距离"%(num)
            fig_path = './'+ file_name + '/'+ fig_name + '.jpg'
            plt.savefig(fig_path)
            plt.show()

            # 求平均值
            sum = 0
            for item in atrack_list:
                sum += item
            avg_d = sum/len(atrack_list)
            ave_distance.append(avg_d)
            print("第%d只 距离锚点平均距离为:"%(num),avg_d)
            
            # 绘制目标在锚点范围内停留时间图
            # 获取停留时间列表
            s_time = 0
            for i in atrack_list:
                if i < dis:
                    s_time += i
            stay_time.append(s_time)
                    
            
    # 绘制所有蚂蚁距离锚点的平均距离图
    name_list = []
    for i in range(number-1):
        name_list.append('第'+ str(i+1) +'只')    
    ax = sns.barplot(x= name_list, y=ave_distance, palette="Blues_d")
    title = '所有个体距离锚点平均距离'
    ax.set_title(title)
    fig_sp_name = '所有个体距离锚点平均距离'
    fig_sp_path = './' + file_name + '/' + fig_sp_name + '.jpg'
    plt.savefig(fig_sp_path)
    plt.show()
    
    # 绘制目标在锚点范围内停留时间图
    ax1 = sns.barplot(x= name_list, y=stay_time, palette="Blues_d")
    title = '所有个体在锚点范围内停留时间'
    ax1.set_title(title)
    fig_st_name = '所有个体在锚点范围内停留时间'
    fig_st_path = './' + file_name + '/' + fig_st_name + '.jpg'
    plt.savefig(fig_st_path)
    plt.show()