# khovanov-solver
给定 PD_CODE 计算 khovanov 同调的通用程序，本程序旨在尽可能减少计算过程中需要的依赖。



## 前置条件

- `python3`
- `openjdk-11`



## 使用方法

- 运行 `python3 ./src/main.py`
  - 向标准输入流中输入一个 list of list 作为 PD_CODE
  - 程序会将 khovanov 同调输出到标准输出流，运行时遇到的错误输出到标准错误流

