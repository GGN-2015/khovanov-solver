# 给定一个没有 r1-move 和 nugatory crossing 的扭结
# 利用 javaKh 计算它的 khovanov 同调



import os
import shutil
import tempfile
import subprocess



# 如果 java 已经在环境变量 PATH 路径下，直接填写 "java" 即可
# 否则需要填写 java 所在的路径
JAVA_PATH = "java"



# 用于创建并销毁临时目录
TMP_DIRS = []

def get_temp_dir_prefix(): # 获取进程、时间、相关的文件名前缀
    return "tmp_kho_solver_%07d_" % (os.getpid())

def create_temp_dir(): # 创建临时目录
    temp_dir = tempfile.mkdtemp("", get_temp_dir_prefix())
    TMP_DIRS.append(os.path.abspath(temp_dir))

def remove_temp_dir(): # 清除所有临时目录
    for temp_dir in TMP_DIRS:
        shutil.rmtree(temp_dir)



# 用于定位模板文件夹
SOURCE_DIR   = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(SOURCE_DIR, "javakh_ori_temp")
assert os.path.isdir(TEMPLATE_DIR)

def copy_template_to_temp(): # 将模板文件夹拷贝到临时目录下
    tmp_dir = TMP_DIRS[0]    # 假设系统已经分配了一个临时目录（若未分配，则报错）
    for file in os.listdir(TEMPLATE_DIR):
        filepath_src = os.path.join(TEMPLATE_DIR, file)
        filepath_dst = os.path.join(tmp_dir, file)
        dirfile      = os.path.isdir(filepath_src)
        os.symlink(filepath_src, filepath_dst, dirfile) # 创建软连接
        assert os.path.islink(filepath_dst)

def dump_pd_code_to_temp_file(wrapped_pd_code: str): # 将 pd_code 写入指定文件夹
    tmp_dir      = TMP_DIRS[0]                       # 假设系统已经分配了一个临时目录（若未分配，则报错）
    pd_code_file = os.path.join(tmp_dir, "PD.txt")
    open(pd_code_file, "w").write(wrapped_pd_code)

def run_javakh_with_shell(pd_code: list):         # 在临时文件夹下运行 java_kh
    tmp_dir         = TMP_DIRS[0]                 # 假设系统已经分配了一个临时目录（若未分配，则报错）
    warpped_pd_code = __pd_code_wrapper(pd_code)  # 计算 JavaKh 的输入字符串
    dump_pd_code_to_temp_file(warpped_pd_code)    # 将指定输入字符串存入文件
    sh_code_file = os.path.join(tmp_dir, "go.sh") # 运行启动脚本
    result     = subprocess.run(["bash", sh_code_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_ans = result.stdout.decode("utf-8").rstrip()
    stderr_ans = result.stderr.decode("utf-8").rstrip()
    khovanov_value = [line for line in stdout_ans.split('\"') if len(line.strip()) > 0]
    khovanov_value = khovanov_value[-1]
    if len(khovanov_value) == 0 or khovanov_value[:2] != "q^":
        raise AssertionError("JavaKh: ")
    return khovanov_value.strip()



def __pd_code_wrapper(pd_code: list) -> str: # 获取 JavaKh 输入风格的名字
    xlist = ["X" + str(x) for x in pd_code]  # 交叉点序列
    return "PD[" + (", ".join(xlist)) + "]"



def kho_solver(pd_code: list) -> str: # 计算 Khovaov 同调，不能处理平凡扭结，r1-move, 8字交点
    create_temp_dir()
    copy_template_to_temp()
    kho_value = ""
    try:
        kho_value = run_javakh_with_shell(pd_code)
    finally:
        remove_temp_dir() # 无论是否报错，都要删除临时文件
    return kho_value      # 如果程序出错，将返回空字符串



if __name__ == "__main__": # 测试
    print(kho_solver([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]))