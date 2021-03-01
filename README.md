## MQHunter
> Python 3.7 + Kivy 2.0.0

### 软件介绍
- [x] 1.订阅并记录MQTT服务器的日志
- [x] 2.计算相同主题消息的推送时间间隔,帮助排查问题
- [] 3.保存用户配置信息到文件
- [] 4.自定义日志监控规则, 支持自定义设置目标值、时间间隔阈值, 并将触发阈值的日志另存到monitor_hunter.log方便排查
- [] 5.自定义mock数据：设置模拟producer数据，自动按自定义规则发布数据
- [] 6.打包为Windows平台的exe安装包、Mac平台的dmg安装包

## 测试及运行帮助
##### 1. 本地已有Python3环境, 首先安装依赖
```shell
cd ./MQHunter
pip3 install -y ./requirements.txt
```

##### 2. 使用docker启动emq服务

```shell
cd ./MQHunter/test
docker-compose -f ./docker-compose-emq.yml up -d
```

##### 3. 在新窗口中运行模拟生产者的脚本

```shell
cd ./MQHunter/test
python3 mock_producer.py
```

##### 4. 运行MQHunter
```shell
cd ./MQHunter/src
python3 main.py
```

## Thanks
在此特别感谢以下著名开源项目:
- [python](https://github.com/python/cpython)
- [kivy](https://github.com/kivy)


## 版权声明
[MIT](https://github.com/WenJieLife/WuKong/blob/main/LICENSE)

copyright: © 2021-present Terry Li