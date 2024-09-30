# xihe-scripts

本仓库提供了一组用于操作xihe数据的脚本工具，包括以下内容:

| 脚本 | 描述 |
| --- | --- |
| whitelist.py | 添加白名单 | 
| promotion_generator.py | 添加活动信息 | 

## 依赖

- python 3.12.3+
- openpyxl 3.1.5
- pymongo 4.8.0

## 安装

```sh
pip install -r requirements.txt
```

## 配置

配置mongo连接信息

mongo.json
```json
{
    "rwuser": "", // 用户名 
    "password": "", // 密码
    "database": "", // 操作的库
    "ip":"",
    "port": "",
    "cafile": ""  // ca文件
}
```

## 使用方法

### 添加白名单

单条添加
```sh
usage: whitelist.py manual [-h] -u USERNAME [-t TYPE] --start_time START_TIME --end_time END_TIME [--enabled ENABLED]

insert account manually

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        xihe account
  -t TYPE, --type TYPE  allowed module
  --start_time START_TIME
                        timestamp like "2024-06-12 09:27:00"
  --end_time END_TIME   timestamp like "2024-06-12 09:27:00"
  --enabled ENABLED     open or block permission [true/false]
```

批量添加
```sh
usage: whitelist.py batch [-h] -f FILENAME

insert accounts in batch

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        the excel of whitelist
```

批量添加文件模板请使用[这里](jupyter_template.xlsx)

### 添加活动信息

```sh
usage: promotion_generator.py [-h] -f FILENAME

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        the excel of promotions
```

批量添加文件模板请使用[这里](promotion_template.xlsx)
