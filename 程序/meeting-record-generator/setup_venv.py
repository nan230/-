#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anaconda环境配置脚本
用于自动化创建和管理项目虚拟环境
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# 项目配置
PROJECT_ROOT = Path(__file__).parent
ENV_NAME = "meeting-generator"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
ENVIRONMENT_FILE = PROJECT_ROOT / "environment.yml"

def run_command(cmd, check=True):
    """执行命令并返回结果"""
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"错误: {result.stderr}")
            sys.exit(1)
        return result
    except Exception as e:
        print(f"执行失败: {e}")
        sys.exit(1)

def check_conda():
    """检查是否安装Anaconda"""
    try:
        result = run_command("conda --version", check=False)
        if result.returncode == 0:
            print(f"✅ Anaconda已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ 未检测到Anaconda，请先安装")
            return False
    except:
        print("❌ 未检测到Anaconda，请先安装")
        return False

def create_environment():
    """创建虚拟环境"""
    print(f"🔄 创建环境: {ENV_NAME}")
    
    # 检查环境是否已存在
    result = run_command(f"conda env list | findstr {ENV_NAME}", check=False)
    if result.returncode == 0:
        print(f"⚠️ 环境 {ENV_NAME} 已存在，是否重新创建？")
        response = input("输入 'y' 重新创建，其他键跳过: ")
        if response.lower() == 'y':
            run_command(f"conda env remove -n {ENV_NAME}")
        else:
            print("跳过创建步骤")
            return
    
    # 创建新环境
    if ENVIRONMENT_FILE.exists():
        print("使用environment.yml创建环境...")
        run_command(f"conda env create -f {ENVIRONMENT_FILE}")
    else:
        print("使用基础配置创建环境...")
        run_command(f"conda create -n {ENV_NAME} python=3.9 -y")

def install_dependencies():
    """安装项目依赖"""
    print("📦 安装项目依赖...")
    
    # 激活环境并安装依赖
    activate_cmd = f"conda activate {ENV_NAME}"
    
    if REQUIREMENTS_FILE.exists():
        print("从requirements.txt安装...")
        full_cmd = f"{activate_cmd} && pip install -r {REQUIREMENTS_FILE}"
        run_command(full_cmd)
    
    # 安装额外的开发工具
    print("安装开发工具...")
    dev_tools = ["jupyter", "pytest", "black", "flake8"]
    for tool in dev_tools:
        run_command(f"{activate_cmd} && conda install {tool} -y -c conda-forge", check=False)

def create_activation_scripts():
    """创建环境激活脚本"""
    print("📝 创建激活脚本...")
    
    # Windows激活脚本
    windows_script = PROJECT_ROOT / "activate_env.bat"
    with open(windows_script, 'w', encoding='utf-8') as f:
        f.write(f"""@echo off
echo 正在激活环境: {ENV_NAME}
call conda activate {ENV_NAME}
echo ✅ 环境已激活，可以开始开发！
echo.
echo 常用命令:
echo   python main.py          - 启动Flask应用
echo   python -m pytest        - 运行测试
echo   jupyter notebook        - 启动Jupyter
echo.
""")
    
    # Unix激活脚本
    unix_script = PROJECT_ROOT / "activate_env.sh"
    with open(unix_script, 'w', encoding='utf-8') as f:
        f.write(f"""#!/bin/bash
echo "正在激活环境: {ENV_NAME}"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate {ENV_NAME}
echo "✅ 环境已激活，可以开始开发！"
echo
echo "常用命令:"
echo "  python main.py          - 启动Flask应用"
echo "  python -m pytest          - 运行测试"
echo "  jupyter notebook          - 启动Jupyter"
echo
""")
    
    # 添加执行权限
    if os.name != 'nt':
        os.chmod(unix_script, 0o755)

def create_project_info():
    """创建项目信息文件"""
    print("📋 创建项目信息...")
    
    project_info = {
        "project_name": "会议记录生成器",
        "environment_name": ENV_NAME,
        "python_version": "3.9",
        "created_date": "2024",
        "dependencies": [
            "Flask==2.3.3",
            "python-docx==0.8.11",
            "Flask-CORS==3.0.10",
            "jieba==0.42.1",
            "requests==2.31.0",
            "numpy==1.24.0"
        ],
        "activation": {
            "windows": "activate_env.bat",
            "unix": "activate_env.sh"
        },
        "usage": {
            "start_app": "python main.py",
            "access_url": "http://127.0.0.1:5000"
        }
    }
    
    with open(PROJECT_ROOT / "project_info.json", 'w', encoding='utf-8') as f:
        json.dump(project_info, f, ensure_ascii=False, indent=2)

def main():
    """主函数"""
    print("🚀 开始配置Anaconda虚拟环境...")
    print("=" * 50)
    
    # 检查Anaconda
    if not check_conda():
        print("请访问 https://www.anaconda.com/download 下载安装Anaconda")
        sys.exit(1)
    
    # 创建环境
    create_environment()
    
    # 安装依赖
    install_dependencies()
    
    # 创建激活脚本
    create_activation_scripts()
    
    # 创建项目信息
    create_project_info()
    
    print("\n" + "=" * 50)
    print("✅ 环境配置完成！")
    print(f"环境名称: {ENV_NAME}")
    print("\n下一步:")
    print("1. 运行 activate_env.bat (Windows) 或 source activate_env.sh (Unix)")
    print("2. 激活环境后运行: python main.py")
    print("3. 访问: http://127.0.0.1:5000")
    print("\n📖 查看 project_info.json 获取更多信息")

if __name__ == "__main__":
    main()