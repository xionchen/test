#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys

if __name__ == '__main__':
    ele_sum = float(sys.argv[1])
    dianfei_file = sys.argv[2]
    print '这月总电费%s' % ele_sum

    with open(dianfei_file, 'r') as f:
        data = f.readlines()
    last_month_ele = [float(ele) for ele in data[0].split(' ')]
    print '上月电量%s\t' % last_month_ele
    this_month_ele = [float(ele) for ele in data[1].split(' ')]
    print '该电量%s\t' % this_month_ele

    ele_usages = []
    for i in xrange(len(last_month_ele)):
        ele_usages.append(this_month_ele[i] - last_month_ele[i])

    print '这月用电量 %s\t' % ele_usages
    ele_sum_usage = sum(ele_usages)

    ele_money = [ele_usage / ele_sum_usage * ele_sum for ele_usage in ele_usages]

    for i in xrange(len(ele_money)):
        print '%s号电表的电费： %s ' % (i+1, ele_money[i])

