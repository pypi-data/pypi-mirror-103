import os

import yaml

DB_CONF = {
    "db_type": "MySQL",
    "db_name": "mysql",
    "user": "root",
    "pwd": "123456",
    "host": "127.0.0.1",
    "table_name": ["sys_menu_router"]
}

data_type_mapping = {
    "varchar(*)|text": "String"
}

target_encoding = "utf-8"
jinja2_config = {}
template_path = ""
myself = {}
ignores = []

# 只生成某个模板文件
gen_one_file = ""


def load_conf(path):
    if not os.path.isfile(path):
        pwd = os.path.dirname(__file__)
        if os.path.isfile(os.path.join(pwd, path)):
            path = os.path.join(pwd, path)
        else:
            print(f"找不到配置文件：{path}")
            return False

    global DB_CONF, data_type_mapping, target_encoding, template_path, myself, gen_one_file, ignores
    c = yaml.safe_load(str(open(path, mode='rb').read(), encoding='utf-8'))
    template_path = c.get("templatePath", os.path.dirname(path))
    DB_CONF = c.get("dbConf", DB_CONF)
    data_type_mapping = c["dataTypeMapping"]
    data_type_mapping = c["dataTypeMapping"]
    jinja2_config["variable_start_string"] = c.get("variable_start_string", "{{")
    jinja2_config["variable_end_string"] = c.get("variable_end_string", "}}")
    myself = c.get("myself", "{}")
    ignores = c.get("ignore", "").split(";")
    gen_one_file = c.get("gen_one_file", None)

    i = input(f"请输入表名（默认：{DB_CONF.get('table_name', '')}）：")
    print("")
    if i.strip() == '' and DB_CONF.get('table_name', '') == '':
        return load_conf(path)
    else:
        if i.strip() != '':
            DB_CONF['table_name'] = i.strip()
    return True
