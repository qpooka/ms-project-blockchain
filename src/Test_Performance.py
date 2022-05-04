#!/usr/bin/env python

'''
========================
Perform measurement module
========================
Created on September.19, 2018
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide performance measure utilities.
'''
import sys
import logging
import argparse

from scipy.stats import binom
import matplotlib
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import math

'''
Data preparation class, such as merge data, calculate execute time
'''
class ExecTime(object):
    '''
    read execution time from log file
    '''
    @staticmethod
    def read_exec_time(client_log, skip_section):
        #------------ read data from log file -------------
        f_client = open(client_log, 'r')
        ls_client=f_client.readlines()
        #close file
        f_client.close()

        line_len=len(ls_client)

        exec_time_data=[]

        for i in range(line_len):
            if( ((i+1) % skip_section) !=0):
                continue
            ls_client[i]=ls_client[i].replace('\n','')
            tmp_list=ls_client[i].split()
            exec_time_data.append(tmp_list)

        return exec_time_data

    '''
    calculate execution time by using average
    '''
    @staticmethod
    def calc_exec_time_ave(ls_exec_time):  
        ave_exec_time = []
        for i in range(len(ls_exec_time[0])):  
            ave_exec_time.append(0.0)
        
        for exec_time in ls_exec_time:
            for i in range(len(exec_time)):
                ave_exec_time[i]+=float(exec_time[i])
        
        for i in range(len(ls_exec_time[0])):
            ave_exec_time[i]=format(ave_exec_time[i]/len(ls_exec_time), '.3f')
        
        #print(ave_exec_time)
        return ave_exec_time

'''
Data visualization class to display data as bar or lines
''' 
class VisualizeData(object):
    '''
    plot group bars given ls_dataset
    '''
    @staticmethod
    def plotGroup_Bar(title_name, legend_label, ax_label, xtick_label, ls_dataset):

        N = len(xtick_label)

        # the x locations for the groups
        ind = np.arange(N) 

        width = 0.29           # the width of the bars
        op_color = ['darkorange', 'seagreen', 'blue']

        ## generate bar axis object
        fig, ax = plt.subplots()

        np_dataset=np.array(ls_dataset)/1024

        group_bars = []
        i = 0
        for dataset in np_dataset.transpose():
            # print(dataset)
            rects_bar = ax.bar(ind + width*i, dataset, width, color=op_color[i], label=legend_label[i])
            group_bars.append(rects_bar)
            i+=1

        ## add some text for labels, title and axes ticks
        ax.set_xlabel(ax_label[0], fontsize=24)
        ax.set_ylabel(ax_label[1], fontsize=24)
        # #ax.set_title('Execution time by group', fontsize=18)
        ax.set_xticks(ind + width)
        ax.set_xticklabels(xtick_label, fontsize=20)
        ax.tick_params(axis='y', labelsize=20)

        leg = ax.legend(loc='upper left', fontsize=20)

        for rect_bar in group_bars:
            VisualizeData.autolabel(rect_bar, ax)

        plt.show()

    '''
    plot groupbar chart given ls_data
    '''
    @staticmethod
    def plot_groupbars_block(xtick_label, y_label, legend_label, ls_data):
        Y_RATIO = 1000
        N = len(xtick_label)

        ind = np.arange(N)  # the x locations for the groups
        width = 0.25           # the width of the bars

        #generate bar axis object
        fig, ax = plt.subplots()

        exec_time_tx = []
        for i in range(len(ls_data)):
            exec_time_tx.append(float(ls_data[i][0])/Y_RATIO)

        rects_tx = ax.bar(ind, exec_time_tx, width, color='b')

        exec_time_block = []
        for i in range(len(ls_data)):
            exec_time_block.append(float(ls_data[i][1])/Y_RATIO)
   
        rects_block = ax.bar(ind + width, exec_time_block, width, color='orange')

        exec_time_vote = []
        for i in range(len(ls_data)):
            exec_time_vote.append(float(ls_data[i][3])/Y_RATIO)
   
        rects_vote = ax.bar(ind + 2*width, exec_time_vote, width, color='g')


        # add some text for labels, title and axes ticks
        ax.set_ylabel(y_label, fontsize=18)
        #ax.set_title('Execution time by group', fontsize=18)
        ax.set_xticks(ind + width)
        ax.set_xticklabels(xtick_label, fontsize=18)
        plt.ylim(0, 5.2)

        ax.legend((rects_tx[0], rects_block[0], rects_vote[0]), legend_label, loc='upper left', fontsize=20)

        VisualizeData.autolabel(rects_tx, ax)
        VisualizeData.autolabel(rects_block, ax)
        VisualizeData.autolabel(rects_vote, ax)
        plt.show()
        pass   

    @staticmethod
    def plot_groupbars_cost(xtick_label, y_label, legend_label, ls_data):
        Y_RATIO = 1
        N = len(xtick_label)

        ind = np.arange(N)  # the x locations for the groups
        width = 0.21           # the width of the bars

        #generate bar axis object
        fig, ax = plt.subplots()

        exec_time_tx = []
        for i in range(len(ls_data)):
            exec_time_tx.append(float(ls_data[i][0])/Y_RATIO)

        rects_tx = ax.bar(ind, exec_time_tx, width, color='b')

        exec_time_mine = []
        for i in range(len(ls_data)):
            exec_time_mine.append(float(ls_data[i][1])/Y_RATIO)
   
        rects_mine = ax.bar(ind + width, exec_time_mine, width, color='r')

        exec_time_block = []
        for i in range(len(ls_data)):
            exec_time_block.append(float(ls_data[i][2])/Y_RATIO)
   
        rects_block = ax.bar(ind + 2*width, exec_time_block, width, color='orange')

        exec_time_vote = []
        for i in range(len(ls_data)):
            exec_time_vote.append(float(ls_data[i][3])/Y_RATIO)
   
        rects_vote = ax.bar(ind + 3*width, exec_time_vote, width, color='g')


        # add some text for labels, title and axes ticks
        ax.set_ylabel(y_label, fontsize=16)
        #ax.set_title('Execution time by group', fontsize=18)
        ax.set_xticks(ind + 3*width/2)
        ax.set_xticklabels(xtick_label, fontsize=16)
        #plt.ylim(0, 22)

        #ax.legend((rects_tx[0], rects_block[0], rects_vote[0]), legend_label, loc='upper left', fontsize=18)
        ax.legend((rects_tx[0], rects_mine[0], rects_block[0], rects_vote[0]), legend_label, loc='upper left', fontsize=18)

        VisualizeData.autolabel(rects_tx, ax)
        VisualizeData.autolabel(rects_mine, ax)
        VisualizeData.autolabel(rects_block, ax)
        VisualizeData.autolabel(rects_vote, ax)
        plt.show()
        pass  

    @staticmethod
    def plot_groupbars_platform(xtick_label, y_label, legend_label, ls_data):
        Y_RATIO = 1
        N = len(xtick_label)

        ind = np.arange(N)  # the x locations for the groups
        width = 0.3           # the width of the bars

        #generate bar axis object
        fig, ax = plt.subplots()

        exec_time_fog = []
        for j in range(len(ls_data[0])):
            exec_time_fog.append(float(ls_data[0][j])/Y_RATIO)

        rects_fog = ax.bar(ind, exec_time_fog, width, color='b')

        exec_time_edge = []
        for j in range(len(ls_data[0])):
            exec_time_edge.append(float(ls_data[1][j])/Y_RATIO)
   
        rects_edge = ax.bar(ind + width, exec_time_edge, width, color='g')

        # add some text for labels, title and axes ticks
        ax.set_ylabel(y_label, fontsize=16)
        #ax.set_title('Execution time by group', fontsize=18)
        ax.set_xticks(ind + width/2)
        ax.set_xticklabels(xtick_label, fontsize=16)
        #plt.ylim(0, 22)

        #ax.legend((rects_tx[0], rects_block[0], rects_vote[0]), legend_label, loc='upper left', fontsize=18)
        ax.legend((rects_fog[0], rects_edge[0]), legend_label, loc='upper left', fontsize=18)

        VisualizeData.autolabel(rects_fog, ax)
        VisualizeData.autolabel(rects_edge, ax)
        plt.show()
        pass 

    @staticmethod
    def autolabel(rects, ax):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, (height+0.1),
                    '%.1f' % height,
                    ha='center', va='bottom', fontsize=20)
            

    '''
    plot multiple lines in single chart given ls_data
    '''
    @staticmethod
    def plot_MultiLines(title_name, legend_label, x_ticks, ax_label, ls_data, isLog=0):
        Y_RATIO = 1000
        x=[]
        commit_tx=[]  
        block_proposal=[]   
        chain_finality=[]    
        sum_latency = []    
        
        # Start from 4 nodes    
        # i=4
        # step=4
        for record in ls_data:
            # x.append(i)
            if(isLog==10):
                commit_tx.append(math.log10(float(record[0])))
                block_proposal.append(math.log10( float(record[1])))
                chain_finality.append(math.log10(float(record[3])))
                sum_latency.append( math.log10( float(record[0])+float(record[1])+float(record[3]) ) )
            else:
                commit_tx.append(float(record[0])/Y_RATIO)
                block_proposal.append(float(record[1])/Y_RATIO)
                chain_finality.append(float(record[3])/Y_RATIO) 
                sum_latency.append(  (float(record[0])+float(record[1])+float(record[3]))/Y_RATIO )     
            # i+=step

        line_list=[]
        line_list.append(plt.plot(x_ticks, commit_tx, lw=1.0, marker='*', color='b'))
        line_list.append(plt.plot(x_ticks, block_proposal, lw=1.0, marker='s', color='orange'))
        line_list.append(plt.plot(x_ticks, chain_finality, lw=1.0, marker='o', color='g'))
        line_list.append(plt.plot(x_ticks, sum_latency, lw=1.0, marker='^', color='gray'))

        for x, a in zip(x_ticks, sum_latency): 
            # plt.plot(x, y, "b^")
            # if(x=='100'):
            # str_a='('+ str(x)+', '+format(a, '.3f') + ')'
            str_a = format(a, '.1f')
            plt.text(int(x), a-0.06, str_a, fontsize=14)

        plt.xlabel(ax_label[0], fontsize=18)
        plt.ylabel(ax_label[1], fontsize=18)
        plt.title(title_name)
        #plt.ylim(0, 34)
        plt.legend(legend_label, loc='upper left', fontsize=20)

        #show plot
        plt.show()

    '''
    plot single line in single chart given ls_data
    '''
    @staticmethod
    def plot_throughputLine(title_name, x_label, y_label, ls_data, isLog=0):
        Y_RATIO = 1000
        N = len(x_label)
        x = np.arange(1,N+1)  # the x locations for the groups
        ls_throughput=[]    
        
        for record in ls_data:
            ls_throughput.append(float(record))


        plt.plot(x, ls_throughput, lw=1.0, marker='*', color='b')
        plt.xticks(x, x_label, fontsize=16)
        plt.xlabel('Block size', fontsize=18)
        plt.ylabel(y_label, fontsize=18)
        plt.title(title_name)
        #plt.ylim(0, 34)

        for x_pos, y in zip(x, ls_throughput): 
            # plt.plot(x, y, "b^")
            str_value=format(y, '.0f')
            plt.text(int(x_pos)-0.13, y+25, str_value, fontsize=14)

        #show plot
        plt.show()

    '''
    plot multiple lines in single chart given ls_data
    '''
    @staticmethod
    def plot_txs_MultiLines(title_name, x_label, y_label, ls_data):
        x=[]
        tx_ethereum=[]  
        tx_tendermint=[]
        tx_microchain=[]        
        
        i=1
        for record in ls_data:
            x.append(i)
            tx_ethereum.append(float(record[0]))
            tx_tendermint.append(float(record[1]))
            tx_microchain.append(float(record[2]))          
            i+=1

        line_list=[]
        line_list.append(plt.plot(x, tx_ethereum, lw=1.0, marker='o', color='darkorange'))
        line_list.append(plt.plot(x, tx_tendermint, lw=1.0, marker='.', color='seagreen'))
        line_list.append(plt.plot(x, tx_microchain, lw=1.0, marker='s', color='r'))

        plt.xlabel('Number of runs', fontsize=16)
        plt.ylabel(y_label, fontsize=16)
        plt.ylim(0, 22)
        plt.title(title_name)
        plt.legend(x_label, loc='upper left', fontsize=18)

        #show plot
        plt.show()

    '''
    plot errror bars shown mdedian and std given ls_dataset[mean, std, median, max, min]
    '''
    @staticmethod
    def plot_errorBar(title_name, legend_label, ax_label, ls_dataset):

        N = len(legend_label)

        # the x locations for the groups
        ind = np.arange(N)

        np_dataset=np.array(ls_dataset, dtype=np.float32)
        trans_np_dataset=np_dataset.transpose()
        ls_mean = trans_np_dataset[0]
        ls_std = trans_np_dataset[1]
        ls_median = trans_np_dataset[2]
        ls_max = trans_np_dataset[3]
        ls_min = trans_np_dataset[4]

        fig, ax = plt.subplots()

        # create stacked errorbars:
        plt.errorbar(ind, ls_mean, ls_std, fmt='or', ecolor='seagreen', lw=30)
        plt.errorbar(ind, ls_median, [ls_mean - ls_min, ls_max - ls_mean], 
                    fmt='*k', ecolor='gray', lw=5)

        ax.set_xticks(ind)
        ax.set_xticklabels(legend_label, fontsize=18)
        ax.set_ylabel(ax_label[1], fontsize=18)
        ax.yaxis.grid(True)
        plt.xlim(-0.5, 2.5)

        plt.show()

def ave_Totaldelay(file_name, skip_section=1):
    exec_time_data=ExecTime.read_exec_time(file_name, skip_section)

    ave_exec_time=ExecTime.calc_exec_time_ave(exec_time_data)

    return ave_exec_time

def cal_throughput(exec_time):
    Y_RATIO = 1000
    ls_throughput=[]
    ls_latency = []
    ls_blocksize = [0.001, 0.5, 1, 2, 4]
    # ls_blocksize = [0.5, 1, 2, 4]
    i = 0
    for ls_time in exec_time:
        #print(ls_time)
        tmp_data = (float(ls_time[0])+float(ls_time[1])+float(ls_time[3]))/Y_RATIO 
        ls_latency.append(tmp_data)
        ls_throughput.append(format(ls_blocksize[i]*3600/tmp_data, '.0f'))
        i+=1
    # print(ls_latency)
    return ls_throughput

def plot_exectime_bar():
    file_list = []
    file_list.append('exec_time_client.log')
    file_list.append('exec_time_server.log')
    file_list.append('exec_time_update_client.log')

    '''merged_data = ExecTime.merge_exec_time('results/exec_time_client_ac.log', 
                                           'results/capac_exec_time_server.log')
    #print(merged_data)
    ave_tmp=[0.0, 0.0, 0.0]
    ave_exec_time=ExecTime.calc_exec_time(merged_data)'''
    exec_time_data = []
    for file_name in file_list:
        exec_time_data.append(float(ave_Totaldelay(file_name)[0]))

    end_to_end = ExecTime.read_exec_time('exec_time_client.log', 1)
    auth = ExecTime.read_exec_time('exec_time_server.log', 1)
    SC_change = ExecTime.read_exec_time('exec_time_update_client.log', 1)

    x_label=['End-to-end query', 'Authorization verification', 'Changing SC token']
    #x_label=['End-to-end query', 'Authorization verification']
    #legend_label=['Commit Transaction', 'Block Proposal', 'Chain Finality']
    
    ind = np.arange(3)
    
    #fig, ax = plt.subplots()
    
    plt.figure(0)
    bars = plt.bar(x_label, exec_time_data, width=0.65)
    
    for i in range(len(ind)):
        plt.text(i,exec_time_data[i],exec_time_data[i], ha='center', fontsize=12)
            
    plt.xticks(rotation=10, fontsize=8)    
    #plt.xlabel('operation', fontsize = 5)
    plt.yscale('log')
    plt.ylabel('Time (ms)', fontsize=8)
    plt.title('Average Execution Time of Operations')
    plt.savefig('exec_time.png')
    plt.show()
    
    plt.figure(1)
    plt_end_to_end = []
    for value in end_to_end:
        plt_end_to_end.append(float(value[0]))
        
    plt.plot(plt_end_to_end, marker='.', color='b')
    plt.title('Execution Time of End-to-End Query')
    plt.xlabel('# of run cycles')
    plt.ylabel('Time (ms)')
    plt.savefig('exec_time_query_line.png')
    plt.show()
    
    pass

def plot_blocksize():
    file_list = []
    file_list.append('block_size/exec_time_1K.log')
    file_list.append('block_size/exec_time_512K.log')
    file_list.append('block_size/exec_time_1M.log')
    file_list.append('block_size/exec_time_2M.log')
    file_list.append('block_size/exec_time_4M.log')

    '''merged_data = ExecTime.merge_exec_time('results/exec_time_client_ac.log', 
                                           'results/capac_exec_time_server.log')
    #print(merged_data)
    ave_tmp=[0.0, 0.0, 0.0]
    ave_exec_time=ExecTime.calc_exec_time(merged_data)'''
    exec_time_data = []
    for file_name in file_list:
        exec_time_data.append(ave_Totaldelay(file_name))

    # x_label=['512 KB', '1 MB', '2 MB', '4 MB']
    x_label=['1 KB', '512 KB', '1 MB', '2 MB', '4 MB']
    legend_label=['Commit Transaction', 'Block Proposal', 'Chain Finality']

    VisualizeData.plot_groupbars_block(x_label, 'Time (s)', legend_label, exec_time_data)

    #calculate throughput
    ls_throughput = cal_throughput(exec_time_data)

    VisualizeData.plot_throughputLine("", x_label, 'MB/h', ls_throughput)
    
   
def plot_network_latency(args):
    if(args.scale_op==0):   
        x_ticks=[4, 8, 12, 16, 20]
        ax_label = ['Number of validators', 'Time (s)']
        file_list = []
        for x in x_ticks:
            # file_list.append('latency_validators_1tx/exec_time_{}.log'.format(x))
            file_list.append('latency_validators_100tx/{}/exec_time.log'.format(x))

        exec_time_data = []
        for file_name in file_list:
            exec_time_data.append(ave_Totaldelay(file_name))

        tps = [25, 13, 9, 7, 5]
        for i in range(len(tps)):
            ## calculate avg for tps.
            exec_time_data[i][0] = format(float(exec_time_data[i][0])/tps[i], '.3f')
        print(exec_time_data)

        leg_label=['Commit Transaction', 'Block Proposal', 'Chain Finality', 'Total']
        VisualizeData.plot_MultiLines("", leg_label, x_ticks, ax_label, exec_time_data)
    else:
        x_ticks=[100, 200, 500, 1000, 2400]
        ax_label = ['Number of transactions', 'Time (s)']
        file_list = []
        for x in x_ticks:
            file_list.append('latency_tps/{}/exec_time.log'.format(x))

        exec_time_data = []
        for file_name in file_list:
            exec_time_data.append(ave_Totaldelay(file_name))

        tps = [5, 10, 25, 50, 120]
        for i in range(len(tps)):
            ## calculate avg for tps.
            exec_time_data[i][0] = format(float(exec_time_data[i][0])/tps[i], '.3f')
        print(exec_time_data)

        leg_label=['Commit Transaction', 'Block Proposal', 'Chain Finality', 'Total']
        VisualizeData.plot_MultiLines("", leg_label, x_ticks, ax_label, exec_time_data)

def plot_cost_exec():
    exec_time_data = []

    test_dir_list = []
    test_dir_list.append('cost_exec_edge/cost_exec_1K')
    test_dir_list.append('cost_exec_edge/cost_exec_512K')
    test_dir_list.append('cost_exec_edge/cost_exec_1M')
    test_dir_list.append('cost_exec_edge/cost_exec_2M')
    test_dir_list.append('cost_exec_edge/cost_exec_4M')

    for test_dir in test_dir_list:
        file_list = []
        file_list.append(test_dir + '/exec_verify_tx.log')
        file_list.append(test_dir + '/exec_mining.log')
        file_list.append(test_dir + '/exec_verify_block.log')
        file_list.append(test_dir + '/exec_verify_vote.log')
        ls_data = []
        for file_name in file_list:
            ls_data.append(ave_Totaldelay(file_name)[0])
        exec_time_data.append(ls_data)
    #print(exec_time_data)

    # x_label=['1 KB', '512 KB', '1 MB']
    x_label=['1 KB', '512 KB', '1 MB', '2 MB', '4 MB']
    legend_label=['Verify Transaction', 'Mining Block', 'Verify Block', 'Verify Vote']

    VisualizeData.plot_groupbars_cost(x_label, 'Time (ms)', legend_label, exec_time_data)

def plot_cost_platform():
    exec_time_data = []

    test_dir_list = []
    test_dir_list.append('cost_exec_fog/cost_exec_1M')
    test_dir_list.append('cost_exec_edge/cost_exec_1M')

    for test_dir in test_dir_list:
        file_list = []
        file_list.append(test_dir + '/exec_verify_tx.log')
        file_list.append(test_dir + '/exec_mining.log')
        file_list.append(test_dir + '/exec_verify_block.log')
        file_list.append(test_dir + '/exec_verify_vote.log')
        ls_data = []
        for file_name in file_list:
            ls_data.append(ave_Totaldelay(file_name)[0])
        exec_time_data.append(ls_data)
    #print(exec_time_data)

    x_label=['Verify Transaction', 'Mining Block', 'Verify Block', 'Verify Vote']
    legend_label=['Desktop', 'Raspberry Pi B+']

    VisualizeData.plot_groupbars_platform(x_label, 'Time (ms)', legend_label, exec_time_data)

def plot_tx_commit_lines():
    exec_time_eth=ExecTime.read_exec_time("fog_tx_commit/exec_tx_commit_ethereum.log", 1)
    exec_time_ten=ExecTime.read_exec_time("fog_tx_commit/exec_tx_commit_tendermint.log", 1)
    exec_time_mic=ExecTime.read_exec_time("fog_tx_commit/exec_tx_commit_microchain.log", 1)

    exec_time_data = []
    for i in range(0, len(exec_time_mic)):
        exec_time_data.append([ exec_time_eth[i][0], exec_time_ten[i][0], exec_time_mic[i][0] ])

    obj_label=['Ethereum', 'Tendermint', 'Microchain']
    VisualizeData.plot_txs_MultiLines("", obj_label, 'Tx commit time (sec)', exec_time_data)

def exec_commit_tx(file_name):
    exec_time_data=ExecTime.read_exec_time(file_name, 1)
    ls_data = []
    for time_data in exec_time_data:
        ls_data.append(time_data[0])

    np_data=np.array(ls_data, dtype=np.float32)

    ave_exec_time=format(np.average(np_data), '.3f' )
    median_exec_time=format(np.median(np_data), '.3f' )
    std_exec_time=format(np.std(np_data), '.3f' )
    max_exec_time=format(np.max(np_data), '.3f' )
    min_exec_time=format(np.min(np_data), '.3f' )

    return [ave_exec_time, std_exec_time, median_exec_time, max_exec_time, min_exec_time]

def plot_commit_tx():
    data_files = ["exec_tx_commit_ethereum.log", "exec_tx_commit_tendermint.log", "exec_tx_commit_microchain.log"]

    exec_time_network = []
    for data_file in data_files:
        ## for each files to build ls_data
        file_name = "fog_tx_commit/"+data_file
        tx_time = exec_commit_tx(file_name)
        exec_time_network.append(tx_time)
        print( "{}:\t average-{}\t std-{}\t median-{}\t max-{}\t min-{}".format( 
            data_file, tx_time[0], tx_time[1], tx_time[2], tx_time[3], tx_time[4]) )

    # print(exec_time_network)

    ax_label = ['', 'Time (s)']
    legend_label=['Ethereum', 'Tendermint', 'Microchain']

    # VisualizeData.plot_Bar_mean_std('', legend_label, ax_label, exec_time_network)
    VisualizeData.plot_errorBar('', legend_label, ax_label, exec_time_network)

def plot_swarm():
    ave_exec_time=ave_Totaldelay("Swarm/test_swarm.log")

    print("Swarm latency, Upload: {}    Download: {}".format(ave_exec_time[0], ave_exec_time[1]))

def plot_Msg_Throughput(args):
    msg_size = {}
    msg_size['block_head'] = 613
    msg_size['tx'] = 430
    msg_size['vote'] = 589
    # print(msg_size)

    ls_nodes = [4, 8, 12, 16, 20]
    ls_txs = [100, 200, 500, 1000, 2400]

    deliver_data = []
    block_size = []

    if(args.scale_op==0):
        txs = ls_txs[0]
        for nodes in ls_nodes:
            txs_data = msg_size['tx']*txs*nodes

            blks_data = ( msg_size['block_head'] + msg_size['tx']*txs )*nodes

            votes_data = msg_size['vote']*nodes*nodes

            deliver_data.append( [txs_data, blks_data, votes_data ] )
            block_size.append( format( (msg_size['block_head'] + msg_size['tx']*nodes)/1024, '.3f') )

        print("Block size: {}".format(block_size))

        ax_label = ['Number of validators', 'Network Usage (KB)']
        legend_label=['Commit Transaction', 'Block Proposal', 'Chain Finality']
        VisualizeData.plotGroup_Bar('', legend_label, ax_label, ls_nodes, deliver_data)
    else:
        nodes = ls_nodes[-1]
        for txs in ls_txs:
            txs_data = msg_size['tx']*txs*nodes/1024

            blks_data = ( msg_size['block_head'] + msg_size['tx']*txs )*nodes/1024

            votes_data = msg_size['vote']*nodes*nodes/1024

            deliver_data.append( [txs_data, blks_data, votes_data ] )
            block_size.append( format( (msg_size['block_head'] + msg_size['tx']*txs)/1024, '.3f') )
        print("Block size: {}".format(block_size))

        ax_label = ['Number of transactions', 'Network Usage (MB)']
        legend_label=['Commit Transaction', 'Block Proposal', 'Chain Finality']
        VisualizeData.plotGroup_Bar('', legend_label, ax_label, ls_txs, deliver_data)


    ## calculate throughput
    if(args.scale_op==0):
        ls_latency = [0.2, 0.4, 0.9, 1.2, 1.6]
    else:
        ls_latency = [1.6, 1.8, 2.5, 4.9, 14.7]

    np_dataset=np.array(deliver_data)
    i=0
    ls_sum=[]
    for dataset in np_dataset:
        sum_data = np.sum(dataset)/1024
        throughput = sum_data/ls_latency[i]
        ls_sum.append([format(sum_data, '.3f'), format(throughput, '.3f')])
        i+=1
    print("Total size: {}".format(ls_sum))

def plot_committee_security(args):
    adversary_stake = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    committee_size = [4, 8, 12, 16, 20]

    if(args.committee_op==1):
        for i in range(len(adversary_stake)):
            n, p = committee_size[-1], adversary_stake[i]
            k_values = list(range(n + 1))

            print("n: {}\tp: {}".format(n, p))

            ## obtaining the mean and variance
            mean, var = binom.stats(n, p)

            ## printing mean and variance
            print("mean: {}\tvar: {}".format(mean, var))

            ## list of pmf values
            dist = [binom.pmf(k, n, p) for k in k_values ]

            k_min = math.floor(len(dist)/2)

            print("Sum k>={}\tP={}".format(k_min, np.sum(dist[k_min:])))
    else:
        for i in range(len(committee_size)):
            n, p = committee_size[i], adversary_stake[4]
            k_values = list(range(n + 1))

            print("n: {}\tp: {}".format(n, p))

            ## obtaining the mean and variance
            mean, var = binom.stats(n, p)

            ## printing mean and variance
            print("mean: {}\tvar: {}".format(mean, var))

            ## list of pmf values
            dist = [binom.pmf(k, n, p) for k in k_values ]

            k_min = math.floor(len(dist)/2)

            print("Sum k>={}\tP={}".format(k_min, np.sum(dist[k_min:])))

    m=0
    P=1.0
    while(P>0.000001):
        P=(0.014)**m
        m+=1
    print(m)        

def plot_encrypt_model():
    ave_delay_fog=ave_Totaldelay("encrypt_model/test_sym_fog.log")
    ave_delay_edge=ave_Totaldelay("encrypt_model/test_sym_edge.log")

    print("Encrypt model latency, Fog: {}    Edge: {}".format(ave_delay_fog[0], ave_delay_edge[0]))
    print("Decrypt model latency, Fog: {}    Edge: {}".format(ave_delay_fog[1], ave_delay_edge[1]))

def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run test evaulation app."
    )
    parser.add_argument("--test_op", type=int, default=0, 
                        help="Execute test operation: \
                        0-function test, \
                        1-plot_network_latency, \
                        2-plot_blocksize, \
                        3-plot_cost_exec, \
                        4-plot_cost_platform, \
                        5-plot_tx_commit, \
                        6-plot_swarm, \
                        7-plot_Msg_Throughput, \
                        10-plot_exectime_bar")
    parser.add_argument("--scale_op", type=int, default=0, 
                        help="Execute scalablity test: \
                        0-scale up nodes, \
                        1-scale up txs")

    parser.add_argument("--tx_op", type=int, default=0, 
                        help="Plot commit tx: \
                        0-show distribution, \
                        1-show lines")

    parser.add_argument("--committee_op", type=int, default=0, 
                        help="Plot committee security: \
                        0- change committee size, \
                        1- change adversary stake")

    args = parser.parse_args(args=args)
    return args

if __name__ == "__main__":
    args = define_and_get_arguments()
    matplotlib.rcParams.update({'font.size': 14})

    if(args.test_op==1):
        #--------------- show nodes latency curves--------------------
        plot_network_latency(args)
    elif(args.test_op==2):
        #--------------- show block size latency curves--------------------
        plot_blocksize()
    elif(args.test_op==3):
        #--------------- show performance cost on edge--------------------
        plot_cost_exec()
    elif(args.test_op==4):
        #--------------- show performance cost on different platform--------------------
        plot_cost_platform()
    elif(args.test_op==5):
        if(args.tx_op==1):
            plot_tx_commit_lines()
        else:
            plot_commit_tx()
    elif(args.test_op==6):
        plot_swarm()
    elif(args.test_op==7):
        plot_Msg_Throughput(args)
    elif(args.test_op==8):
        plot_committee_security(args)
    elif(args.test_op==9):
        plot_encrypt_model()
    elif(args.test_op==10):
        plot_exectime_bar()
    else:
        pass