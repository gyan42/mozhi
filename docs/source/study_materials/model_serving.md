# Model Serving

## Tensorflow Model Serving

### Saving and Loading Models

The phrase "Saving a TensorFlow model" typically means one of two things:

- **[CheckPoints](https://www.tensorflow.org/guide/checkpoint)**
- **[SavedModel](https://www.tensorflow.org/guide/saved_model)**
    - **[Keras Model](https://www.tensorflow.org/api_docs/python/tf/keras/models/save_model)**
    
Checkpoints capture the exact value of all parameters (tf.Variable objects) used by a model. Checkpoints do not contain 
any description of the computation defined by the model and thus are typically only useful when source code that will 
use the saved parameter values is available.

The SavedModel format on the other hand includes a serialized description of the computation defined by the model in 
addition to the parameter values (checkpoint). Models in this format are independent of the source code that created 
the model. They are thus suitable for deployment via TensorFlow Serving, TensorFlow Lite, TensorFlow.js, or programs 
in other programming languages (the C, C++, Java, Go, Rust, C# etc. TensorFlow APIs).

### Serving Models
- **[Tensorflow Serving](https://www.tensorflow.org/tfx/guide/serving)**


-----------------------------------------------------------------------

## PyTorch Serve

TODO: https://towardsdatascience.com/pytorch-jit-and-torchscript-c2a77bac0fff

PyTorch supports 2 separate modes to handle research and production environment.
- First is the **Eager mode**. It is built for faster prototyping, training, and experimentation.
- Second is the **Script mode**. It is focused on the production use case. It has 2 components **PyTorch JIT** and **TorchScript**.

Why do we need Script mode?

In one line, it gets rids of Python’s GIL and dependence on Python runtime. A nuanced explanation is as follows

**Portability**
Portability allows models to be deployed in multithreaded inference servers, mobiles, and cars which is difficult with Python. 
In order to achieve this PyTorch models needs to be decoupled from any specific runtime.

**Performance**
PyTorch JIT is an optimizing JIT compiler for PyTorch. It uses runtime information to optimize TorchScript modules. 
It can automate optimizations like layer fusion, quantization, sparsification.

### [Pytorch](https://pytorch.org/blog/model-serving-in-pyorch/) 
There are three ways to export a PyTorch Lightning model for serving:

- Saving the model as a PyTorch checkpoint (*.ckpt)
- Converting the model to ONNX
- Exporting the model to Torchscript 

### Serving Models

- **[TorchServe](https://github.com/pytorch/serve/blob/master/README.md#torchserve)**
- https://blog.ceshine.net/post/torchserve/
- https://towardsdatascience.com/deploy-models-and-create-custom-handlers-in-torchserve-fc2d048fbe91
- https://medium.com/analytics-vidhya/deploying-named-entity-recognition-model-to-production-using-torchserve-fd8cf5cff02f

