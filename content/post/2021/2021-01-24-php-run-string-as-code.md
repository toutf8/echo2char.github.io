---
title: "PHP 字符串当作代码执行"
date: 2021-01-25T00:08:56+08:00
draft: false
url: "/2021/01/24/php-run-string-as-code/"
categories:
 - 技术文章
---

最近遇到的问题，部分代码是直接写入到 redis 缓存的，这部分代码需要转换成代码执行。
处理的方式有下面三种：
1. 简单的方式 可以通过 php 的 `eval` 函数直接使用
2. 读取内容保存成文件后再执行
3. 复杂的情况，需要通过 流 的方式处理

下面是通过第三种方式实现， 避免了保存文件再清理的麻烦
```php
<?php
/**
 * Theme
 *
 * desc: include theme string as php file
 * by: dbquan
 * data: Tue Apr 10 14:15:42 CST 2018
 *
 */


/** Register theme wrapper */
ThemeStreamWrapper::register();


// ticket:7642
class ThemeStreamWrapper {
    private $string;
    private $position;

    /**
     * Register wrapper
     */
    public static function register() {
        @stream_wrapper_unregister("theme");
        @stream_wrapper_register("theme", __CLASS__);
    }

    /**
     * Open Stream
     */
    public function stream_open($path, $mode, $options, &$opened_path) {
        // Parse URL
        $url = parse_url($path);
        $theme_redis_key = $url["host"];

        //根据redis_key到数据库中取出php字符串代码
        $theme_redis = RedisHelper::getInstance(THEME_REDIS_HOST, THEME_REDIS_DB, THEME_REDIS_PORT, THEME_REDIS_PASSWORD);
        $this->string = $theme_redis->get($theme_redis_key);
        $this->position = 0;
        return true;
    }

    public function stream_read($count) {
        $ret = substr($this->string, $this->position, $count);
        $this->position += strlen($ret);
        return $ret;
    }
    public function stream_eof() {}
    public function stream_stat() {}
    public function url_stat() {}
}

// usage example
// include("theme://0_page_en_v2_00_53_53_53");

```

---------
参考 
* https://www.cnblogs.com/jingjingdidunhe/p/6346884.html
* https://www.cnblogs.com/dormscript/p/6163774.html
