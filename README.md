# i至诚自动化打卡签到
基于requests的i至诚打卡签到，自用

## 友情链接 可能比我的更好用，我的workflow配置照搬他的代码
https://github.com/Lin1031/izhicheng

## 使用方法
### 本地/服务器使用:
安装Python后，打开终端（或cmd）,安装依赖：
``pip install requests``
在脚本的同级目录下新建student.txt
格式如下：
学号 [省 市 区]
可填多行，省市区不填默认福建省福州市鼓楼区

例子：
![image](https://user-images.githubusercontent.com/91642542/149620748-351ed950-3ce6-41d1-99b8-f1417b5e237d.png)

## 自动使用
注册github,点会项目主页面，fork到自己的仓库
![image](https://user-images.githubusercontent.com/91642542/149620802-efee27ea-21a9-42f3-8255-4f6f328fba71.png)
点击action,下面会提示你是否启用workflow,enable即可
![image](https://user-images.githubusercontent.com/91642542/149620830-0e8136bc-7940-41c5-9b2b-bd998ee13371.png)
点击setting，secrets，新建名为students的secret
![image](https://user-images.githubusercontent.com/91642542/149620848-236c4198-f653-46c9-8ba8-53869f48ae2c.png)
![image](https://user-images.githubusercontent.com/91642542/149620878-f4f3db82-a3da-4884-a76d-3d3c5192f212.png)
格式参考本地/服务器使用。
输入后可以自己在action里面运行一次看看是不是成功。
每天2点 4点 7点自动打卡三次。防止gg（其实我也不是很清楚啥时候打卡）
