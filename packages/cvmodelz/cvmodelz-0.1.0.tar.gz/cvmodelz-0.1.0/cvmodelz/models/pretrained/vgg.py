from chainer import links as L
from chainer.links.model.vision.vgg import prepare
from chainer.links.model.vision.vgg import _max_pooling_2d

from cvmodelz.models.meta_info import ModelInfo
from cvmodelz.models.pretrained.base import PretrainedModelMixin

def _vgg_meta(final_conv_layer):
	return ModelInfo(
		name="VGG",
		input_size=224,
		feature_size=4096,
		n_conv_maps=512,

		conv_map_layer=final_conv_layer,
		feature_layer="fc7",

		classifier_layers=["fc6", "fc7", "fc8"],
	)


class VGG19(PretrainedModelMixin, L.VGG19Layers):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, pooling=_max_pooling_2d, **kwargs)

	def init_model_info(self):
		self.meta = _vgg_meta("conv5_3")

	@property
	def functions(self):
		return super().functions

class VGG16(PretrainedModelMixin, L.VGG16Layers):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, pooling=_max_pooling_2d, **kwargs)

	def init_model_info(self):
		self.meta = _vgg_meta("conv5_4")

	@property
	def functions(self):
		return super().functions

