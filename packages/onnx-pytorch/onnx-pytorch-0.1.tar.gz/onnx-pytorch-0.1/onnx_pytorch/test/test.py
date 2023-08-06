import onnx
import onnxruntime
import torch
from onnx.helper import make_node, make_tensor_value_info, make_graph, make_model, make_tensor
import numpy as np
from onnxruntime.tools.symbolic_shape_infer import SymbolicShapeInference

from onnx_pytorch import OnnxModel


def conv_flatten_relu():
  t1 = make_tensor("Conv_input_1", onnx.TensorProto.FLOAT, [32, 3, 3, 3],
                   np.random.randn(32, 3, 3, 3).astype(np.float32).flatten())
  t2 = make_tensor("Conv_input_2", onnx.TensorProto.FLOAT, [32],
                   np.random.randn(32).astype(np.float32).flatten())
  n = make_node(
      "Conv",
      ["Conv_input_{}".format(i) for i in range(3)],
      ["Conv_output_{}".format(i) for i in range(1)],
  )
  n1 = make_node(
      "Flatten",
      n.output,
      ["Flatten_output_{}".format(i) for i in range(1)],
  )
  n2 = make_node(
      "Relu",
      n1.output,
      ["Relu_output_{}".format(i) for i in range(1)],
  )
  input_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, [1, 3, 224, 224])
      for i in n.input[:1]
  ]
  output_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, None) for i in n2.output
  ]
  model = make_model(
      make_graph([n, n1, n2], "", input_vis, output_vis, initializer=[t1, t2]))

  sess_options = onnxruntime.SessionOptions()
  session = onnxruntime.InferenceSession(model.SerializeToString(),
                                         sess_options)
  inputs = {"Conv_input_0": np.random.randn(1, 3, 224, 224).astype(np.float32)}
  ort_outputs = session.run(None, inputs)
  print(ort_outputs)

  model.graph.ClearField("value_info")
  model = SymbolicShapeInference.infer_shapes(model, 2**31 - 1, True, True, 1)
  onnx.save(model, "conv_flatten_relu.onnx")


def conv_flatten_add_relu():
  t1 = make_tensor("Conv_input_1", onnx.TensorProto.FLOAT, [32, 3, 3, 3],
                   np.random.randn(32, 3, 3, 3).astype(np.float32).flatten())
  t2 = make_tensor("Conv_input_2", onnx.TensorProto.FLOAT, [32],
                   np.random.randn(32).astype(np.float32).flatten())
  t3 = make_tensor("Add_input_1", onnx.TensorProto.FLOAT, [1, 1577088],
                   np.random.randn(1577088).astype(np.float32).flatten())
  n = make_node(
      "Conv",
      ["Conv_input_{}".format(i) for i in range(3)],
      ["Conv_output_{}".format(i) for i in range(1)],
  )
  n1 = make_node(
      "Flatten",
      n.output,
      ["Flatten_output_{}".format(i) for i in range(1)],
  )
  n2 = make_node(
      "Add",
      list(n1.output) + [t3.name],
      ["Add_output_{}".format(i) for i in range(1)],
  )
  n3 = make_node(
      "Relu",
      n2.output,
      ["Relu_output_{}".format(i) for i in range(1)],
  )
  input_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, [1, 3, 224, 224])
      for i in n.input[:1]
  ]
  output_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, None) for i in n3.output
  ]
  model = make_model(
      make_graph([n, n1, n2, n3],
                 "",
                 input_vis,
                 output_vis,
                 initializer=[t1, t2, t3]))
  sess_options = onnxruntime.SessionOptions()
  session = onnxruntime.InferenceSession(model.SerializeToString(),
                                         sess_options)
  inputs = {"Conv_input_0": np.random.randn(1, 3, 224, 224).astype(np.float32)}
  ort_outputs = session.run(None, inputs)
  print(ort_outputs)

  model.graph.ClearField("value_info")
  model = SymbolicShapeInference.infer_shapes(model, 2**31 - 1, True, True, 1)
  onnx.save(model, "conv_flatten_add_relu.onnx")


def conv_maxpool_flatten_add_relu():
  t1 = make_tensor("Conv_input_1", onnx.TensorProto.FLOAT, [32, 3, 3, 3],
                   np.random.randn(32, 3, 3, 3).astype(np.float32).flatten())
  t2 = make_tensor("Conv_input_2", onnx.TensorProto.FLOAT, [32],
                   np.random.randn(32).astype(np.float32).flatten())
  t3 = make_tensor("Add_input_1", onnx.TensorProto.FLOAT, [1],
                   np.random.randn(1).astype(np.float32).flatten())
  n = make_node(
      "Conv",
      ["Conv_input_{}".format(i) for i in range(3)],
      ["Conv_output_{}".format(i) for i in range(1)],
  )
  n1 = make_node(
      "MaxPool",
      n.output,
      ["MaxPool_output_{}".format(i) for i in range(1)],
      kernel_shape=(3, 3),
      strides=(2, 2),
      pads=(0, 0, 1, 1),
  )
  n2 = make_node(
      "Flatten",
      n1.output,
      ["Flatten_output_{}".format(i) for i in range(1)],
  )
  n3 = make_node(
      "Add",
      list(n2.output) + [t3.name],
      ["Add_output_{}".format(i) for i in range(1)],
  )
  n4 = make_node(
      "Relu",
      n3.output,
      ["Relu_output_{}".format(i) for i in range(1)],
  )
  input_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, [1, 3, 224, 224])
      for i in n.input[:1]
  ]
  output_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, None) for i in n4.output
  ]
  model = make_model(
      make_graph([n, n1, n2, n3, n4],
                 "",
                 input_vis,
                 output_vis,
                 initializer=[t1, t2, t3]))
  sess_options = onnxruntime.SessionOptions()
  session = onnxruntime.InferenceSession(model.SerializeToString(),
                                         sess_options)
  inputs = {"Conv_input_0": np.random.randn(1, 3, 224, 224).astype(np.float32)}
  ort_outputs = session.run(None, inputs)
  print(ort_outputs)

  model.graph.ClearField("value_info")
  model = SymbolicShapeInference.infer_shapes(model, 2**31 - 1, True, True, 1)
  onnx.save(model, "conv_maxpool_flatten_add_relu.onnx")


def conv_maxpool_globalavgpool_flatten_add_relu():
  t1 = make_tensor("Conv_input_1", onnx.TensorProto.FLOAT, [32, 3, 3, 3],
                   np.random.randn(32, 3, 3, 3).astype(np.float32).flatten())
  t2 = make_tensor("Conv_input_2", onnx.TensorProto.FLOAT, [32],
                   np.random.randn(32).astype(np.float32).flatten())
  t3 = make_tensor("Add_input_1", onnx.TensorProto.FLOAT, [1],
                   np.random.randn(1).astype(np.float32).flatten())
  n = make_node(
      "Conv",
      ["Conv_input_{}".format(i) for i in range(3)],
      ["Conv_output_{}".format(i) for i in range(1)],
  )
  n1 = make_node(
      "MaxPool",
      n.output,
      ["MaxPool_output_{}".format(i) for i in range(1)],
      kernel_shape=(3, 3),
      strides=(2, 2),
      pads=(0, 0, 1, 1),
  )
  n2 = make_node(
      "GlobalAveragePool",
      n1.output,
      ["GlobalAveragePool_output_{}".format(i) for i in range(1)],
  )
  n3 = make_node(
      "Flatten",
      n2.output,
      ["Flatten_output_{}".format(i) for i in range(1)],
  )
  n4 = make_node(
      "Add",
      list(n3.output) + [t3.name],
      ["Add_output_{}".format(i) for i in range(1)],
  )
  n5 = make_node(
      "Relu",
      n4.output,
      ["Relu_output_{}".format(i) for i in range(1)],
  )
  input_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, [1, 3, 224, 224])
      for i in n.input[:1]
  ]
  output_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, None) for i in n5.output
  ]
  model = make_model(
      make_graph([n, n1, n2, n3, n4, n5],
                 "",
                 input_vis,
                 output_vis,
                 initializer=[t1, t2, t3]))
  sess_options = onnxruntime.SessionOptions()
  session = onnxruntime.InferenceSession(model.SerializeToString(),
                                         sess_options)
  inputs = {"Conv_input_0": np.random.randn(1, 3, 224, 224).astype(np.float32)}
  ort_outputs = session.run(None, inputs)
  print(ort_outputs)

  model.graph.ClearField("value_info")
  model = SymbolicShapeInference.infer_shapes(model, 2**31 - 1, True, True, 1)
  onnx.save(model, "conv_maxpool_globalavgpool_flatten_add_relu.onnx")


def conv_batchnorm_maxpool_globalavgpool_flatten_add_relu():
  t1 = make_tensor("Conv_input_1", onnx.TensorProto.FLOAT, [32, 3, 3, 3],
                   np.random.randn(32, 3, 3, 3).astype(np.float32).flatten())
  t2 = make_tensor("Conv_input_2", onnx.TensorProto.FLOAT, [32],
                   np.random.randn(32).astype(np.float32).flatten())
  t3 = make_tensor("Add_input_1", onnx.TensorProto.FLOAT, [1],
                   np.random.randn(1).astype(np.float32).flatten())
  t4 = make_tensor("BatchNormalization_input_0", onnx.TensorProto.FLOAT, [32],
                   np.ones(32).astype(np.float32).flatten())
  t5 = make_tensor("BatchNormalization_input_1", onnx.TensorProto.FLOAT, [32],
                   np.zeros(32).astype(np.float32).flatten())
  t6 = make_tensor("BatchNormalization_input_2", onnx.TensorProto.FLOAT, [32],
                   np.random.randn(32).astype(np.float32).flatten())
  t7 = make_tensor("BatchNormalization_input_3", onnx.TensorProto.FLOAT, [32],
                   np.random.randn(32).astype(np.float32).flatten())
  n = make_node(
      "Conv",
      ["Conv_input_{}".format(i) for i in range(3)],
      ["Conv_output_{}".format(i) for i in range(1)],
  )
  n1 = make_node(
      "BatchNormalization",
      list(n.output) + [t4.name, t5.name, t6.name, t7.name],
      ["BatchNormalization_output_{}".format(i) for i in range(1)],
  )
  n2 = make_node(
      "MaxPool",
      n1.output,
      ["MaxPool_output_{}".format(i) for i in range(1)],
      kernel_shape=(3, 3),
      strides=(2, 2),
      pads=(0, 0, 1, 1),
  )
  n3 = make_node(
      "GlobalAveragePool",
      n2.output,
      ["GlobalAveragePool_output_{}".format(i) for i in range(1)],
  )
  n4 = make_node(
      "Flatten",
      n3.output,
      ["Flatten_output_{}".format(i) for i in range(1)],
  )
  n5 = make_node(
      "Add",
      list(n4.output) + [t3.name],
      ["Add_output_{}".format(i) for i in range(1)],
  )
  n6 = make_node(
      "Relu",
      n5.output,
      ["Relu_output_{}".format(i) for i in range(1)],
  )
  input_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, [1, 3, 224, 224])
      for i in n.input[:1]
  ]
  output_vis = [
      make_tensor_value_info(i, onnx.TensorProto.FLOAT, None) for i in n6.output
  ]
  model = make_model(
      make_graph([n, n1, n2, n3, n4, n5, n6],
                 "",
                 input_vis,
                 output_vis,
                 initializer=[t1, t2, t3, t4, t5, t6, t7]))
  sess_options = onnxruntime.SessionOptions()
  session = onnxruntime.InferenceSession(model.SerializeToString(),
                                         sess_options)
  inputs = {"Conv_input_0": np.random.randn(1, 3, 224, 224).astype(np.float32)}
  ort_outputs = session.run(None, inputs)
  print(ort_outputs)

  model.graph.ClearField("value_info")
  model = SymbolicShapeInference.infer_shapes(model, 2**31 - 1, True, True, 1)
  onnx.save(model, "conv_batchnorm_maxpool_globalavgpool_flatten_add_relu.onnx")


def resnet_18():
  model = onnx.load("ort_train_resnet18.onnx")
  model.graph.ClearField("value_info")
  for n in model.graph.node:
    inputs, outputs = [], []
    for i in n.input:
      if i.isnumeric():
        inputs.append(i)
      else:
        i.replace(".", "_")
        inputs.append(i)
    for i in n.output:
      if i.isnumeric():
        outputs.append(i)
      else:
        i.replace(".", "_")
        outputs.append(i)

    n.ClearField("input")
    n.input.extend(inputs)
    n.ClearField("output")
    n.output.extend(outputs)

  for i in model.graph.input:
    if i.name.isnumeric():
      i.name = "__t_{}".format(i.name)
    else:
      i.name = i.name.replace(".", "_")
  for i in model.graph.output:
    if i.name.isnumeric():
      i.name = "__t_{}".format(i.name)
    else:
      i.name = i.name.replace(".", "_")

    for i in model.graph.initializer:
      if i.name.isnumeric():
        i.name = "__t_{}".format(i.name)
      else:
        i.name = i.name.replace(".", "_")
  onnx.save(model, "ort_train_resnet18.onnx")
  model = SymbolicShapeInference.infer_shapes(model, 2**31 - 1, True, True, 1)

  onnx.save(model, "ort_train_resnet18.onnx")


if __name__ == '__main__':
  resnet_18()
