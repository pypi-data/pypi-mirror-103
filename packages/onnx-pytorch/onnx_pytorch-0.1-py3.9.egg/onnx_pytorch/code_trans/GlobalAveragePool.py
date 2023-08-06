from onnx_pytorch.code_gen_templates.temp_formatter import TempFormatter
from onnx_pytorch.code_trans import CodeTrans


class GlobalAveragePoolCodeTrans(CodeTrans):

  def __init__(self, schema):
    super(GlobalAveragePoolCodeTrans, self).__init__(schema)

  def get_nn_name_str(self):
    return "\"functional.avg_pool{}d\".format(len(value_infos[node.input[0]].type.tensor_type.shape.dim) - 2)"

  def init_str(self):
    return f'''"self.{{node_name}} = nn.{{nn_name}}".format(
    nn_name={self.get_nn_name_str()},
    node_name=node.name,)'''

  def trans_attr(self):
    self.add_attr(
        "", "kernel_size",
        "{pytorch_attr}=\"self.{{}}.shape[{{}}:]\".format(node.input[0], (len(value_infos[node.input[0]].type.tensor_type.shape.dim) - 2))"
    )

  def forward_str(self):
    return TempFormatter.forward_str_functional()
