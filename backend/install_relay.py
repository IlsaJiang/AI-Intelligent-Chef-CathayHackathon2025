import sys
import subprocess


def install_dependencies():
    """安装 Django 项目所需的依赖包"""
    dependencies = [
        "django-cors-headers",
        "drf-spectacular",
        "djangorestframework"
    ]

    print("正在安装项目依赖...")
    for package in dependencies:
        try:
            print(f"安装 {package}...")
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                package
            ])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"❌ {package} 安装失败，请手动执行: pip install {package}")

    print("\n安装完成！请重新运行 Django 项目")


if __name__ == "__main__":
    install_dependencies()
