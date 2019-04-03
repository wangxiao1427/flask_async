# flask_async

## 使用gunicorn+gevent+flask实现异步非阻塞io框架
* 项目主要代码:
  ```
    @app.route('/cast/<n>')
    def cast(n):
        '''用于ab压力测试
        '''
        time.sleep(int(n))
        print('cast', time.ctime())
        return 'ok'

    @app.route('/other_cast/<n>')
    def other_cast(n):
        '''用于测试不同接口之间的异步
        '''
        time.sleep(int(n))
        print('cast', time.ctime())
        return 'other_ok'
  ```  

* Dockerfile中启动方式为:  
  `gunicorn -w 9 -b 0.0.0.0:5001 -k gevent run:app`  
  
  常用参数:   
  ```
    -w workers工作进程数量，推荐为当前CPU个数*2 + 1
    -b bind绑定套接字，可以多个  
  ```

## 测试

* 先检查项目运行环境CPU个数  
  ```
    λ docker exec -it de970220650c /bin/sh
    /app # python
    Python 3.7.1 (default, Oct 24 2018, 22:42:07)
    [GCC 6.4.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import multiprocessing
    >>> multiprocessing.cpu_count()
    4
  ```
* ab压力测试  
  官方文档[http://httpd.apache.org/docs/current/programs/ab.html]  

  使用
  ```
    λ ab -n 1000 -c 100 "http://127.0.0.1:5001/cast/10"                   
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/   
    Licensed to The Apache Software Foundation, http://www.apache.org/         
                                                                              
    Benchmarking 127.0.0.1 (be patient)                                        
    Completed 100 requests                                                     
    Completed 200 requests                                                     
    Completed 300 requests                                                     
    Completed 400 requests                                                     
    Completed 500 requests                                                     
    Completed 600 requests                                                     
    Completed 700 requests                                                     
    Completed 800 requests                                                     
    Completed 900 requests                                                     
    Completed 1000 requests                                                    
    Finished 1000 requests                                                     
                                                                              
    Server Software:        gunicorn/19.9.0                                    
    Server Hostname:        127.0.0.1                                          
    Server Port:            5001                                               
                                                                              
    Document Path:          /cast/10                                           
    Document Length:        2 bytes                                            
                                                                              
    Concurrency Level:      100                                                
    Time taken for tests:   111.167 seconds                                    
    Complete requests:      1000                                               
    Failed requests:        0                                                  
    Total transferred:      161000 bytes                                       
    HTML transferred:       2000 bytes                                         
    Requests per second:    9.00 [#/sec] (mean)                                
    Time per request:       11116.725 [ms] (mean)                              
    Time per request:       111.167 [ms] (mean, across all concurrent requests)
    Transfer rate:          1.41 [Kbytes/sec] received                         
                                                                              
    Connection Times (ms)                                                      
                  min  mean[+/-sd] median   max                                
    Connect:        0    0   0.5      0       1                                
    Processing: 10003 10074  52.5  10090   10170                               
    Waiting:    10003 10073  52.3  10090   10169                               
    Total:      10003 10074  52.5  10090   10170                               
                                                                              
    Percentage of the requests served within a certain time (ms)               
      50%  10090                                                               
      66%  10109                                                               
      75%  10118                                                               
      80%  10122                                                               
      90%  10136                                                               
      95%  10142                                                               
      98%  10158                                                               
      99%  10163                                                               
    100%  10170 (longest request)                                             
  ```

  常用参数:   
  ```
    -n 为基准测试会话执行的请求个数  
    -c concurrency, 并发数, 同时发起请求的客户端数量   
  ```

  结果分析:  
    ```
    Concurrency Level:      100                                                # 100个客户端
    Time taken for tests:   111.167 seconds                                    # 总耗时
    Complete requests:      1000                                               # 完成请求数
    Failed requests:        0                                                  # 失败请求数
    Requests per second:    9.00 [#/sec] (mean)                                # 每秒请求数
    Time per request:       11116.725 [ms] (mean)                              # 每个请求耗时(平均)
    Time per request:       111.167 [ms] (mean, across all concurrent requests)
    ```