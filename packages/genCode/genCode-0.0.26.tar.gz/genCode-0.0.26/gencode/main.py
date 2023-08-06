import os
import shutil
import sys
import time

from jinja2 import Template
from rich.console import Console
from rich.table import Table

from gencode.data import get_data
from gencode.models import Gcode
from gencode.utils import get_path_list
from gencode.version import VER

console = Console()


def render(data, test=True, code_files=[]):
    index = 1
    code_map = {}
    if test:
        console.print("-----------将生成文件：------------", style="bold blue")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("NO.")
        table.add_column("FILE ")
        table.add_row("A", "[red]ALL[/red]")

    from gencode.config import target_encoding, template_path, gen_one_file
    # 路径经过模板
    for gcode in get_path_list(path=template_path, encode=target_encoding):
        if gen_one_file is None or gcode.temp_base_name == gen_one_file:
            g = to_template(gcode, data)
            if g is not None:
                if test:
                    if not g.is_dir:
                        # print(index, "#", g.target_path)
                        table.add_row(str(index), g.target_path)
                        code_map[str(index)] = g.target_path
                        index += 1
                else:
                    gen_result(g, code_files)
    if test:
        console.print(table)
        i = input("请输入要生成的文件（例：1,2,3）：")
        print("")
        if i.lower() == 'a':
            return code_map.values()
        else:
            i = i.replace("，", ",")
            ii = i.split(",")
            aa = []
            for a in ii:
                if a in code_map.keys():
                    aa.append(code_map[a])
            return aa


def to_template(gcode: Gcode, data) -> Gcode:
    from gencode.config import jinja2_config
    try:
        if not gcode.is_dir:
            template = Template(gcode.temp_content, variable_start_string=jinja2_config["variable_start_string"],
                                variable_end_string=jinja2_config["variable_end_string"])
            txt = template.render(data, ljust=str.ljust, rjust=str.rjust)
            gcode.target_content = txt
        template = Template(gcode.target_path, variable_start_string=jinja2_config["variable_start_string"],
                            variable_end_string=jinja2_config["variable_end_string"])
        result = template.render(data, ljust=str.ljust, rjust=str.rjust)
        gcode.target_path = result
        return gcode
    except Exception:
        console.print("============错误==============", style="bold red")
        console.print(f"模板：{gcode.temp_path}", style="bold red")
        console.print_exception(extra_lines=5, show_locals=True)


def gen_result(gcode: Gcode, code_files):
    """生成目录和文件"""
    backups = []
    if gcode.target_path in code_files:
        if gcode.is_dir:
            if not os.path.exists(gcode.target_path):
                os.makedirs(gcode.target_path, exist_ok=True)
                print("创建目录：" + os.path.abspath(gcode.target_path))
        else:

            os.makedirs(os.path.dirname(gcode.target_path), exist_ok=True)
            if os.path.exists(gcode.target_path):
                target_path = gcode.target_path + "_backup_" + str(int(time.time() * 1000))
                shutil.copyfile(gcode.target_path, target_path)
                backups.append(target_path)
            f = open(gcode.target_path, mode="wb+")
            f.write(gcode.target_content.encode(encoding=gcode.encode))
            f.flush()
            f.close()
            print("生成代码：" + os.path.abspath(gcode.target_path))

    if len(backups) > 0:
        for b in backups:
            print("备份", b)
        i = input("是否删除本次备份文件（Y/N）")
        if i.upper() == "Y":
            for b in backups:
                os.remove(b)


def run():
    console.print(f"""
     
 ██████  ███████ ███    ██      ██████  ██████  ██████  ███████ 
██       ██      ████   ██     ██      ██    ██ ██   ██ ██      
██   ███ █████   ██ ██  ██     ██      ██    ██ ██   ██ █████   
██    ██ ██      ██  ██ ██     ██      ██    ██ ██   ██ ██      
 ██████  ███████ ██   ████      ██████  ██████  ██████  ███████ 
                                                             
                        liuzhuogood@foxmail.com
                        version:{VER}  
                        doc: https://github.com/liuzhuogood/GenCode
                        
                                    """, style="bold blue")
    inputs = sys.argv
    if len(inputs) < 2:
        print("请使用带上yml配置文件，比如 gencode config.yml")
    has_yml = False
    c = ""
    for ins in inputs:
        if ins.endswith(".yml"):
            has_yml = True
            c = ins
            break
        if ins == "--debug":
            IS_DEBUG = 1

    if not has_yml:
        print("请使用带上yml配置文件，比如 gencode config.yml")

    try:
        from gencode.config import load_conf
        if load_conf(c):
            from gencode.config import DB_CONF
            table_names = str(DB_CONF["table_name"]).split(";")
            for table in table_names:
                if table == "":
                    continue
                d = get_data(table_name=table)
                code_files = render(data=d)
                render(data=d, test=False, code_files=code_files)
    except KeyboardInterrupt:
        console.print(f"""\nBye ~""", style="bold dim")


if __name__ == '__main__':
    run()
