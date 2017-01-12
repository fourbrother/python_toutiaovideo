# python_toutiaovideo
##python脚本爬取今日头条视频数据
<br><br>

##1、配置好python命令环境变量<br>
##2、直接运行run.bat即可<br>
##3、如果想修改爬取视频页面链接，可以在website.py中getHtml函数处修改即可<br>

<br><br>
#今日头条视频链接构造流程
##1、将/video/urls/v/1/toutiao/mp4/{videoid}?r={Math.random()}，进行crc32加密。
##2、将上面得到的加密值拼接到上面的链接中即可，最终的链接形式是：http://i.snssdk.com/video/urls/v/1/toutiao/mp4/{videoid}?r={Math.random()}&s={crc32值}
##3、访问这个链接得到一个json数据，需要解析video_list数组中的main_url值，然后用base64解码得到最终的原始视频链接。

# Android版本视频下载器
#toutiaovideo.apk文件安装即可使用！



