## MQHunter
> 基于Python3.7 + Kivy2.0.0实现的MQTT协议辅助测试工具

### 软件介绍
- [x] 1.登录和订阅topic, 打印接收的消息,并记录到日志文件
- [x] 2.对同一主题最近2次消息的推送时间做间隔计算,帮助用户检查推送周期
- [ ] 3.保存用户配置信息到文件
- [ ] 4.自定义日志监控规则, 支持自定义设置目标值、时间间隔阈值, 并将触发阈值的日志另存到monitor_hunter.log方便排查
- [ ] 5.自定义mock数据：对目标主题发布自定义数据,支持随机数\定增数\特殊字符串等格式, 支持按定时或循环规则自动发布消息
- [ ] 6.打包为Windows平台的exe安装包、Mac平台的dmg安装包

## 测试及运行帮助
- **运行之前, 需准备Python3.7和docker环境**
##### 1. 安装Kivy和mqtt依赖库

```shell
//进入项目根目录
cd ./MQHunter
```

```shell
pip3 install -r ./requirements.txt
```

##### 2. 使用docker部署emqx服务(emqx是一个主流的开源MQTT服务器)

```shell
cd ./test
docker-compose -f ./docker-compose-emqx.yml up -d
```

##### 3. 新开一个命令行窗口,启动模拟生产者的脚本

```shell
python3 mock_producer.py
```

##### 4. 运行MQHunter GUI程序
```shell
cd ../src
python3 main.py
```


## License
[MIT](https://github.com/WenJieLife/MQHunter/blob/main/LICENSE)

copyright: © 2021-present Terry Li

## Thanks
在此特别感谢以下著名开源项目:
- [python](https://github.com/python/cpython)
- [kivy](https://github.com/kivy)
- [emqx](https://github.com/emqx/emqx)