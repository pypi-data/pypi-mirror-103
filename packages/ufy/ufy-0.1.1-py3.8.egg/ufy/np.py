# -*- coding: utf-8 -*-
# @Time     : 2021/4/22 19:25
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : np.py
# @info     :
try:
    import cupy as np
    np.cuda.set_allocator(np.cuda.MemoryPool().malloc)

    print('\033[92m' + '-' * 60 + '\033[0m')
    print(' ' * 23 + '\033[92mGPU Mode (cupy)\033[0m')
    print('\033[92m' + '-' * 60 + '\033[0m\n')
except:
    import numpy as np

    print('\033[92m' + '-' * 60 + '\033[0m')
    print(' ' * 23 + '\033[92mCPU Mode (numpy)\033[0m')
    print('\033[92m' + '-' * 60 + '\033[0m\n')