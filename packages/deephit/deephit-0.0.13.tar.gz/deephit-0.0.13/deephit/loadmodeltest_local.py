
# Adapting from Databricks notebook source
# This is an example of how a draft of LOS model saved in databricks can be downloaded in a different environment
# and loaded to make a predict
# Step 1: download the following files 
#https://adb-7829703706139892.12.azuredatabricks.net/files/Los_v2.data-00000-of-00001?o=7829703706139892
#https://adb-7829703706139892.12.azuredatabricks.net/files/Los_v2.index?o=7829703706139892
#https://adb-7829703706139892.12.azuredatabricks.net/files/Los_v2.meta?o=7829703706139892
#https://adb-7829703706139892.12.azuredatabricks.net/files/Los_v2_par.pkl?o=7829703706139892
#https://adb-7829703706139892.12.azuredatabricks.net/files/pd_test_dumy.csv?o=7829703706139892
# Step 2: save in folder defined in file_path_final
# to-dos:
#   easy: 
    #   redo import function for general data intake
    #   check if masks are necessary for predict
    #   separate data load, model restore and predict in functions. 
    #   create main.
#  not so easy:
    #  save/import list of mean and std for each feature of final dummies for whole data to be used in normalization in import function, do data import function can be called for just one entry


import numpy as np 
import pandas as pd 
import tensorflow as tf 
from tensorflow.contrib.layers import fully_connected as FC_Net 
from sklearn.metrics import brier_score_loss 
from sklearn.model_selection import train_test_split 
import random 
from lifelines import KaplanMeierFitter 


import matplotlib.pyplot as plt 
import math 
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder

import sklearn.metrics as metrics

import datetime
print( datetime.datetime.now() )

from termcolor import colored
import importlib

from scipy import stats
import math



pd_test_dummy=pd.read_csv('pd_test_dumy.csv')


### reorder the columns for easy data load later

not_feat_list=['iculos',
'hosplos',
'icudeath',
'hospdeath',
'icuid',
'unitdischargeyear',
'predictedICULOS',
'predictedHospitalLOS']

featlist= [col for col in pd_test_dummy.columns if col not in not_feat_list]

pd_test_dummy = pd_test_dummy[not_feat_list+featlist]



### FEEDFORWARD NETWORK
def utils_create_FCNet(inputs, num_layers, h_dim, h_fn, o_dim, o_fn, w_init, keep_prob=1.0, w_reg=None):
    '''
        GOAL             : Create FC network with different specifications 
        inputs (tensor)  : input tensor
        num_layers       : number of layers in FCNet
        h_dim  (int)     : number of hidden units
        h_fn             : activation function for hidden layers (default: tf.nn.relu)
        o_dim  (int)     : number of output units
        o_fn             : activation function for output layers (defalut: None)
        w_init           : initialization for weight matrix (defalut: Xavier)
        keep_prob        : keep probabilty [0, 1]  (if None, dropout is not employed)
    '''
    # default active functions (hidden: relu, out: None)
    if h_fn is None:
        h_fn = tf.nn.relu
    if o_fn is None:
        o_fn = None

    # default initialization functions (weight: Xavier, bias: None)
    if w_init is None:
        w_init = tf.contrib.layers.xavier_initializer() # Xavier initialization

    for layer in range(num_layers):
        if num_layers == 1:
            out = FC_Net(inputs, o_dim, activation_fn=o_fn, weights_initializer=w_init, weights_regularizer=w_reg)
        else:
            if layer == 0:
                h = FC_Net(inputs, h_dim, activation_fn=h_fn, weights_initializer=w_init, weights_regularizer=w_reg)
                if not keep_prob is None:
                    h = tf.nn.dropout(h, keep_prob=keep_prob)

            elif layer > 0 and layer != (num_layers-1): # layer > 0:
                h = FC_Net(h, h_dim, activation_fn=h_fn, weights_initializer=w_init, weights_regularizer=w_reg)
                if not keep_prob is None:
                    h = tf.nn.dropout(h, keep_prob=keep_prob)

            else: # layer == num_layers-1 (the last layer)
                out = FC_Net(h, o_dim, activation_fn=o_fn, weights_initializer=w_init, weights_regularizer=w_reg)

    return out



'''
This declare DeepHit architecture:

INPUTS:
    - input_dims: dictionary of dimension information
        > x_dim: dimension of features
        > num_Event: number of competing events (this does not include censoring label)
        > num_Category: dimension of time horizon of interest, i.e., |T| where T = {0, 1, ..., T_max-1}
                      : this is equivalent to the output dimension
    - network_settings:
        > h_dim_shared & num_layers_shared: number of nodes and number of fully-connected layers for the shared subnetwork
        > h_dim_CS & num_layers_CS: number of nodes and number of fully-connected layers for the cause-specific subnetworks
        > active_fn: 'relu', 'elu', 'tanh'
        > initial_W: Xavier initialization is used as a baseline

LOSS FUNCTIONS:
    - 1. loglikelihood (this includes log-likelihood of subjects who are censored)
    - 2. rankding loss (this is calculated only for acceptable pairs; see the paper for the definition)
    - 3. calibration loss (this is to reduce the calibration loss; this is not included in the paper version)
'''

_EPSILON = 1e-08



##### USER-DEFINED FUNCTIONS
def log(x):
    return tf.log(x + _EPSILON)

def div(x, y):
    return tf.div(x, (y + _EPSILON))


class Model_DeepHit:
    def __init__(self, sess, name, input_dims, network_settings):
        self.sess               = sess
        self.name               = name

        # INPUT DIMENSIONS
        self.x_dim              = input_dims['x_dim']

        self.num_Event          = input_dims['num_Event']
        self.num_Category       = input_dims['num_Category']

        # NETWORK HYPER-PARMETERS
        self.h_dim_shared       = network_settings['h_dim_shared']
        self.h_dim_CS           = network_settings['h_dim_CS']
        self.num_layers_shared  = network_settings['num_layers_shared']
        self.num_layers_CS      = network_settings['num_layers_CS']

        self.active_fn          = network_settings['active_fn']
        self.initial_W          = network_settings['initial_W']
        self.reg_W              = tf.contrib.layers.l2_regularizer(scale=1.0)
        self.reg_W_out          = tf.contrib.layers.l1_regularizer(scale=1.0)

        self._build_net()


    def _build_net(self):
        with tf.variable_scope(self.name):
            #### PLACEHOLDER DECLARATION
            self.mb_size     = tf.placeholder(tf.int32, [], name='batch_size')
            self.lr_rate     = tf.placeholder(tf.float32, [], name='learning_rate')
            self.keep_prob   = tf.placeholder(tf.float32, [], name='keep_probability')   #keeping rate
            self.a           = tf.placeholder(tf.float32, [], name='alpha')
            self.b           = tf.placeholder(tf.float32, [], name='beta')
            self.c           = tf.placeholder(tf.float32, [], name='gamma')

            self.x           = tf.placeholder(tf.float32, shape=[None, self.x_dim], name='inputs')
            self.k           = tf.placeholder(tf.float32, shape=[None, 1], name='labels')     #event/censoring label (censoring:0)
            self.t           = tf.placeholder(tf.float32, shape=[None, 1], name='timetoevents')

            self.fc_mask1    = tf.placeholder(tf.float32, shape=[None, self.num_Event, self.num_Category], name='mask1')  #for Loss 1
            self.fc_mask2    = tf.placeholder(tf.float32, shape=[None, self.num_Category], name='mask2')  #for Loss 2 / Loss 3


            ##### SHARED SUBNETWORK w/ FCNETS
            shared_out = utils_create_FCNet(self.x, self.num_layers_shared, self.h_dim_shared, self.active_fn, self.h_dim_shared, self.active_fn, self.initial_W, self.keep_prob, self.reg_W)
            last_x = self.x  #for residual connection

            h = tf.concat([last_x, shared_out], axis=1)

            #(num_layers_CS) layers for cause-specific (num_Event subNets)
            out = []
            for _ in range(self.num_Event):
                cs_out = utils_create_FCNet(h, (self.num_layers_CS), self.h_dim_CS, self.active_fn, self.h_dim_CS, self.active_fn, self.initial_W, self.keep_prob, self.reg_W)
                out.append(cs_out)
            out = tf.stack(out, axis=1) # stack referenced on subject
            out = tf.reshape(out, [-1, self.num_Event*self.h_dim_CS])
            out = tf.nn.dropout(out, keep_prob=self.keep_prob)

            out = FC_Net(out, self.num_Event * self.num_Category, activation_fn=tf.nn.softmax, 
                         weights_initializer=self.initial_W, weights_regularizer=self.reg_W_out, scope="Output")
            self.out = tf.reshape(out, [-1, self.num_Event, self.num_Category])


            ##### GET LOSS FUNCTIONS
            self.loss_Log_Likelihood()      #get loss1: Log-Likelihood loss
            self.loss_Ranking()             #get loss2: Ranking loss
            self.loss_Calibration()         #get loss3: Calibration loss

            self.LOSS_TOTAL = self.a*self.LOSS_1 + self.b*self.LOSS_2 + self.c*self.LOSS_3
            self.solver = tf.train.AdamOptimizer(learning_rate=self.lr_rate).minimize(self.LOSS_TOTAL)


    ### LOSS-FUNCTION 1 -- Log-likelihood loss
    def loss_Log_Likelihood(self):
        I_1 = tf.sign(self.k)

        #for uncenosred: log P(T=t,K=k|x)
        tmp1 = tf.reduce_sum(tf.reduce_sum(self.fc_mask1 * self.out, reduction_indices=2), reduction_indices=1, keep_dims=True)
        tmp1 = I_1 * log(tmp1)

        #for censored: log \sum P(T>t|x)
        tmp2 = tf.reduce_sum(tf.reduce_sum(self.fc_mask1 * self.out, reduction_indices=2), reduction_indices=1, keep_dims=True)
        tmp2 = (1. - I_1) * log(tmp2)

        self.LOSS_1 = - tf.reduce_mean(tmp1 + 1.0*tmp2)


    ### LOSS-FUNCTION 2 -- Ranking loss
    def loss_Ranking(self):
#x        sigma1 = tf.constant(0.1, dtype=tf.float32)
#x        sigma1 = tf.constant(0.65, dtype=tf.float32)
        
        sigma1 = tf.constant(0.65, dtype=tf.float32)
        eta = []
        for e in range(self.num_Event):
            one_vector = tf.ones_like(self.t, dtype=tf.float32)
            I_2 = tf.cast(tf.equal(self.k, e+1), dtype = tf.float32) #indicator for event
            I_2 = tf.diag(tf.squeeze(I_2))
            tmp_e = tf.reshape(tf.slice(self.out, [0, e, 0], [-1, 1, -1]), [-1, self.num_Category]) #event specific joint prob.

            R = tf.matmul(tmp_e, tf.transpose(self.fc_mask2)) #no need to divide by each individual dominator
            # r_{ij} = risk of i-th pat based on j-th time-condition (last meas. time ~ event time) , i.e. r_i(T_{j})

            diag_R = tf.reshape(tf.diag_part(R), [-1, 1])
            R = tf.matmul(one_vector, tf.transpose(diag_R)) - R # R_{ij} = r_{j}(T_{j}) - r_{i}(T_{j})
            R = tf.transpose(R)                                 # Now, R_{ij} (i-th row j-th column) = r_{i}(T_{i}) - r_{j}(T_{i})

            T = tf.nn.relu(tf.sign(tf.matmul(one_vector, tf.transpose(self.t)) - tf.matmul(self.t, tf.transpose(one_vector))))
            # T_{ij}=1 if t_i < t_j  and T_{ij}=0 if t_i >= t_j

            T = tf.matmul(I_2, T) # only remains T_{ij}=1 when event occured for subject i

            tmp_eta = tf.reduce_mean(T * tf.exp(-R/sigma1), reduction_indices=1, keep_dims=True)

            eta.append(tmp_eta)
        eta = tf.stack(eta, axis=1) #stack referenced on subjects
        eta = tf.reduce_mean(tf.reshape(eta, [-1, self.num_Event]), reduction_indices=1, keep_dims=True)

        self.LOSS_2 = tf.reduce_sum(eta) #sum over num_Events



    ### LOSS-FUNCTION 3 -- Calibration Loss
    def loss_Calibration(self):
        eta = []
        for e in range(self.num_Event):
            one_vector = tf.ones_like(self.t, dtype=tf.float32)
            I_2 = tf.cast(tf.equal(self.k, e+1), dtype = tf.float32) #indicator for event
            tmp_e = tf.reshape(tf.slice(self.out, [0, e, 0], [-1, 1, -1]), [-1, self.num_Category]) #event specific joint prob.

            r = tf.reduce_sum(tmp_e * self.fc_mask2, axis=0) #no need to divide by each individual dominator
            tmp_eta = tf.reduce_mean((r - I_2)**2, reduction_indices=1, keep_dims=True)

            eta.append(tmp_eta)
        eta = tf.stack(eta, axis=1) #stack referenced on subjects
        eta = tf.reduce_mean(tf.reshape(eta, [-1, self.num_Event]), reduction_indices=1, keep_dims=True)

        self.LOSS_3 = tf.reduce_sum(eta) #sum over num_Events

    
    def get_cost(self, DATA, MASK, PARAMETERS, keep_prob, lr_train):
        (x_mb, k_mb, t_mb) = DATA
        (m1_mb, m2_mb) = MASK
        (alpha, beta, gamma) = PARAMETERS
        return self.sess.run(self.LOSS_TOTAL, 
                             feed_dict={self.x:x_mb, self.k:k_mb, self.t:t_mb, self.fc_mask1: m1_mb, self.fc_mask2:m2_mb, 
                                        self.a:alpha, self.b:beta, self.c:gamma, 
                                        self.mb_size: np.shape(x_mb)[0], self.keep_prob:keep_prob, self.lr_rate:lr_train})
# No need for load !!!lb!!!
#    def train(self, DATA, MASK, PARAMETERS, keep_prob, lr_train):
#        (x_mb, k_mb, t_mb) = DATA
#        (m1_mb, m2_mb) = MASK
#        (alpha, beta, gamma) = PARAMETERS
#        return self.sess.run([self.solver, self.LOSS_TOTAL], 
#                             feed_dict={self.x:x_mb, self.k:k_mb, self.t:t_mb, self.fc_mask1: m1_mb, self.fc_mask2:m2_mb, 
#                                        self.a:alpha, self.b:beta, self.c:gamma, 
#                                        self.mb_size: np.shape(x_mb)[0], self.keep_prob:keep_prob, self.lr_rate:lr_train})
    
    def predict(self, x_test, keep_prob=1.0):
        return self.sess.run(self.out, feed_dict={self.x: x_test, self.mb_size: np.shape(x_test)[0], self.keep_prob: keep_prob})





'''
This provide the dimension/data/mask to train/test the network.

Once must construct a function similar to "import_dataset_SYNTHETIC":
    - DATA FORMAT:
        > data: covariates with x_dim dimension.
        > label: 0: censoring, 1 ~ K: K competing(single) risk(s)
        > time: time-to-event or time-to-censoring
    - Based on the data, creat mask1 and mask2 that are required to calculate loss functions.
'''



# This is called even for test, so might be needed to save std of every variable and load hard copy here !!!lb!!!

##### DEFINE USER-FUNCTIONS #####
def impt_f_get_Normalization(X, norm_mode):
    num_Patient, num_Feature = np.shape(X)

    if norm_mode == 'standard': #zero mean unit variance
        for j in range(num_Feature):
            if np.std(X[:,j]) != 0:
                X[:,j] = (X[:,j] - np.mean(X[:, j]))/np.std(X[:,j])
            else:
                X[:,j] = (X[:,j] - np.mean(X[:, j]))
    elif norm_mode == 'normal': #min-max normalization
        for j in range(num_Feature):
            X[:,j] = (X[:,j] - np.min(X[:,j]))/(np.max(X[:,j]) - np.min(X[:,j]))
    else:
        print("INPUT MODE ERROR!")

    return X

### MASK FUNCTIONS
'''
    fc_mask2      : To calculate LOSS_1 (log-likelihood loss)
    fc_mask3      : To calculate LOSS_2 (ranking loss)
'''
def impt_f_get_fc_mask2(time, label, num_Event, num_Category):
    '''
        mask4 is required to get the log-likelihood loss
        mask4 size is [N, num_Event, num_Category]
            if not censored : one element = 1 (0 elsewhere)
            if censored     : fill elements with 1 after the censoring time (for all events)
    '''
    mask = np.zeros([np.shape(time)[0], num_Event, num_Category]) # for the first loss function
    for i in range(np.shape(time)[0]):
        if label[i,0] != 0:  #not censored
            mask[i,int(label[i,0]-1),int(time[i,0])] = 1
        else: #label[i,2]==0: censored
            mask[i,:,int(time[i,0]+1):] =  1 #fill 1 until from the censoring time (to get 1 - \sum F)
    return mask


def impt_f_get_fc_mask3(time, meas_time, num_Category):
    '''
        mask5 is required calculate the ranking loss (for pair-wise comparision)
        mask5 size is [N, num_Category].
        - For longitudinal measurements:
             1's from the last measurement to the event time (exclusive and inclusive, respectively)
             denom is not needed since comparing is done over the same denom
        - For single measurement:
             1's from start to the event time(inclusive)
    '''
    mask = np.zeros([np.shape(time)[0], num_Category]) # for the first loss function
    if np.shape(meas_time):  #lonogitudinal measurements
        for i in range(np.shape(time)[0]):
            t1 = int(meas_time[i, 0]) # last measurement time
            t2 = int(time[i, 0]) # censoring/event time
            mask[i,(t1+1):(t2+1)] = 1  #this excludes the last measurement time and includes the event time
    else:                    #single measurement
        for i in range(np.shape(time)[0]):
            t = int(time[i, 0]) # censoring/event time
            mask[i,:(t+1)] = 1  #this excludes the last measurement time and includes the event time
    return mask


  
def impt_import_dataset_xliu(norm_mode='standard'):
    #in_filename = './sample data/nbm/test.csv'
    #df = pd.read_csv(in_filename, sep=',')
    df = pd_test_dummy
    
    label           = np.asarray(df[['icudeath']] + 1)
    time            = np.asarray(df[['iculos']])
    data            = np.asarray(df.iloc[:,8:])
    data            = impt_f_get_Normalization(data, norm_mode)

    num_Category    = int(np.max(time) * 1.2)  #to have enough time-horizon
    num_Event       = int(len(np.unique(label))) #only count the number of events (do not count censoring as an event)
    
    x_dim           = np.shape(data)[1]

    mask1           = impt_f_get_fc_mask2(time, label, num_Event, num_Category)
    mask2           = impt_f_get_fc_mask3(time, -1, num_Category)

    DIM             = (x_dim)
    DATA            = (data, time, label)
    MASK            = (mask1, mask2)

    return DIM, DATA, MASK



### MODEL LOAD AND PREDICT

file_path_final='./'

gregorio_tabajara= pkl.load(open(file_path_final+'Los_v2_par.pkl','rb'))


input_dims=gregorio_tabajara['input_dims']
network_settings=gregorio_tabajara['network_settings_part']
network_settings['initial_W']=tf.contrib.layers.xavier_initializer()


(x_dim), (data, time, label), (mask1, mask2) = impt_import_dataset_xliu(norm_mode = 'standard')

tf.reset_default_graph()
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)


model = Model_DeepHit(sess, "DeepHit", input_dims, network_settings)
saver = tf.compat.v1.train.Saver()
sess.run(tf.global_variables_initializer())
saver.restore(sess, file_path_final + 'Los_v2')


#making one prediction 
pred = model.predict([data[0,:]]) 


print(pred)
print(pred.shape)



