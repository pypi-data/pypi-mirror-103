from onnx_pytorch.code_gen_templates.temp_formatter import TempFormatter
from onnx_pytorch.code_trans import CodeTrans


class BatchNormalizationCodeTrans(CodeTrans):

  def __init__(self, schema):
    super(BatchNormalizationCodeTrans, self).__init__(schema)

  def get_torch_input_num(self):
    return 1

  def get_nn_name_str(self):
    return "\"BatchNorm{}d\".format(len(value_infos[node.input[0]].type.tensor_type.shape.dim) - 2)"

  def init_str(self):
    init_str = f'''
    \'\'\'self.{{node_name}} = nn.{{nn_name}}(**{{params}})
    self.{{node_name}}.weight.data = self.__variables[\"{{weight_name}}\"]
    if {{bias}}:
      self.{{node_name}}.bias.data = self.__variables[\"{{bias_name}}\"]
\'\'\'.format(
    nn_name={self.get_nn_name_str()},
    weight_name=node.input[1],
    bias_name="Undefined" if len(node.input) == 2 else node.input[2],
    node_name=node.name,
    bias=len(node.input) > 2,
    params=params_str,)'''
    return init_str

  def trans_input(self):
    pass

  def trans_attr(self):
    self.add_attr("epsilon", "eps")
    self.add_attr("momentum", "momentum")
    self.add_attr(
        "", "num_features",
        "{pytorch_attr}=onnx.numpy_helper.to_array(initializers[node.input[1]]).shape[0]"
    )
