#测试说明
##项目结构说明
```text
    - assets 
        - img 按钮等截图
    - config 存放一些配置文件
        - 
    - base airtest相关操作封装
    - page 游戏内一些页面操作的封装
    - testcase 各类检查的测试用例
    - util 工具类，如文件、日志处理等
    - logs 日志
    - report 报告目录
    - run.py 执行文件（执行testcase）

```

##后续编写说明
- 因该结构以及单元测试是依据unittest进行编写的，所以结构规则也需按照其规则，用例以test开头
- 如需要更改结构或者项目名称，需要对起内部root_path进行一并更改
- 因目前没有使用其poco的单元测试pocoui，如需更改，请参照其官方文档进行修改编写
- yaml文件暂时没有用上，暂时可以无视它

##运行准备
-环境准备
```text
    1）python3.6以上
    2）pip install -r requirements.txt
    3）如遇点击不到的设备，建议更换2400*1080分辨率的手机
