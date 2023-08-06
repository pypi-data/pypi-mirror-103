import onnx
import onnx.helper

def add_conv(graph):
  last_node = graph.node[-1]
