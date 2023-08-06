from onnx_pytorch.code_trans import CodeTrans


class AddCodeTrans(CodeTrans):

  def __init__(self, schema):
    super(AddCodeTrans, self).__init__(schema)

  def init_str(self):
    return "\"\""

  def forward_str(self):
    return f'''\'\'\'{{outputs_str}} = {{inputs_str}}\'\'\'.format(
            node_name=node.name,
            inputs_str=" + ".join(inputs_str),
            outputs_str=", ".join(outputs_str),)'''

  def additional_str(self):
    return '''inputs_str = ["self.{}".format(i) if i not in initializers else "self.__variables[\\"{}\\"]".format(i) for i in node.input]'''
