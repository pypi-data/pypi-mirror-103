import collections
import inspect
import dis
import itertools
import os
import shutil
import sys

import onnx_pytorch
import numpy as np
import onnx
from onnx import defs, TensorProto
import onnxruntime
import torch
import torch.nn as nn
from onnx.helper import make_node, make_empty_tensor_value_info, make_graph, make_model, make_tensor_value_info
from onnx.numpy_helper import to_array

from onnx_pytorch.code_gen_templates.temp_formatter import TempFormatter
from onnx_pytorch.code_trans import *

torch.set_printoptions(6)

MATH_OP = {
    "LessOrEqual": "<=",
}

nn_dict = {
    nn_name.lower(): getattr(nn, nn_name)
    for nn_name in dir(nn)
    if nn_name[0].isupper()
}

nn_name_dict = {
    nn_name.lower(): nn_name for nn_name in dir(nn) if nn_name[0].isupper()
}

ignore_torch_attr = {"inplace"}
ignore_onnx_attr = {}


def try_run_ort(schema, attrs={}, inputs={}):
  n = make_node(schema.name,
                ["input_{}".format(i) for i in range(schema.max_input)],
                ["output_{}".format(i) for i in range(schema.max_output)],
                **attrs)
  input_vis = [
      make_tensor_value_info(i, TensorProto.FLOAT, None) for i in n.input
  ]
  output_vis = [
      make_tensor_value_info(i, TensorProto.FLOAT, None) for i in n.output
  ]
  model = make_model(make_graph([n], "", input_vis, output_vis))
  sess_options = onnxruntime.SessionOptions()
  session = onnxruntime.InferenceSession(model.SerializeToString(),
                                         sess_options)
  ort_outputs = session.run(None, inputs)
  return ort_outputs


def try_run_torch(schema, attrs={}, inputs=[]):
  nn_instance = nn_dict[schema.name.lower()](**attrs)
  return nn_instance(*[torch.from_numpy(i) for i in inputs])


def try_mapping_args_WIP(schema):
  if schema.name.lower() not in nn_dict:
    return None
  curr_nn = nn_dict[schema.name.lower()]
  full_arg_spec = inspect.getfullargspec(curr_nn.__init__)
  args = full_arg_spec.args[1:]
  args_perm = collections.OrderedDict()
  for a in args:
    if a in ignore_torch_attr:
      continue
    anno = full_arg_spec.annotations[a]
    if anno is bool:
      args_perm[a] = (True, False)
    elif anno is int:
      args_perm[a] = (1, 2, 4)
  torch_attr_pool = list(itertools.product(args_perm.values()))
  print(torch_attr_pool)

  ort_inputs = collections.OrderedDict()
  for idx, i in enumerate(schema.inputs):
    ort_inputs["input_{}".format(idx)] = np.random.randn(1,
                                                         10).astype(np.float32)

  print(schema.attributes)

  if full_arg_spec.defaults:
    # ort_outputs = try_run_ort(schema, attrs={}, inputs=ort_inputs)
    torch_attr_default = {a: d for a, d in zip(args, full_arg_spec.defaults)}
    torch_output = try_run_torch(schema,
                                 attrs=torch_attr_default,
                                 inputs=list(ort_inputs.values()))
  elif not torch_attr_pool:
    ort_outputs = try_run_ort(schema, attrs={}, inputs=ort_inputs)
    torch_output = try_run_torch(schema,
                                 attrs={},
                                 inputs=list(ort_inputs.values()))
    assert np.allclose(ort_outputs, torch_output)
    print(torch_output)


def gen_code_gen():
  shutil.rmtree(os.path.join(os.path.dirname(__file__), "op_code_generators"))
  os.mkdir(os.path.join(os.path.dirname(__file__), "op_code_generators"))
  with open(
      os.path.join(os.path.dirname(__file__), "op_code_generators", "__init__.py"),
      "w") as f:
    f.write(TempFormatter.code_generator())
  for schema in defs.get_all_schemas():
    if schema.domain in ("ai.onnx.preview.training", "ai.onnx.ml"):
      continue
    if schema.name not in ("Conv", "Relu", "Gemm", "Add", "Flatten",
                           "GlobalAveragePool", "MaxPool",
                           "BatchNormalization"):
      continue
    trans_cls = get_op_trans(schema.name)
    if trans_cls is not None:
      trans_cls_ins = trans_cls(schema)
    else:
      trans_cls = get_op_trans()
      trans_cls_ins = trans_cls()
    trans_cls_ins.trans_attr()
    mapped_attrs = trans_cls_ins.mapped_attrs
    attr_default = "{{{attr_default_contents}}}"
    attr_default_contents = []
    for a, i in schema.attributes.items():
      try:
        default_value = onnx.helper.get_attribute_value(i.default_value)
        attr_default_contents.append("\"{key}\": {value}".format(
            key=a, value=default_value))
      except:
        continue
    attr_default_str = attr_default.format(
        attr_default_contents=", ".join(attr_default_contents))

    params_content = ""
    format_contents = []
    if mapped_attrs:
      for onnx_attr, pytorch_attr, trans in mapped_attrs:
        format_contents.append(trans)
        params_content += TempFormatter.single_attr(pytorch_attr=pytorch_attr)
    params_str = f'"{{{{{params_content}}}}}"'
    params_str += TempFormatter.format(format_str=", ".join(format_contents))
    gened_op_code_generator = TempFormatter.op_code_generator(
        attr_default_str=attr_default_str,
        op=schema.name,
        onnx_ver=schema.since_version,
        torch_ver=torch.__version__,
        input_num=trans_cls_ins.get_torch_input_num(),
        params_str=params_str,
        init_str=trans_cls_ins.init_str(),
        forward_str=trans_cls_ins.forward_str(),
        additional_str=trans_cls_ins.additional_str(),
    )

    with open(
        os.path.join(os.path.dirname(__file__), "op_code_generators",
                     "{}.py".format(schema.name)), "w") as f:
      f.write(gened_op_code_generator)
    pass
  pass


def gen_code():
  # shutil.rmtree(os.path.join(os.path.dirname(__file__), "op_code_generators"))
  # os.mkdir(os.path.join(os.path.dirname(__file__), "op_code_generators"))
  with open(
      os.path.join(os.path.dirname(__file__), "op_code_generators", "__init__.py"),
      "w") as f:
    f.write(TempFormatter.code_generator())
  # for schema in defs.get_all_schemas():
  #   if schema.domain in ("ai.onnx.preview.training", "ai.onnx.ml"):
  #     continue
  #   if schema.name not in ("Conv", "Relu", "Gemm", "Add", "Flatten",
  #                          "GlobalAveragePool", "MaxPool",
  #                          "BatchNormalization"):
  #     continue
  #   trans_cls = get_op_trans(schema.name)
  #   if trans_cls is not None:
  #     trans_cls_ins = trans_cls(schema)
  #   else:
  #     trans_cls = get_op_trans()
  #     trans_cls_ins = trans_cls()
  #   trans_cls_ins.trans_attr()
  #   mapped_attrs = trans_cls_ins.mapped_attrs
  #   attr_default = "{{{attr_default_contents}}}"
  #   attr_default_contents = []
  #   for a, i in schema.attributes.items():
  #     try:
  #       default_value = onnx.helper.get_attribute_value(i.default_value)
  #       attr_default_contents.append("\"{key}\": {value}".format(
  #         key=a, value=default_value))
  #     except:
  #       continue
  #   attr_default_str = attr_default.format(
  #     attr_default_contents=", ".join(attr_default_contents))
  #
  #   params_content = ""
  #   format_contents = []
  #   if mapped_attrs:
  #     for onnx_attr, pytorch_attr, trans in mapped_attrs:
  #       format_contents.append(trans)
  #       params_content += TempFormatter.single_attr(pytorch_attr=pytorch_attr)
  #   params_str = f'"{{{{{params_content}}}}}"'
  #   params_str += TempFormatter.format(format_str=", ".join(format_contents))
  #   gened_op_code_generator = TempFormatter.op_code_generator(
  #     attr_default_str=attr_default_str,
  #     op=schema.name,
  #     onnx_ver=schema.since_version,
  #     torch_ver=torch.__version__,
  #     input_num=trans_cls_ins.get_torch_input_num(),
  #     params_str=params_str,
  #     init_str=trans_cls_ins.init_str(),
  #     forward_str=trans_cls_ins.forward_str(),
  #     additional_str=trans_cls_ins.additional_str(),
  #   )
  #
  #   with open(
  #       os.path.join(os.path.dirname(__file__), "op_code_generators",
  #                    "{}.py".format(schema.name)), "w") as f:
  #     f.write(gened_op_code_generator)
  #   pass
  pass

gen_code()