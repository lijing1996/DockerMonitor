# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午5:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import os
import numpy as np
import cv2
import sqlite3
import copy


def fun(nums):
    # down
    in_nums = copy.deepcopy(nums)
    down_change = 0
    for i in range(len(nums)):
        if i > 0 and nums[i] > nums[i - 1]:
            down_change += (nums[i] - nums[i - 1])
            nums[i] = nums[i - 1]

        if i < len(nums) - 1 and nums[i + 1] > nums[i]:
            if i == 0 or nums[i - 1] >= nums[i + 1]:
                down_change += (nums[i + 1] - nums[i])
                nums[i] = nums[i + 1]
            else:
                down_change += (nums[i - 1] - nums[i])
                nums[i] = nums[i - 1]

    # up
    nums = in_nums
    up_change = 0
    for i in range(len(nums)):
        if i > 0 and nums[i] < nums[i - 1]:
            up_change += (nums[i - 1] - nums[i])
            nums[i] = nums[i - 1]

        if i < len(nums) - 1 and nums[i + 1] < nums[i]:
            if i == 0 or nums[i - 1] <= nums[i + 1]:
                up_change += (nums[i] - nums[i + 1])
                nums[i] = nums[i + 1]
            else:
                up_change += (nums[i] - nums[i - 1])
                nums[i] = nums[i - 1]

    return min(down_change, up_change)


if __name__ == '__main__':
    print(fun([1, 2, 3, 3, 4]))
    print(fun([9, 8, 7, 2, 3, 3]))
    print(fun([1, 2, 3, 10, 10, 2]))
    print(fun([9, 8, 7, 2, 10, 10]))
