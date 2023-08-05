
from deephit import *
import pickle as pkl


# to save the trained model
file_model_path_final='./dbfs/FileStore/v2noairway/'
filenamemodel='Losv2_311'

mb_size=128
evalstep=100 #evalstep was 100 for mb_size=128
CindexEvalStep=10000
MAX_ITR=2000
MAX_ITR=800   #10000  sonhei com este numero

num_layers_shared           = 2
num_layers_CS               = 2

range_alpha =[3]
range_beta  =[1]
range_gamma =[1] # gamma=0 there is no calibration loss contribution
base_range  =[(a,b,c) for a in range_alpha for b in range_beta for c in range_gamma]
random.shuffle(base_range)

#priority_params=[(3,1,1),(1,1,1),(3,1,0),(1,1,0)]
#params_abc=priority_params+[it for it in base_range if it not in priority_params]
params_abc=base_range
print(params_abc)



pd_train_test=pd.read_csv('/dbfs/FileStore/LOS/pd_train_test.csv')

pd_train_test=pd_train_test.sample(frac=1,random_state=1234) # scrambling because I'm splitting later !!!lb!!!
split_train_size=int(np.floor(0.6*pd_train_test.shape[0]))


# lb: removed other dummies dataframe
### a different way to do one hot encode: get dummies, output is a dataframe
pd_train_test_dummy = pd.get_dummies(pd_train_test, prefix_sep='_', drop_first = True)


# lb: hat to change the order of the cells, because pd_train_test_dummy was being transformed before being created.  Also removed unused variables and modules ( onehotencode for example)
# sanity checkpoint: columns are manually reordered, just checking if it makes sense
columns_check1=pd_train_test_dummy.columns
#columns_check1

# COMMAND ----------

### !!!lb!!! change to drop!!
### cap iculos at 30 days
pd_train_test_dummy.head(10)
pd_train_test_dummy['iculos'] = np.where(pd_train_test_dummy['iculos'] >720, 720, pd_train_test_dummy['iculos'])
#pd_train_test_dummy['iculos'].describe()



# COMMAND ----------

### reorder the columns for easy data load later
not_feat_list=['iculos',
 'hosplos',
 'icudeath',
 'hospdeath',
 'icuid',
 'unitdischargeyear',
 'predictedICULOS',
 'predictedHospitalLOS']

featlist= [col for col in pd_train_test_dummy.columns if col not in not_feat_list]

pd_train_test_dummy = pd_train_test_dummy[not_feat_list+featlist]


# COMMAND ----------

set(pd_train_test_dummy.columns)==set(columns_check1)
 # lb: ok columns are fine

# COMMAND ----------

# pd_train_test_dummy.shape
# 1213307/2021749
# lb: means a 60:40 train: test

# COMMAND ----------

pd_train_test_dummy.shape

# COMMAND ----------


### replit into training and testing
pd_train_dummy = pd_train_test_dummy.iloc[0:split_train_size,]
pd_test_dummy = pd_train_test_dummy.iloc[split_train_size+1:,]

pd_test=pd_train_test.iloc[split_train_size+1:,]

pd_test.to_csv('/dbfs/FileStore/LOS/los_testV2.csv')

print(pd_train_dummy.shape, pd_test_dummy.shape)


# COMMAND ----------

pd.set_option('max_columns', None)
pd_train_test_dummy.head(10)

# COMMAND ----------

### filter down to a smaller set for code development 
pd_train_sml = pd_train_dummy[pd_train_dummy.unitdischargeyear.eq(2017) | pd_train_dummy.unitdischargeyear.eq(2018)]
pd_train_sml.shape


# COMMAND ----------

pd_train_sml.shape

# COMMAND ----------

#lb: from deep hit repo starts-------------------------------->

# COMMAND ----------

# lb: ref: https://github.com/chl8856/DeepHit/blob/master/utils_network.py

###utility network

### CONSTRUCT MULTICELL FOR MULTI-LAYER RNNS
def utils_create_rnn_cell(num_units, num_layers, keep_prob, RNN_type): 
    '''
        GOAL         : create multi-cell (including a single cell) to construct multi-layer RNN
        num_units    : number of units in each layer
        num_layers   : number of layers in MulticellRNN
        keep_prob    : keep probabilty [0, 1]  (if None, dropout is not employed)
        RNN_type     : either 'LSTM' or 'GRU'
    '''
    cells = []
    for _ in range(num_layers):
        if RNN_type == 'GRU':
            cell = tf.contrib.rnn.GRUCell(num_units)
        elif RNN_type == 'LSTM':
            cell = tf.contrib.rnn.LSTMCell(num_units)
        if not keep_prob is None:
            cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=keep_prob)
        cells.append(cell)
    cell = tf.contrib.rnn.MultiRNNCell(cells)
    
    return cell

### EXTRACT STATE OUTPUT OF MULTICELL-RNNS
def utils_create_concat_state(state, num_layers, RNN_type):
    '''
        GOAL	     : concatenate the tuple-type tensor (state) into a single tensor
        state        : input state is a tuple ofo MulticellRNN (i.e. output of MulticellRNN)
                       consist of only hidden states h for GRU and hidden states c and h for LSTM
        num_layers   : number of layers in MulticellRNN
        RNN_type     : either 'LSTM' or 'GRU'
    '''
    for i in range(num_layers):
        if RNN_type == 'LSTM':
            tmp = state[i][1] ## i-th layer, h state for LSTM
        elif RNN_type == 'GRU':
            tmp = state[i] ## i-th layer, h state for GRU
        else:
            print('ERROR: WRONG RNN CELL TYPE')

        if i == 0:
            rnn_state_out = tmp
        else:
            rnn_state_out = tf.concat([rnn_state_out, tmp], axis = 1)
    
    return rnn_state_out


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

# COMMAND ----------


# lb: ref: https://github.com/chl8856/DeepHit/blob/master/class_DeepHit.py
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


### user-defined functions
# import utils_network as utils

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

            self.LOSS_TOTAL = self.a*self.LOSS_1 + self.b*self.LOSS_2 + self.c*self.LOSS_3 #+ tf.losses.get_regularization_loss() 
            #!!!lb!!! XL had removed this regularization term!!! putting it back for a try.
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

    def train(self, DATA, MASK, PARAMETERS, keep_prob, lr_train):
        (x_mb, k_mb, t_mb) = DATA
        (m1_mb, m2_mb) = MASK
        (alpha, beta, gamma) = PARAMETERS
        return self.sess.run([self.solver, self.LOSS_TOTAL], 
                             feed_dict={self.x:x_mb, self.k:k_mb, self.t:t_mb, self.fc_mask1: m1_mb, self.fc_mask2:m2_mb, 
                                        self.a:alpha, self.b:beta, self.c:gamma, 
                                        self.mb_size: np.shape(x_mb)[0], self.keep_prob:keep_prob, self.lr_rate:lr_train})
    
    def predict(self, x_test, keep_prob=1.0):
        return self.sess.run(self.out, feed_dict={self.x: x_test, self.mb_size: np.shape(x_test)[0], self.keep_prob: keep_prob})

    # def predict(self, x_test, MASK, keep_prob=1.0):
    #     (m1_test, m2_test) = MASK
    #     return self.sess.run(self.out, 
    #                          feed_dict={self.x: x_test, self.rnn_mask1:m1_test, self.rnn_mask2:m2_test, self.keep_prob: keep_prob})

# COMMAND ----------


# lb: ref: https://github.com/chl8856/DeepHit/blob/master/utils_eval.py

'''
This provide time-dependent Concordance index and Brier Score:
    - Use weighted_c_index and weighted_brier_score, which are the unbiased estimates.
    
See equations and descriptions eq. (11) and (12) of the following paper:
    - C. Lee, W. R. Zame, A. Alaa, M. van der Schaar, "Temporal Quilting for Survival Analysis", AISTATS 2019
'''


### C(t)-INDEX CALCULATION
def c_index(Prediction, Time_survival, Death, Time):
    '''
        This is a cause-specific c(t)-index
        - Prediction      : risk at Time (higher --> more risky)
        - Time_survival   : survival/censoring time
        - Death           :
            > 1: death
            > 0: censored (including death from other cause)
        - Time            : time of evaluation (time-horizon when evaluating C-index)
    '''
    N = len(Prediction)
    A = np.zeros((N,N))
    Q = np.zeros((N,N))
    N_t = np.zeros((N,N))
    Num = 0
    Den = 0
    for i in range(N):
        A[i, np.where(Time_survival[i] < Time_survival)] = 1
        Q[i, np.where(Prediction[i] > Prediction)] = 1
  
        if (Time_survival[i]<=Time and Death[i]==1):
            N_t[i,:] = 1

    Num  = np.sum(((A)*N_t)*Q)
    Den  = np.sum((A)*N_t)

    if Num == 0 and Den == 0:
        result = -1 # not able to compute c-index!
    else:
        result = float(Num/Den)

    return result

### BRIER-SCORE
def brier_score(Prediction, Time_survival, Death, Time):
    N = len(Prediction)
    y_true = ((Time_survival <= Time) * Death).astype(float)

    return np.mean((Prediction - y_true)**2)

    # result2[k, t] = brier_score_loss(risk[:, k], ((te_time[:,0] <= eval_horizon) * (te_label[:,0] == k+1)).astype(int))


##### WEIGHTED C-INDEX & BRIER-SCORE
def CensoringProb(Y, T):

    T = T.reshape([-1]) # (N,) - np array
    Y = Y.reshape([-1]) # (N,) - np array

    kmf = KaplanMeierFitter()
    kmf.fit(T, event_observed=(Y==0).astype(int))  # censoring prob = survival probability of event "censoring"
    G = np.asarray(kmf.survival_function_.reset_index()).transpose()
    G[1, G[1, :] == 0] = G[1, G[1, :] != 0][-1]  #fill 0 with ZoH (to prevent nan values)
    
    return G


### C(t)-INDEX CALCULATION: this account for the weighted average for unbaised estimation
def weighted_c_index(T_train, Y_train, Prediction, T_test, Y_test, Time):
    '''
        Thi6@gmail.coms is a cause-specific c(t)-index
        - Prediction      : risk at Time (higher --> more risky)
        - Time_survival   : survival/censoring time
        - Death           :
            > 1: death
            > 0: censored (including death from other cause)
        - Time            : time of evaluation (time-horizon when evaluating C-index)
    '''
    G = CensoringProb(Y_train, T_train)

    N = len(Prediction)
    A = np.zeros((N,N))
    Q = np.zeros((N,N))
    N_t = np.zeros((N,N))
    Num = 0
    Den = 0
    for i in range(N):
        tmp_idx = np.where(G[0,:] >= T_test[i])[0]

        if len(tmp_idx) == 0:
            W = (1./G[1, -1])**2
        else:
            W = (1./G[1, tmp_idx[0]])**2

        A[i, np.where(T_test[i] < T_test)] = 1. * W
        Q[i, np.where(Prediction[i] > Prediction)] = 1. # give weights

        if (T_test[i]<=Time and Y_test[i]==1):
            N_t[i,:] = 1.

    Num  = np.sum(((A)*N_t)*Q)
    Den  = np.sum((A)*N_t)

    if Num == 0 and Den == 0:
        result = -1 # not able to compute c-index!
    else:
        result = float(Num/Den)

    return result


# this account for the weighted average for unbaised estimation
def weighted_brier_score(T_train, Y_train, Prediction, T_test, Y_test, Time):
    G = CensoringProb(Y_train, T_train)
    N = len(Prediction)

    W = np.zeros(len(Y_test))
    Y_tilde = (T_test > Time).astype(float)

    for i in range(N):
        tmp_idx1 = np.where(G[0,:] >= T_test[i])[0]
        tmp_idx2 = np.where(G[0,:] >= Time)[0]

        if len(tmp_idx1) == 0:
            G1 = G[1, -1]
        else:
            G1 = G[1, tmp_idx1[0]]

        if len(tmp_idx2) == 0:
            G2 = G[1, -1]
        else:
            G2 = G[1, tmp_idx2[0]]
        W[i] = (1. - Y_tilde[i])*float(Y_test[i])/G1 + Y_tilde[i]/G2

    y_true = ((T_test <= Time) * Y_test).astype(float)

    return np.mean(W*(Y_tilde - (1.-Prediction))**2)




# COMMAND ----------

# lb: ref: https://github.com/chl8856/DeepHit/blob/master/import_data.py 
# difference is that
# import_data was imported with name impt
# here XL uses impt.FUNCTION as impt_FUNCTION and adapted his function

'''
This provide the dimension/data/mask to train/test the network.

Once must construct a function similar to "import_dataset_SYNTHETIC":
    - DATA FORMAT:
        > data: covariates with x_dim dimension.
        > label: 0: censoring, 1 ~ K: K competing(single) risk(s)
        > time: time-to-event or time-to-censoring
    - Based on the data, creat mask1 and mask2 that are required to calculate loss functions.
'''


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


def impt_import_dataset_SYNTHETIC(norm_mode='standard'): ## lb: XL is treating this as train
    #in_filename = './sample data/nbm/train.csv'
    #df = pd.read_csv(in_filename, sep=',')
    df = pd_train_sml  # lb: XL edited here !!!! should be passed as arg though
    
    label           = np.asarray(df[['icudeath']] + 1) # lb: XL edited here !!!! 
    time            = np.asarray(df[['iculos']]) # lb: XL edited here !!!! 
    data            = np.asarray(df.iloc[:,8:]) # lb: XL edited here !!!! 
    data            = impt_f_get_Normalization(data, norm_mode)

    num_Category    = int(np.max(time) * 1.2)  #to have enough time-horizon #lb: same as original. what does it mean??
    num_Event       = int(len(np.unique(label))) #only count the number of events (do not count censoring as an event)
    
    x_dim           = np.shape(data)[1]

    mask1           = impt_f_get_fc_mask2(time, label, num_Event, num_Category) # lb: same as original. i dont understand this function 
    mask2           = impt_f_get_fc_mask3(time, -1, num_Category)

    DIM             = (x_dim)
    DATA            = (data, time, label)
    MASK            = (mask1, mask2)

    return DIM, DATA, MASK


def impt_import_dataset_xliu(norm_mode='standard'):  ## lb: XL is treating this as test, but should do the same as the above
    #in_filename = './sample data/nbm/test.csv'
    #df = pd.read_csv(in_filename, sep=',')
    df = pd_test_dummy.iloc[0:200000,] # lb: should be passing this as argument
    
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


def impt_import_dataset_METABRIC(norm_mode='standard'):
    in_filename1 = './sample data/METABRIC/cleaned_features_final.csv'
    in_filename2 = './sample data/METABRIC/label.csv'

    df1 = pd.read_csv(in_filename1, sep =',')
    df2 = pd.read_csv(in_filename2, sep =',')

    data  = np.asarray(df1)
    data  = impt_f_get_Normalization(data, norm_mode)
    
    time  = np.asarray(df2[['event_time']])
    # time  = np.round(time/12.) #unit time = month
    label = np.asarray(df2[['label']])

    
    num_Category    = int(np.max(time) * 1.2)        #to have enough time-horizon
    num_Event       = int(len(np.unique(label)) - 1) #only count the number of events (do not count censoring as an event)

    x_dim           = np.shape(data)[1]

    mask1           = impt_f_get_fc_mask2(time, label, num_Event, num_Category)
    mask2           = impt_f_get_fc_mask3(time, -1, num_Category)

    DIM             = (x_dim)
    DATA            = (data, time, label)
    MASK            = (mask1, mask2)

    return DIM, DATA, MASK

# COMMAND ----------

#lb: from deep hit repo ends--------------------------------

# COMMAND ----------


# lb: from get_main.py

###x other utilities used

### random with replace minibatches function    
def f_get_minibatch(mb_size, x, label, time, mask1, mask2):
    idx = range(np.shape(x)[0])
    idx = random.sample(idx, mb_size)

    x_mb = x[idx, :].astype(np.float32)
    k_mb = label[idx, :].astype(np.float32) # censoring(0)/event(1,2,..) label
    t_mb = time[idx, :].astype(np.float32)
    m1_mb = mask1[idx, :, :].astype(np.float32) #fc_mask
    m2_mb = mask2[idx, :].astype(np.float32) #fc_mask
    return x_mb, k_mb, t_mb, m1_mb, m2_mb


# COMMAND ----------

# play: beta, gamma, batch size


mb_size                     = 128 #lb: SET_BATCH_SIZE last val
keep_prob                   = 0.6 # lb:same val
lr_train                    = 0.0001 # lb:same val
h_dim_shared                = 300
h_dim_CS                    = 200
num_layers_shared           = 2
num_layers_CS               = 2
active_fn                   = tf.nn.elu # lb: options are relu, elu and tanh
eval_time = [4, 11, 15, 18, 21, 23, 26, 29, 34, 39, 43, 47, 53, 62, 70, 82, 97, 120, 162, 247, 360, 719]

seed = 4321 # for split

initial_W                   = tf.contrib.layers.xavier_initializer()

      
#lb: in the paper synthetic is the name of data with competing risks
(x_dim), (data, time, label), (mask1, mask2) = impt_import_dataset_SYNTHETIC(norm_mode = 'standard')

_, num_Event, num_Category  = np.shape(mask1) 


##### MAKE DICTIONARIES
# INPUT DIMENSIONS
input_dims                  = { 'x_dim'         : x_dim,
                                'num_Event'     : num_Event,
                                'num_Category'  : num_Category}

# NETWORK HYPER-PARMETERS
network_settings            = { 'h_dim_shared'         : h_dim_shared,
                                'h_dim_CS'          : h_dim_CS,
                                'num_layers_shared'    : num_layers_shared,
                                'num_layers_CS'    : num_layers_CS,
                                'active_fn'      : active_fn,
                                'initial_W'         : initial_W }



# COMMAND ----------

def xbatchpredict(xdata,xfunc, n=10000):
    xlength = len(xdata)
    #print("BatchSubmitPrediction, total size= " + str(xlength))
    for xindex in range (0, xlength, n):
        x_pred_xindex = xfunc(xdata[xindex: xindex + n, :])
        if xindex == 0:
            pred_x = x_pred_xindex
        else:
            pred_x = np.concatenate((pred_x, x_pred_xindex), axis=0)
            print(np.shape(pred_x))
    return pred_x 
  
def xprob2los(xdata):
  
  pred1 = xdata[:,0,:]
  pred2 = xdata[:,1,:]
  pred3 = pred1 + pred2
  predlosmean = np.multiply(pred3, np.arange(1,865,1))
  xlos=predlosmean.cumsum(axis=1)[:,863]
  
  data_output= pd.concat([pd_test_dummy[['iculos']].reset_index(),
                          pd.DataFrame(pd_test_dummy[['icudeath']]).reset_index(),
                          
                          pd.DataFrame(xlos)
                         ], 
  axis=1, ignore_index=True)

  column_newname = ["index1","iculos","index2", "icudeath", "newlos"] # why called median here ? !!!lb!!!
  data_output.columns = column_newname
  
  return data_output  

# COMMAND ----------

print('bug is here...')

# COMMAND ----------

##### CREATE DEEPFHT NETWORK

### TRAINING-TESTING SPLIT
### make 10,000 sample out of the training set for monitoring of iterations (early stops)
(tr_data,mte_data, tr_time,mte_time, tr_label,mte_label, 
 tr_mask1,mte_mask1, tr_mask2,mte_mask2)  = train_test_split(data, time, label, mask1, mask2, test_size=10000, random_state=seed)

# hope all configs reset in loop

for pind in range(len(params_abc)):
  alpha,beta,gamma=params_abc[pind]
  print('\n\n\n'+'-'*1000+'\n\t alpha,beta,gamma=',alpha,beta,gamma,'\n\n')
    
  tf.reset_default_graph()
  config = tf.ConfigProto() 
  config.gpu_options.allow_growth = True
  sess = tf.Session(config=config)
  model = Model_DeepHit(sess, "DeepHit", input_dims, network_settings)
  saver = tf.train.Saver()
  sess.run(tf.global_variables_initializer())

  dparams={'mb_size':mb_size, 'keep_prob':keep_prob, 'lr_train':lr_train , 'h_dim_shared':h_dim_shared , 'h_dim_CS':h_dim_CS , 'num_layers_shared':num_layers_shared, 'num_layers_CS':num_layers_CS, 'alpha':alpha,  'beta':beta, 'gamma':gamma,'eval_time':eval_time}    
  dmetrics={'itr':[],'batch loss':[],'average C-index':[],'DeathP':[],'DeathA':[],'AUC':[],'R2':[],'RMSE':[]}

  avg_loss = 0  
  for itr in range(MAX_ITR):  
      x_mb, k_mb, t_mb, m1_mb, m2_mb = f_get_minibatch(mb_size, tr_data, tr_label, tr_time, tr_mask1, tr_mask2)
      DATA = (x_mb, k_mb, t_mb)
      MASK = (m1_mb, m2_mb)
      PARAMETERS = (alpha, beta, gamma)
      _, loss_curr = model.train(DATA, MASK, PARAMETERS, keep_prob, lr_train)

      pred = model.predict(mte_data)
      mte_result1 = np.zeros([num_Event, len(eval_time)])
      avg_loss += loss_curr/mb_size # !!!lb!!! was 128, changed here!!!

      if (itr+1)%(evalstep) == 0:
          for t, t_time in enumerate(eval_time):
              eval_horizon = int(t_time)

              if eval_horizon >= num_Category:
                  print('ERROR: evaluation horizon is out of range')
                  mte_result1[:, t] = mte_result1[:, t] = -1
              else:
                  if ((itr+1)%1000 ==0) : # only calc C index  a few times
                    risk = np.sum(pred[:,:,:(eval_horizon+1)], axis=2) #risk score until eval_time
                    for k in range(num_Event):
                       mte_result1[k, t] = weighted_c_index(\
                                  tr_time, (tr_label[:,0] == k+1).astype(int), \
                                  risk[:,k], \
                                  mte_time, (mte_label[:,0] == k+1).astype(int), \
                                  eval_horizon)
                  
          tmp_valid = np.mean(mte_result1)

          pred1 = pred[:,0,:]
          pred2 = pred[:,1,:]
          pred1_cum = pred1.cumsum(axis=1)
          pred2_cum = pred2.cumsum(axis=1)
          pred1_max = pred1_cum[:,np.shape(mte_mask2)[1] - 1]
          pred2_max = pred2_cum[:,np.shape(mte_mask2)[1] - 1]
          tmp_death = np.mean(pred2_max)
          act_death = np.mean(abs(mte_label - 1))
          auc = roc_auc_score(abs(mte_label - 1), pred2_max)

          pred3 = pred1 + pred2
          pred3_cum = pred3.cumsum(axis=1) # lb: introducing here because pred3_cum was missing and this is where it makes sense to have it generated.
          predlosmean = np.multiply(pred3, np.arange(1,865,1))  # lb: not the right was 5162 i changed it to 865
          xlos=predlosmean.cumsum(axis=1)[:,863] # was 5160, changed it to 863: compatible with time horizon: this is a transformation from 719 in tim_eval per 1.2  

          mae = metrics.mean_absolute_error(mte_time, xlos)
          mse = metrics.mean_squared_error(mte_time, xlos)
          rmse = np.sqrt(mse)
          r2 = metrics.r2_score(mte_time, xlos) 
          metrics.r2_score
          
          dmetrics_temp={'itr':itr,'batch loss':avg_loss,'average C-index':tmp_valid,'DeathP':tmp_death,'DeathA':act_death,'AUC':auc,'R2':r2,'RMSE':rmse}
          for key in dmetrics.keys():
            dmetrics[key].append(dmetrics_temp[key])
          
          print('itr: ' + str('%04d' % (itr)) +  \
                ',batch loss: ' + str('%.4f' %(avg_loss)) + \
                ',average C-index : ' + str('%.4f' %(tmp_valid)) + \
                ',DeathP: ' + str('%.4f' %(tmp_death)) + \
                ',DeathA: ' + str('%.4f' %(act_death)) + \
                ',AUC: ' + str('%.4f' %(auc))     + \
                ' R2 ' + str('%.4f' %(r2)) + ' RMSE ' + str('%.4f' %(rmse)))

          avg_loss = 0
  ###make predictions on the testing set
  (x_dim), (train, time, label), (mask1, mask2) = impt_import_dataset_SYNTHETIC(norm_mode = 'standard')
  (x_dim), (test, time, label), (mask1, mask2)  = impt_import_dataset_xliu(norm_mode = 'standard')
  pred_train = xbatchpredict(train, model.predict, n=10000)
  pred_test = xbatchpredict(test, model.predict, n=10000)
  data_output=xprob2los(pred_test)   
  pkl.dump({'params':dparams,'metrics':dmetrics,'pred_train':pred_train,'pred_test':pred_test,
                                                  'data_output':data_output},open(fileprefix+str(alpha)+str(beta)+str(gamma)+'.pkl','wb'))
  

# COMMAND ----------

# DBTITLE 1,Saving Model
#import pickle as pkl

def save_model_tf(sess, input_dims, network_settings):
    saver = tf.compat.v1.train.Saver()
    sess.run(tf.global_variables_initializer())
    dpar={'input_dims':input_dims,
          'network_settings_part':{ 'h_dim_shared'         : h_dim_shared,
                                  'h_dim_CS'          : h_dim_CS,
                                  'num_layers_shared'    : num_layers_shared,
                                  'num_layers_CS'    : num_layers_CS,
                                  'active_fn'      : active_fn
                                  }
         }
    saver.save(sess, file_model_path_final + filenamemodel)
    pkl.dump(dpar,open(file_model_path_final+filenamemodel+'_par.pkl','wb'))



# COMMAND ----------

save_model_tf(sess, input_dims, network_settings)

# COMMAND ----------

#pd_test_dummy.to_csv('/dbfs/FileStore/LOS/los_testhotV2.csv')

# COMMAND ----------


# evaluate lin reg. 
# plot with seaborn 
# make tests individual predictions instead of batches
# test model with hourly data


# COMMAND ----------

from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import seaborn as sns

# COMMAND ----------

# MAGIC %fs ls  FileStore/v2noairway

# COMMAND ----------

# MAGIC %fs ls  FileStore/v2noairway

# COMMAND ----------

print(data_output.shape,data_output[data_output.newlos.notna()].shape)
data_output[data_output.newlos.notna()].sample(10)

# COMMAND ----------

X=np.asarray([[it] for it in  data_output[(data_output.newlos).notna()]['newlos']])
y=np.asarray(data_output[(data_output.newlos).notna()]['iculos'])
reg = LinearRegression().fit(X, y)
print(alpha, beta, gamma, reg.score(X, y),reg.coef_,reg.intercept_)


# COMMAND ----------

#print(pd_train_test_dummy[pd_train_test_dummy.iculos>=720].shape[0]/pd_train_test_dummy.shape[0])
data_output['newlos_cor']=data_output['newlos']*reg.coef_ +reg.intercept_
sns.jointplot(data=data_output.sample(10000), x="newlos_cor", y="iculos", kind="reg")
plt.xlim([0,200])
plt.ylim([0,200])

# COMMAND ----------

data_output[data_output.newlos.notna()][['iculos','newlos_cor','icudeath']].sample(200).sort_values(by='newlos_cor')

# COMMAND ----------

for col in pd_test_dummy.columns:
  print(col)

# COMMAND ----------

pd_test_dummy

# COMMAND ----------


