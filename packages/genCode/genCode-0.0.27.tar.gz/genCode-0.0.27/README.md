# gencode

**[gencode](https://github.com/liuzhuogood/GenCode)** 
代码生成工具，可以连接MySQL\Oracle\postgresql\sqlite根据jinjan2模板生成出自已想要的代码

### 安装
``` shell
pip install gencode
```

### 使用方式
在模板文件所在的目录里执行 
``` sh
gendcode -c config.yml
```    
### 配置文件
##### config.yml
``` YAML
# 模板文件地址
#templatePath: '/data'
dbConf:
  # MySQL / Oracle / Sqlite / postgresql
  db_type: MySQL
  db_name: admin
  user: admin
  pwd: Vile123adMin_#
  host: 127.0.0.1
  # 多表使用;分割
  table_name: sys_operator

# Java
dataTypeMapping:
  varchar|text: String
  decimal(10,2): int

# Python
#dataTypeMapping:
#   default:
#  varchar(*)|text: str

myself:
  author: liuzhuo
  mail: liuzhuogood@foxmail.com
  sign: 我的签名

jinja2:
  variable_start_string: '{{'
  variable_end_string: '}}'


```

### 模板变量

| 变量           | 示例              | 说明 |
| ---------------- | ----------------- | ---- |
| XX_TABLE_NAME | SYS_BULLETIN_FILE |  表名变形  |
| xx_table_name | sys_bulletin_file | 表名变形 |
| XxTableName | SysBulletinFile | 表名变形 |
| xxTableName | sysBulletinFile | 表名变形 |
| TableName | BulletinFile | 表名变形 |
| tableName | bulletinFile | 表名变形 |
| table_name | bulletin_file | 表名变形 |
| xx | sys | 表名变形 |
| XX | SYS | 表名变形 |
| date | 2021-10-11 | 当前日期 |
| datetime | 2021-10-11 10:10:10 | 当前时间 |
| author | liuzhuo | 名称 |
| mail | liuzhuogood@foxmail | 邮箱 |
| sign | 自动生成代码 | 签名 |
| comment | 文件表 | 表备注 |
| columns | <参考columns集合> | 列集合 |



##### columns集合
| 关键字            | 说明                          |
| ----------------- | ----------------------------- |
| column_name    | 列名变形                      |
| COLUMN_NAME   | 列名变形                      |
| ColumnName     | 列名变形                      |
| ColumnName     | 列名变形                      |
| columnname     | 列名变形                      |
| COLUMNAME     | 列名变形                      |
| comment       | 列名备注                      |
| dataType       | 列名 的类型,可以通过配置映射 |
| is_pk       | 1：是主键 0：不是主键 |


##### 方法
* ljust(str,[width],[fill_char]) : 左补全字符
* rjust(str,[width],[fill_char]) : 右补全字符

### 模板
模板可以是文件目录，也可是文件，如果是文件为了区分必须以`.gcode`后缀命名，比如：
##### {{XxTableName}}Po.java.gcode
```
package {{xx}}

/**
 {{comment}} 实体类
 author: {{author}}
 mail: {{mail}}
*/
public class {{TableName}}{
    {% for c in columns %}
        private {{c.dataType}} {{c.columnName}};  //{{c.comment}}

        /**{{c.comment}}*/
        public {{c.dataType}} get{{c.ColumnName}}(){return {{c.columnName}};};

        /**{{c.comment}}*/
        public void set{{c.ColumnName}}({{c.dataType}} {{c.columnName}}){this.{{c.columnName}}={{c.columnName}};};
    {% endfor %}

}

```

