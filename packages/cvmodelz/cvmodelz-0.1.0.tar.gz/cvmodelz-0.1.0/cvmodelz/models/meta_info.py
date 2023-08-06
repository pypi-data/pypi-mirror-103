import pyaml

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ModelInfo(object):

	name:                       str         = "GenericModel"
	input_size:                 int         = 224
	feature_size:               int         = 2048
	n_conv_maps:                int         = 2048

	conv_map_layer:             str         = "conv"
	feature_layer:              str         = "fc"

	classifier_layers:          Tuple[str]  = ("fc",)

	def __str__(self):
		obj = dict(ModelInfo=self.__dict__)
		return pyaml.dump(obj, sort_dicts=False, )


if __name__ == '__main__':
	print(ModelInfo())
