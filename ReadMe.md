## 备份程序  
### 配置文件(config.json)：  
```json
{
  "thread_num": 10,// 线程数量 1-32
  "file_log": true, // true/false 是否启用文件备份日志输出
  "file_log_only_modify": true,  // true/false 是否只输出有改变的文件日志
  "backup_path": [  // 备份的配置
    {
      "name": "工作文件",// 配置名称
      "from":"D:\\工作\\",// 需要备份的文件夹
      "to": "Z:\\backup\\工作\\",// 备份文件夹
      "ignore_path": [
      ],
      "ignore_file": [
      ]
    }, {
      "name": "代码文件",
      "from":"D:\\work\\",
      "to": "Z:\\backup\\",
      "ignore_path": [ //忽略文件夹 子目录
        "*.git",
        "*.idea"
      ],
      "ignore_file": [
        "*.log", // 忽略文件
        "*.exe"
      ]
    }
  ]
}

```
### 更新日志
#### v0.2 2023-09-05
1、文件已存在就覆盖  
2、添加文件日志输出  
展望：  
2、源文件删除，备份文件也同时删除  
#### v0.1 2023-09-01
1、可以多线程进行备份  
2、可以设定多个备份文件夹  
3、文件已存在就跳过（目前还未做覆盖）  
展望：  
1、文件已存在就覆盖  
2、源文件删除，备份文件也同时删除  