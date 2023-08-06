from onnx_pytorch.code_gen_templates.temp_formatter import TempFormatter
from onnx_pytorch.code_trans import CodeTrans


class MaxPoolCodeTrans(CodeTrans):

  def __init__(self, schema):
    super(MaxPoolCodeTrans, self).__init__(schema)

  def get_nn_name_str(self):
    return "\"MaxPool{}d\".format(len(value_infos[node.input[0]].type.tensor_type.shape.dim) - 2)"

  def trans_attr(self):
    trans = '{{pytorch_attr}}=attr_value_dict[\"{{onnx_attr}}\"]'
    self.add_attr(
        "dilations", "dilation",
        (trans +
         '[:].__repr__() if \"{curr_attr}\" in attr_value_dict else 1').format(
             curr_attr="dilations"))
    self.add_attr(
        "strides", "stride",
        (trans +
         '[:].__repr__() if \"{curr_attr}\" in attr_value_dict else 1').format(
             curr_attr="strides"))
    self.add_attr("kernel_shape", "kernel_size",
                  (trans + '[:].__repr__()').format(curr_attr="kernel_shape"))
    self.add_attr(
        "pads", "padding",
        (trans +
         '[2:].__repr__() if \"{curr_attr}\" in attr_value_dict else 0').format(
             curr_attr="pads"))
    self.add_attr("ceil_mode", "ceil_mode",
                  "{pytorch_attr}=bool(attr_value_dict[\"ceil_mode\"])")
    self.add_attr("", "return_indices",
                  "{pytorch_attr}=(len(node.output) == 2)")
