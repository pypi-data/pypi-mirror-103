from onnx_pytorch.code_gen_templates.temp_formatter import TempFormatter
from onnx_pytorch.code_trans import CodeTrans


class GemmCodeTrans(CodeTrans):

  def __init__(self, schema):
    super(GemmCodeTrans, self).__init__(schema)

  def get_torch_input_num(self):
    return 1

  def get_nn_name_str(self):
    return "\"Conv{}d\".format(len(value_infos[node.input[0]].type.tensor_type.shape.dim) - 2)"

  def init_str(self):
    return "\"\""

  def trans_input(self):
    pass

  def forward_str(self):
    return '''\'\'\'
    torch.matmul({{inputs_str}}, {{outputs_str}})
    \'\'\'.format(        
            inputs_str=", ".join(inputs_str),
            outputs_str=", ".join(outputs_str),)'''

  def additional_str(self):
    return '''
    inputs_str[0] = "torch.transpose({}, 0, 1)".format(inputs_str[0]) if attr_value_dict["transA"] == 1 else inputs_str[0]
    inputs_str[1] = "torch.transpose({}, 0, 1)".format(inputs_str[1]) if attr_value_dict["transB"] == 1 else inputs_str[1]
'''