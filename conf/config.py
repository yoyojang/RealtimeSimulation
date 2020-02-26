vissim_file_path = r'D:\Program\RealtimeSimulation\zsvissim\Road ziyun.inpx'

vissim_version = r'vissim.vissim'

volume_file = r'D:\Program\RealtimeSimulation\db\volume'
routerate_file = r'D:\Program\RealtimeSimulation\db\route_rate'
signal_program = r'D:\Program\RealtimeSimulation\db\offline_signal_program'

# 存储数据库配置
datacollection_file = r'D:\Program\RealtimeSimulation\db\evaluation_datacollection'
traveltime_file = r'D:\Program\RealtimeSimulation\db\evaluation_traveltime'
movement_file = r'D:\Program\RealtimeSimulation\db\evaluation_movement'

VolumeHistory = r'D:\Program\RealtimeSimulation\db\VolumeList'
RateHistory = r'D:\Program\RealtimeSimulation\db\RateList'

update_interval_time = 5*60  # 数据更新间隔时间， seconds
output_multiple = 1 # 评价输出间隔时间，是更新时间的整数倍
run_total_time = 22*60*60 #seconds 0为总是运行


#编辑对应配时文件
intersection_info = {
    '双麒路':[1, [3,1,1,1,2,2,3,3], 'zs033.sig'],
    '永丰大道':[2, [3,1,1,2,3,4,4,5], 'zs022.sig'],
    '永智路':[3, [3,1,2,2,3,3,4,4], 'zs034.sig'],
    '运粮河西路':[4, [3,1,1,2,3,4,4,5], 'zs035.sig'],
}


# 是否存数据库
StoreDBFlag = True #true 为存储入数据库

