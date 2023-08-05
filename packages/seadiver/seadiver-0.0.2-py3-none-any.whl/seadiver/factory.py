#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import toynn.model as mdl

def make(file):
        
    with open(file, "r") as f:
        model_json = json.load(f)
        
    #create a default model
        
    model = mdl.ANN((1,1), (1, 1), "sigmoid")
        
    #essential imports
        
    model.input_size = model_json["input_shape"]
    model.shape = model_json["network_structure"]
    model.strict = model_json["strict"]
    model.initializer = model_json["initializer"]
    model.output = model_json["output"]
    model.loss = model_json["loss"]
    model.activation = model_json["activation"]
    model.delta = model_json["delta"]
        
    temp = []
    for i in range(len(model.shape)):
        temp.append(np.array(model_json["w_layers"][i]))
        
    model.layers = temp
    model.biases = model_json["b_layers"]
        
        
    #optional import
        
    model.error_log = model_json["error_log"]
        
    try:
        temp = []
        for i in range(len(model.shape)):
            temp.append(np.array(model_json["w_gradients"][i]))
            
        model.layer_gradients = temp
            
    except Exception as e:
        pass
        
    try:
        temp = []
        for i in range(len(model.shape)):
            temp.append(np.array(model_json["b_gradients"][i]))
            
        model.b_gradients = temp
            
    except Exception as e:
        pass
        
    try:
        temp = []
        for i in range(len(model.shape)):
            temp.append(np.array(model_json["affine_inputs"][i]))
            
        model.affine_inputs = temp
            
    except Exception as e:
        pass
        
    try:
        temp = []
        for i in range(len(model.shape)):
            temp.append(np.array(model_json["affine_outputs"][i]))
            
        model.affine_outputs = temp
            
    except Exception as e:
        pass
        
    return model

