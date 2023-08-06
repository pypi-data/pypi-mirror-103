import glob
import inspect
import os
import torch.nn as nn

from onnx_pytorch.code_gen_templates.temp_formatter import TempFormatter

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [
    os.path.basename(f)[:-3]
    for f in modules
    if os.path.isfile(f) and not f.endswith('__init__.py')
] + ["get_op_trans"]

nn_dict = {
    nn_name.lower(): getattr(nn, nn_name)
    for nn_name in dir(nn)
    if nn_name[0].isupper()
}

nn_name_dict = {
    nn_name.lower(): nn_name for nn_name in dir(nn) if nn_name[0].isupper()
}


class CodeTrans:

  def __init__(self, schema=None):
    self.mapped_attrs = set()
    self.schema = schema

  def get_torch_input_num(self):
    curr_nn = nn_dict.get(self.schema.name.lower())
    if not curr_nn:
      return 1
    return len(inspect.getfullargspec(curr_nn.forward).args) - 1

  def get_nn_name_str(self):
    if not self.schema:
      return "Undefined"
    if self.schema.name.lower() in nn_name_dict:
      return "\"{}\"".format(nn_name_dict[self.schema.name.lower()])
    return "\"{}\"".format(
        nn_name_dict.get(self.schema.name.lower(), self.schema.name.lower()))

  def init_str(self):
    return TempFormatter.init_str(self.get_nn_name_str())

  def forward_str(self):
    return TempFormatter.forward_str()

  def additional_str(self):
    return ""

  def trans_input(self):
    pass

  def trans_attr(self):
    pass

  def add_attr(self, onnx_attr, pytorch_attr, trans=None):
    if trans is None:
      trans = TempFormatter.default_attr_trans(pytorch_attr=pytorch_attr,
                                               onnx_attr=onnx_attr)
    self.mapped_attrs.add((onnx_attr, pytorch_attr,
                           trans.format(onnx_attr=onnx_attr,
                                        pytorch_attr=pytorch_attr)))


def get_op_trans(op=None):
  mod = globals().get(op, None)
  if mod is None:
    return CodeTrans
  return getattr(mod, "{}CodeTrans".format(op))
