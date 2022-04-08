# [![HaxExtend](https://github.com/mybdye/HaxExtend/actions/workflows/main.yml/badge.svg)](https://github.com/mybdye/HaxExtend/actions/workflows/main.yml)
#### Dev 记录
##### To Do List
- [ ] cloud flare 5s, undetected_chromedriver 难搞哦
- [x] login, 异常跳转,audio 元素找不到, 元素遮挡问题


#### 状态
- 

#### 项目进度
- 0330 添加了 tg push，`func submit` 也还有些 ~~小~~ 问题
- 0328 ~~能跑~~ 本地能跑，workflow 再研究下。
- 0326 新建文件夹

#### 🍳 烹饪方法：1.1 
- Settings > Secrets > Actions 添加以下变量

|YOU SECRET NAME|YOU SECRET VALUE|
|-----|-----|
|`USER_ID`|你的 id|
|`PASS_WD`|你的密码|
|`BARK_KEY`|(可选) https://api.day.app/BARK_KEY/|
|`TG_BOT_TOKEN`|(可选) `xxxxxx:xxxxxxxxxxxxx`|
|`TG_USER_ID`|(可选) 给 bot `@userinfobot` 发送 `/start`|

#### 🍳 烹饪方法：1.2 
- Actions > Workflows [HaxExtend] > Run workflow
<img src=./step.png width=50% />

#### 触发说明：手动 + schedule
```
name: 'HaxExtend'

on:
  #push:
  schedule:
    # run everyday at UTC 04:30 (CN time UTC+8)
     - cron: '30 4 * * *'
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:
```

#### 运行结果
```
*** 💣 Possibly blocked by google! ***
Your computer or network may be sending automated queries. To protect our users, we can't process your request right now. For more details visit our help page.
```
or
```
 🎉 Your VPS has been renewed until April 6, 2022
```
<img src=./result.jpg width=50% />

#### How This Work
- https://github.com/mybdye/HaxExtend/blob/master/howthiswork.md

#### 资料参考
- https://www.python.org/
- https://www.selenium.dev/
- https://www.youtube.com/watch?v=As-_hfZUyIs
- https://github.com/actions/virtual-environments/blob/main/images/macos/macos-12-Readme.md
- https://github.com/mherrmann/selenium-python-helium/blob/master/helium/__init__.py

#### 以上仅供学习 ：）
