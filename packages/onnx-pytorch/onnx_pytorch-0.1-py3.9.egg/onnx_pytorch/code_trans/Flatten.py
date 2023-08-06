from onnx_pytorch.code_trans import CodeTrans


class FlattenCodeTrans(CodeTrans):

  def __init__(self, schema):
    super(FlattenCodeTrans, self).__init__(schema)

  def trans_attr(self):
    self.add_attr("axis", "start_dim")
