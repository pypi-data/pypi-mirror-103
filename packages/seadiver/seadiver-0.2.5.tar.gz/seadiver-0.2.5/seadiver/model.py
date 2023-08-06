#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

import copy
import time
import json

import matplotlib as mpl
import matplotlib.pyplot as plt


class ANN():
    
    def __init__(self, input_shape, structure, output, activation= "sigmoid", loss = "auto", initializer = "auto", strict=False, delta=1e-7):
        
        #describes compatible parameters
    
        self.compat_activation_functions = {"sigmoid", "relu", "softmax", "identity"}
        self.compat_loss_functions = {"cross_entropy", "mean_square", "auto"}
        self.compat_initializers = {"uniform", "normal", "xabier", "he", "auto"}
        
        #model identity
        
        self.w_layers = []
        self.b_layers = []
        self.activations = []
        
        self.input_shape = input_shape
        self.structure = structure
        self.strict = strict
        self.delta = delta
        self.initializer = None
        self.output= None
        self.loss = None
        
        #fields for temporal use and calculation
        
        self.w_gradients = []
        self.b_gradients = []
        
        self.fan_ins = []
        self.fan_outs = []
        
        self.error_log = []
        
        
        #initialize fields if given parameters are valid
        
        if initializer not in self.compat_initializers:
            raise Exception("invalid initialzier name")
        else:
            self.initializer = initializer
            
        if output not in self.compat_activation_functions:
            raise Exception("invalid output function name")
        else:
            self.output = output
            
        if loss not in self.compat_loss_functions:
            raise Exception("invalid loss function name")
        else:
            
            if loss == "auto":

                if output == "softmax":
                    self.loss = "cross_entropy"
                    
                elif output == "identity":
                    self.loss = "mean_square"
                
                elif output == "relu":
                    self.loss = "mean_square"

                elif output == "sigmoid":
                    self.loss = "mean_square"

                else:
                    raise Exception("Loss function not matched")

            else:
                self.loss = loss
            
        #set activation functions que
        
        if activation == "relu":
            
            for i in range(len(structure)-1):
                self.activations.append("relu")
                
        elif activation == "sigmoid":
            
            for i in range(len(structure)-1):
                self.activations.append("sigmoid")
                
        elif activation == "softmax":
            
            for i in range(len(structure)-1):
                self.activations.append("softmax")
                
        elif activation == "identity":
            
            for i in range(len(structure)-1):
                self.activations.append("identity")
                
        elif type(activation) == list or type(activation) == tuple:
            
            if len(activation) != len(structure)-1:
                raise Exception("invalid number of activation functions")
            
            for i in range(len(activation)):
                if activation[i] not in self.compat_activation_functions:
                    raise Exception("invalid actiavtion function name")
                    
            self.activations = activation
                
        else:
            raise Exception("invalid actiavtion function name")
        
        self.activations.append(self.output)
        
        
        #bias 초기값은 initializer 종류와 상관 없이 모두 -1~1사이 정규분포(표준편차=1)로 설정함
        
        if self.initializer == "uniform":
        
            for i in range(len(structure)):
                if i == 0:
                    self.w_layers.append(np.random.rand(input_shape[1], structure[0]))
                else:
                    self.w_layers.append(np.random.rand(structure[i-1], structure[i]))
                
            for i in range(len(structure)):
                #self.biases.append(np.random.rand(input_shape[0], structure[i]))
                self.b_layers.append(np.random.randn())
        
        elif self.initializer == "normal":
            
            for i in range(len(structure)):
                if i == 0:
                    self.w_layers.append(np.random.randn(input_shape[1], structure[0]))
                else:
                    self.w_layers.append(np.random.randn(structure[i-1], structure[i]))
                
            for i in range(len(structure)):
                #self.biases.append(np.random.randn(input_shape[0], structure[i]))
                self.b_layers.append(np.random.randn())
                
        elif self.initializer == "xabier" or (self.initializer == "auto" and activation == "sigmoid"):
            
            for i in range(len(structure)):
                if i == 0:
                    self.w_layers.append(np.random.randn(input_shape[1], structure[0]) / np.sqrt(input_shape[1]*structure[0]))
                else:
                    self.w_layers.append(np.random.randn(structure[i-1], structure[i]) / np.sqrt(structure[i-1]*structure[i]))
                
            for i in range(len(structure)):
                #self.biases.append(np.random.randn(input_shape[0], structure[i]))
                self.b_layers.append(np.random.randn())
                
            self.initializer = "xabier"
               
        elif self.initializer == "he" or (self.initializer == "auto" and activation == "relu"):
            
            for i in range(len(structure)):
                if i == 0:
                    self.w_layers.append(np.random.randn(input_shape[1], structure[0]) *np.sqrt(2/input_shape[1]))
                else:
                    self.w_layers.append(np.random.randn(structure[i-1], structure[i]) * np.sqrt(2/structure[i-1]))
                
            for i in range(len(structure)):
                #self.biases.append(np.random.randn(input_shape[0], structure[i]))
                self.b_layers.append(np.random.randn())
                
            self.initializer = "he"
            
        else:
            for i in range(len(structure)):
                if i == 0:
                    self.w_layers.append(np.random.randn(input_shape[1], structure[0]) / np.sqrt(input_shape[1]*structure[0]))
                else:
                    self.w_layers.append(np.random.randn(structure[i-1], structure[i]) / np.sqrt(structure[i-1]*structure[i]))
                
            for i in range(len(structure)):
                #self.biases.append(np.random.randn(input_shape[0], structure[i]))
                self.b_layers.append(np.random.randn())
                
            self.initializer = "xabier"
            print("Initializer set to 'xabier'")
        
        return
    
    def describe(self):
        
        print("Input Shape: " + str(self.input_shape))
        print("Network Sturcture: " + str(self.structure) + "\n")
        
        print("Actiavation: " + str(self.activations))
        print("Output Function: " + str(self.output))
        print("Loss Function: " + str(self.loss))
        print("Initializer: " + str(self.initializer) + "\n")
        
        for i in range(len(self.w_layers)):
            print("Layer " + str(i+1) + "\n")
            print(str(self.w_layers[i]) + "\n")
        
        print("Biases: \n")
        print(str(self.b_layers) + "\n")
        
        return
    
    def params(self):
        
        print("Activation functions: " + str(self.compat_activation_functions))
        print("Loss functions: " + str(self.compat_loss_functions))
        print("Initializers: " + str(self.compat_initializers) + "\n")
        
        return

    
    def forward(self, x, t, display=False):
        
        if np.asmatrix(x).shape[0] % self.input_shape[0] != 0:
            raise Exception("size of a mini-batch must be a multiple of specified input size of the model object")
        
        batch_size = int(np.asmatrix(x).shape[0]/self.input_shape[0])
        
        if display:
            print("batch_size: " + str(batch_size) +"\n")

        # prepare memory lists for backward propagation
                
        self.fan_ins = []
        self.fan_outs = []
        
        self.fan_ins.append(x)
        
        temp_x = x
        
        for i in range(len(self.w_layers)): #affine and activation
            
            temp_affined = self.affine_forward(temp_x, self.w_layers[i], self.b_layers[i])
            
            #batch normalization
            #if batch_normalization:
             #   temp_affined = 10
            
            self.fan_outs.append(temp_affined)
            
            if self.activations[i] == "sigmoid":
                temp_activated = self.sigmoid_forward(temp_affined)  # see here to check gradient loss!
                self.fan_ins.append(temp_activated)
                
                if display:
                    print("sigmoid forward " + str(temp_activated.shape))
                    
            elif self.activations[i] == "relu":
                temp_activated = self.relu_forward(temp_affined)  # see here to check gradient loss!
                self.fan_ins.append(temp_activated)
                
                if display:
                    print("relu forward " + str(temp_activated.shape))
                    
            elif self.activations[i] == "softmax":
                temp_activated = self.softmax_forward(temp_affined, batch_size)  # see here to check gradient loss!
                self.fan_ins.append(temp_activated)
                
                if display:
                    print("softmax forward " + str(temp_activated.shape))
                    
            elif self.activations[i] == "identity":
                temp_activated = self.identity_forward(temp_affined)  # see here to check gradient loss!
                self.fan_ins.append(temp_activated)
                
                if display:
                    print("identity forward " + str(temp_activated.shape))
                    
            else:
                raise Exception("Layer" + str(i+1) + ": " + "activation not successful")

            temp_x = temp_activated
            
            if display:
                print("Layer" + str(i+1) + ": " + "activated\n")
                            
        network_out = temp_activated
        
        #loss calculation
        
        if self.loss == "cross_entropy":
            error = self.cross_entropy_forward(network_out, t, batch_size)
            
        elif self.loss == "mean_square":
            error = self.mean_square_forward(network_out, t)
            
        else:
            raise Exception("Loss function not successfull")
        
        if display:
        
            print("Output: \n") 
            print(str(network_out) + "\n")

            print("Error: " + str(error))
            print("----------------------------------------\n")
        
        return network_out, error, batch_size
    
    
    def backward(self, y, t, batch_size, display = False):
        
        #prepare gradient lists
        
        self.w_gradients = []
        self.b_gradients = []
        
        #prepare memory lists
        
        activation_type_history = self.activations[::-1]
        
        affine_outputs_history = self.fan_outs[::-1]
        affine_inputs_history = self.fan_ins[::-1]
        
        layers_reversed = self.w_layers[::-1]
        
        #back propagate loss function, omit if it's softmax-cross entroy' combination
        if self.loss == "cross_entropy":
            if self.output == "softmax":
                if not self.strict:         
                    pass
                else:
                    propagation = self.cross_entropy_backward(y, t)
            else:
                propagation = self.cross_entropy_backward(y, t)
            
        elif self.loss == "mean_square":
            propagation = self.mean_square_backward(y, t)
        
        
        for i in range(len(self.w_layers)):
            
            if activation_type_history[i] == "sigmoid":
                propagation = self.sigmoid_backward(affine_outputs_history[i], affine_inputs_history[i], propagation)
                
                x_grad, layer_grad, b_grad = self.affine_backward(affine_inputs_history[i+1], layers_reversed[i], propagation) #the first element of'affine_inputs_history' is the final output of forward propagation and has been taken care of
                
                self.w_gradients.append(layer_grad)
                self.b_gradients.append(b_grad)
                
                propagation = x_grad
                
                if display:
                    print("sigmoid backward " + str(layer_grad.shape))
                
            elif activation_type_history[i] == "relu":
                propagation = self.relu_backward(affine_outputs_history[i], propagation)
                
                x_grad, layer_grad, b_grad = self.affine_backward(affine_inputs_history[i+1], layers_reversed[i], propagation) #the first element of'affine_inputs_history' is the final output of forward propagation and has been taken care of
                
                self.w_gradients.append(layer_grad)
                self.b_gradients.append(b_grad)
                
                propagation = x_grad
                                
                if display:
                    print("relu backward " + str(layer_grad.shape))
                    
            elif activation_type_history[i] == "softmax":
                
                if self.loss =="cross_entropy" and i==0:
                    if not self.strict:
                        propagation = y-t
                    else:
                        propagation = self.softmax_backward(affine_outputs_history[i], propagation, batch_size)
                else:
                    propagation = self.softmax_backward(affine_outputs_history[i], propagation, batch_size)
                
                x_grad, layer_grad, b_grad = self.affine_backward(affine_inputs_history[i+1], layers_reversed[i], propagation) #the first element of'affine_inputs_history' is the final output of forward propagation and has been taken care of
                
                self.w_gradients.append(layer_grad)
                self.b_gradients.append(b_grad)
                
                propagation = x_grad
                       
                if display:
                    print("softmax backward " + str(layer_grad.shape))
                    
            elif activation_type_history[i] == "identity":
                propagation = self.identity_backward(affine_outputs_history[i], propagation)
                
                x_grad, layer_grad, b_grad = self.affine_backward(affine_inputs_history[i+1], layers_reversed[i], propagation) #the first element of'affine_inputs_history' is the final output of forward propagation and has been taken care of
                
                self.w_gradients.append(layer_grad)
                self.b_gradients.append(b_grad)
                
                propagation = x_grad
                
                if display:
                    print("identity backward " + str(layer_grad.shape))
                    
            else:
                raise Exception("Gradient Propagation in Layer" + str(len(self.w_layers) - i) + " not successful")
        
            if display:
                    print("Layer" + str(len(self.w_layers) - i) + ": " + "propagated\n")
        
        self.w_gradients = self.w_gradients[::-1]
        self.b_gradients = self.b_gradients[::-1]
        
        if display:
                       
            for i in range(len(self.w_gradients)):
                print("Layer" + str(i+1) + " gradients: \n")
                print(str(self.w_gradients[i]) + "\n")
            
            print("Bias Gradients: \n")
            print(self.b_gradients)
            
        return self.w_gradients, self.b_gradients
        
        
    def predict(self, x):
        
        if np.asmatrix(x).shape[0] % self.input_shape[0] != 0:
            raise Exception("size of an input must be a multiple of specified input size of the model object")
        
        batch_size = int(np.asmatrix(x).shape[0]/self.input_shape[0])
        
        temp_x = x
        
        for i in range(len(self.w_layers)): #affine and activation
            
            temp_affined = self.affine_forward(temp_x, self.w_layers[i], self.b_layers[i])
            
            if self.activations[i] == "sigmoid":
                temp_activated = self.sigmoid_forward(temp_affined)  # see here to check gradient loss!
                
            elif self.activations[i] == "relu":
                temp_activated = self.relu_forward(temp_affined)  # see here to check gradient loss!
                
            elif self.activations[i] == "softmax":
                temp_activated = self.softmax_forward(temp_affined, batch_size)  # see here to check gradient loss!
                
            elif self.activations[i] == "identity":
                temp_activated = self.identity_forward(temp_affined)  # see here to check gradient loss!
                
            else:
                raise Exception("Layer" + str(i+1) + ": " + "activation not successful")

            temp_x = temp_activated
                            
        network_out = temp_activated
        
        return network_out
    
    
    def train(self, x, t, learning_rate, iteration, save_log=False, flush_log=True, display=True, error_round=10):
        
        print("mini batch process (learning rate: " + str(learning_rate) + ", iteration: " + str(iteration) + ")")
        
        if flush_log:
            self.error_log = []
        
        error_memory = []
        initial_five_passed = False
        
        start_time = time.time()
        
        for i in range(iteration):

            if save_log:
                out, error, batch_size= self.forward(x, t)
                self.backward(out, t, batch_size)
                self.error_log.append(error)
            else:
                out, error, batch_size = self.forward(x, t)
                self.backward(out, t, batch_size)
            
            #print(error)
            
            #print("round" +str(i) + " layer gradients: \n")
            #print(str(self.layer_gradients) +"\n")
            #print("round" +str(i) + " bias gradients: \n")
            #print(str(self.b_gradients) + "\n")
                  
            #update
            nparray_layers = np.array(self.w_layers, dtype=object)
            nparray_biases = np.array(self.b_layers)
            nparray_layer_gradients = np.array(self.w_gradients, dtype=object)
            nparray_b_gradients = np.array(self.b_gradients)
            
            self.w_layers = list(nparray_layers - nparray_layer_gradients*learning_rate)
            self.b_layers = list(nparray_biases - nparray_b_gradients*learning_rate)
            
            if i<5:
                error_memory.append(error)
            else:
                if i == 5:
                    initial_five_passed = True
                del error_memory[0]
                error_memory.append(error)
            
            if np.count_nonzero(nparray_layer_gradients[len(self.w_layers)-1] == 0) == np.size(nparray_layer_gradients[len(self.w_layers)-1]):
                print("Gradient Lost: last layer gradients equals to 0, i: " + str(i+1) + ", error: " + str(error))
                return
            elif initial_five_passed and error_memory[0] == error_memory[1] == error_memory[2] == error_memory[3] == error_memory[4]:
                print("Learning Effect Vanished, i: " + str(i+1) + ", error: " + str(error))
                return
            
            if display:
                if i < 0.5*iteration/10:
                    print("process                      0%  epoch: " + str(i+1)  + " error: " + str(round(error, error_round)), end="\r", flush=True)
                elif i < 1*iteration/10:
                    print("process =                    5%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 1.5*iteration/10:
                    print("process ==                   10%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 2*iteration/10:
                    print("process ===                  15%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 2.5*iteration/10:
                    print("process ====                 20%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 3*iteration/10:
                    print("process =====                25%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 3.5*iteration/10:
                    print("process ======               30%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 4*iteration/10:
                    print("process =======              35%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 4.5*iteration/10:
                    print("process ========             40%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 5*iteration/10:
                    print("process =========            45%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 5.5*iteration/10:
                    print("process ==========           50%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 6*iteration/10:
                    print("process ===========          55%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 6.5*iteration/10:
                    print("process ============         60%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 7*iteration/10:
                    print("process =============        65%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 7.5*iteration/10:
                    print("process ==============       70%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 8*iteration/10:
                    print("process ===============      75%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 8.5*iteration/10:
                    print("process ================     80%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 9*iteration/10:
                    print("process =================    85%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 9.5*iteration/10:
                    print("process ==================   90%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
                elif i < 10*iteration/10:
                    print("process ===================  95%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\r")
        
        if display:
            print("process ==================== 100%  epoch: " + str(i+1) + " error: " + str(round(error, error_round)), end="\n\n", flush=False)
        
        end_time = time.time()
        
        t = end_time - start_time
        h = int(round(t//3600, 0))
        m = int(round((t-(3600*h))//60, 0))
        s = int(round(t-(3600*h)-(60*m), 0))
        
        if display:
            print(str(h) + " hour " + str(m) + " min " +  str(s)+ " sec taken")
            
        return
    
    
    
    #활성화 함수 정의

    def sigmoid_forward(self, x):
        return 1/(1+np.exp(-x))
    
    def sigmoid_backward(self, ret_x, ret_y, propagation):
        #np.exp(-ret_x)*(ret_y**2)*propagation
        return ret_y*(1-ret_y)*propagation

    def relu_forward(self, x):
        return np.maximum(0, x)
    
    def relu_backward(self, ret_x, propagation):
        
        temp_grad = np.zeros(ret_x.shape, dtype=float)
        temp_grad[ret_x>0] = ret_x[ret_x>0]
                
        return temp_grad*propagation

    def softmax(self, x):
        return np.exp(x - np.max(x))/np.sum(np.exp(x - np.max(x)))
    
    def softmax_individual(self, x, i):   #when x is a flattened numpy array or matrix, returns the softmax value of x[i]
        
        if type(x) == np.ndarray:
            return np.exp(x[i] - np.max(x))/np.sum(np.exp(x - np.max(x)))
        
        elif type(x) == np.matrix:
            return np.exp(x[0, i] - np.max(x))/np.sum(np.exp(x - np.max(x)))
        
        else:
            raise Exception("unsupported argument type: takes numpy array or matrix")
    
    def softmax_forward(self, x, batch_size):
    
        temp_x =  copy.deepcopy(np.asmatrix(x.reshape(batch_size, -1)))  #batch 내의 각 input을 단위로 softmax를 수행하기 위해 reshape를 수행
        
        for i in range(len(temp_x)):
            temp_x[i] = self.softmax(temp_x[i])
        
        return np.asarray(temp_x.reshape(x.shape))   #원래 형상으로 복귀하여 전달
                            
    def softmax_backward(self, ret_x, propagation, batch_size):

        temp_x = np.asmatrix(ret_x.reshape(batch_size, -1))  #batch 내의 각 input을 단위로 softmax를 수행하기 위해 reshape를 수행
        temp_prop = propagation.reshape(batch_size, -1)

        temp_grads_batch = np.array([])
        for batch_index in range(len(temp_x)):

            temp_grads = np.array([])
            for i in range(temp_x[batch_index].shape[1]):

                temp_subgrads = np.array([])
                for j in range(temp_x[batch_index].shape[1]):
                    if i == j:
                        #derivative for the element in corresponding position
                        temp_subgrads = np.append(temp_subgrads, self.softmax_individual(temp_x[batch_index], i)*(1-self.softmax_individual(temp_x[batch_index], i)))
                    elif i!=j:
                        #derivatives for the rest
                        temp_subgrads = np.append(temp_subgrads, -self.softmax_individual(temp_x[batch_index], i)*self.softmax_individual(temp_x[batch_index], j))
                    else:
                        raise Exception()
                        
                temp_grads = np.append(temp_grads, np.sum(temp_subgrads*temp_prop[batch_index]))

            temp_grads_batch = np.append(temp_grads_batch, temp_grads)
            
        return temp_grads_batch.reshape(ret_x.shape)
                
            
    def identity_forward(self, x):
        return x
    
    def identity_backward(self, ret_x, propagation):
        return np.ones(ret_x.shape)*propagation


    #손실 함수 정의: y는 forward의 최종 output, t는 정답

    def mean_square_forward(self, y, t):
        return 0.5*np.sum((y-t)**2)

    def mean_square_backward(self, y, t):
        return y-t
    
    def cross_entropy(self, y, t):
        y[y==0] = y[y==0] + self.delta
        return -np.sum(t*np.log(y))
    
    def cross_entropy_forward(self, y, t, batch_size):   
        return self.cross_entropy(y, t)/batch_size
        
    def cross_entropy_backward(self, y, t):
        y[y==0] = y[y==0] + self.delta
        return -t/y

    
    #affine 연산 함수

    def affine_forward(self, x, w, b):  
        return np.dot(x, w) + b

    def affine_backward(self, ret_x, ret_w, propagation):
        
        x_gradient = np.asarray(np.dot(propagation, np.asmatrix(ret_w).T))
        w_gradient = np.asarray(np.dot(np.asmatrix(ret_x).T, propagation))
        b_gradient = np.sum(propagation)
    
        return x_gradient, w_gradient, b_gradient
    
    def batch_normalize_forward(self, x):
        
        temp_x = copy.deepcopy(x)
        
        mean = temp_x.mean()
        std = temp_x.std()
        
        temp_x = (temp_x - mean)/(std + self.delta)
        
        return temp_x
    
    def batch_normalize_backward(self, ret_x, propagation):
        
        
        
        
        return
    
    
    #util: export
    
    def export(self, directory=r".", file_name="model.json"):
        
        if not file_name.endswith(".json"):
            raise Exception("'file_name' must end with '.json'")
            return
        
        model_json = {}
        
        #essential export
        model_json["input_shape"] = self.input_shape
        model_json["structure"] = self.structure
        model_json["strict"] = self.strict
        model_json["initializer"] = self.initializer
        model_json["output"] = self.output
        model_json["loss"] = self.loss
        model_json["activations"] = self.activations
        model_json["delta"] = self.delta
        
        temp= []
        for i in range(len(self.structure)):
            temp.append(self.w_layers[i].tolist())
        
        model_json["w_layers"] = temp
        model_json["b_layers"] = self.b_layers
        
        #optional export
        
        try:
            model_json["error_log"] = self.error_log
            
        except Exception as e:
            pass
        
        try:
            temp=[]
            for i in range(len(self.structure)):
                temp.append(self.w_gradients[i].tolist())
            
            model_json["w_gradients"] = temp
            
        except Exception as e:
            pass
    
        try:
            temp=[]
            for i in range(len(self.structure)):
                temp.append(self.b_gradients[i].tolist())
            
            model_json["b_gradients"] = temp
            
        except Exception as e:
            pass
        
        try:
            temp=[]
            for i in range(len(self.structure)):
                temp.append(self.fan_ins[i].tolist())

            model_json["fan_ins"] = temp
            
        except Exception as e:
            pass
        
        try:
            temp=[]
            for i in range(len(self.structure)):
                temp.append(self.fan_outs[i].tolist())
            
            model_json["fan_outs"] = temp
            
        except Exception as e:
            pass
        
        #export as json file
        with open(directory + "/" + file_name, "w") as f:
            json.dump(model_json, f)
        
        print("model export successful: " + directory + "\\" + file_name)
        
        return

    #util: visualizer

    def vis_error_log(self):

        visualize_error_log(self.error_log)
        return

    def vis_inner_dist(self):

        visualize_fanio(self.fan_ins, self.fan_outs)
        return


#util: create a model from a json file

def make(file):
        
    with open(file, "r") as f:
        model_json = json.load(f)
        
    #create a default model
        
    model = ANN((1,1), (1, 1), "sigmoid")
        
    #essential imports
        
    model.input_shape = model_json["input_shape"]
    model.structure = model_json["structure"]
    model.strict = model_json["strict"]
    model.initializer = model_json["initializer"]
    model.output = model_json["output"]
    model.loss = model_json["loss"]
    model.activations = model_json["activations"]
    model.delta = model_json["delta"]
        
    temp = []
    for i in range(len(model.structure)):
        temp.append(np.array(model_json["w_layers"][i]))
        
    model.w_layers = temp
    model.b_layers = model_json["b_layers"]
        
        
    #optional import
        
    model.error_log = model_json["error_log"]
        
    try:
        temp = []
        for i in range(len(model.structure)):
            temp.append(np.array(model_json["w_gradients"][i]))
            
        model.w_gradients = temp
            
    except Exception as e:
        pass
        
    try:
        temp = []
        for i in range(len(model.structure)):
            temp.append(np.array(model_json["b_gradients"][i]))
            
        model.b_gradients = temp
            
    except Exception as e:
        pass
        
    try:
        temp = []
        for i in range(len(model.structure)):
            temp.append(np.array(model_json["fan_ins"][i]))
            
        model.fan_ins = temp
            
    except Exception as e:
        pass
        
    try:
        temp = []
        for i in range(len(model.structure)):
            temp.append(np.array(model_json["fan_outs"][i]))
            
        model.fan_outs = temp
            
    except Exception as e:
        pass
        
    return model


#util: visualizer

def visualize_error_log(error_log):

    mpl.rc('xtick', color = '#4A4A4A', labelsize = 12)
    mpl.rc('ytick', color = '#4A4A4A', labelsize = 12)
    mpl.rc('lines', linewidth = 1.5, markeredgewidth = 0)
    mpl.rc('axes', labelsize= 18, titlesize = 30, titlepad=40, labelpad = 17)
    mpl.rc('axes.spines', left=False, right=False, top=False, bottom = False)

    fig = plt.figure(figsize = (20, 10))
    plt.plot(error_log, color="#00ACCD")
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    plt.grid(True, color='#00ACCD', alpha=0.2, linestyle='--')

    plt.show()

    return
  
def visualize_fanio(fan_ins, fan_outs):

    mpl.rc('xtick', color = '#4A4A4A', labelsize = 12)
    mpl.rc('ytick', color = '#4A4A4A', labelsize = 12)
    mpl.rc('lines', linewidth = 1.5, markeredgewidth = 0)
    mpl.rc('axes', labelsize= 14, titlesize = 30, titlepad=40, labelpad = 17)
    mpl.rc('axes.spines', left=False, right=False, top=False, bottom = False)
    mpl.rc('figure', titlesize = 20, figsize = (20, 7))

    fig1, fi_axes = plt.subplots(1, len(fan_ins)-1)
    fig2, fo_axes = plt.subplots(1, len(fan_outs))

    fig1.suptitle("Actiavation Distributions")
    fig2.suptitle("Fan Out Distributions")

    for i in range(len(fan_outs)):

        fi_axes[i].hist(fan_ins[i+1].reshape(1, -1)[0], bins=20, color="#00ACCD")
        fi_axes[i].set_xlabel('Layer' + str(i+1))
        fi_axes[i].grid(True, color='#00ACCD', alpha=0.2, linestyle='--')

        fo_axes[i].hist(fan_outs[i].reshape(1, -1)[0], bins=20, color="#00ACCD")
        fo_axes[i].set_xlabel('Layer' + str(i+1))
        fo_axes[i].grid(True, color='#00ACCD', alpha=0.2, linestyle='--')
    
    plt.show()

    return