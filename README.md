## 项目介绍
pytest-jenkins是基于pytest封装的一套接口测试框架，可以本地使用也可集成jenkins使用。

## 功能支持
1. 支持数据驱动，维护excel中的用例表格即可增删用例
2. 支持jsonpath和正则取值，在用例中传递
3. 支持url,header,body中的变量参数
4. 支持对响应json中单据字段类型和value的校验
5. 支持整段响应json的差异对比

## 模块介绍
1. base: 将接口的url,header,body,断言等做了拆封，实现模块化的处理
2. log: 运行日志的输出路径
3. properties: 数据库或其他配置文件的存放
4. resources: 测试执行过程中所需的文件，如果上传文件功能的测试
5. test: pytest测试运行的目录
6. testcase: 用例存放目录
7. utils: 工具模块，包含数据库、邮件消息、文件处理等

## 运行命令
使用pytest的命令触发即可
```shell
pytest -m 'prod and outing' test/prod/
```

## Jenkins集成和Allure报告配置
1. Jenkins安装插件`Allure Report`
2. 构建->执行shell
```shell
cd ${WORKSPACE}
pytest -m 'prod and hw' test/prod/ --alluredir=target/allure-results
```
3. 构建后操作->Results
```shell
target/allure-results
```