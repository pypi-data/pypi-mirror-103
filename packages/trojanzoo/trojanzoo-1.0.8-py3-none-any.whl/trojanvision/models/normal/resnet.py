#!/usr/bin/env python3

from trojanvision.models.imagemodel import _ImageModel, ImageModel

import torch
import torch.nn as nn
import torchvision.models
from torchvision.models.resnet import model_urls as urls
from collections import OrderedDict
from collections.abc import Callable


class _ResNet(_ImageModel):

    def __init__(self, name: str = 'resnet18', **kwargs):
        super().__init__(**kwargs)
        module_list: list[nn.Module] = []
        if 's' in name.split('_'):
            from trojanvision.utils.model_archs.resnet_s import resnet_s
            _model = resnet_s(nclasses=self.num_classes)
            module_list.append(('conv1', _model.conv1))
            module_list.append(('bn1', _model.bn1))
            module_list.append(('relu', nn.ReLU(inplace=True)))
            self.classifier = nn.Sequential(OrderedDict([
                ('fc', _model.fc)
            ]))
        else:
            model_class = name.replace('_comp', '').replace('_s', '')
            ModelClass: Callable[..., torchvision.models.ResNet] = getattr(torchvision.models, model_class)
            _model = ModelClass(num_classes=self.num_classes)
            if 'comp' in name:
                conv1: nn.Conv2d = _model.conv1
                _model.conv1 = nn.Conv2d(conv1.in_channels, conv1.out_channels,
                                         kernel_size=3, stride=1, padding=1, bias=False)
                if 'resnext' in name:
                    _model.fc = nn.Linear(_model.fc.in_features // 2,
                                          _model.fc.out_features,
                                          bias=_model.fc.bias is None)
                module_list.append(('conv1', _model.conv1))
                module_list.append(('bn1', _model.bn1))
                module_list.append(('relu', _model.relu))
            else:
                module_list.append(('conv1', _model.conv1))
                module_list.append(('bn1', _model.bn1))
                module_list.append(('relu', _model.relu))
                module_list.append(('maxpool', _model.maxpool))
            self.pool = _model.avgpool  # nn.AdaptiveAvgPool2d((1, 1))
            self.classifier = nn.Sequential(OrderedDict([
                ('fc', _model.fc)  # nn.Linear(512 * block.expansion, num_classes)
            ]))
            # block.expansion = 1 if BasicBlock and 4 if Bottleneck
            # ResNet 18,34 use BasicBlock, 50 and higher use Bottleneck
        module_list.extend([('layer1', _model.layer1),
                            ('layer2', _model.layer2),
                            ('layer3', _model.layer3)])
        if not ('comp' in name and 'resnext' in name):
            module_list.append(('layer4', _model.layer4))
        self.features = nn.Sequential(OrderedDict(module_list))


class ResNet(ImageModel):
    available_models = ['resnet', 'resnet_comp', 'resnet_s',
                        'resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152',
                        'resnet18_comp', 'resnet34_comp', 'resnet50_comp', 'resnet101_comp', 'resnet152_comp',
                        'resnet18_s', 'resnet34_s', 'resnet50_s', 'resnet101_s', 'resnet152_s',
                        'resnext50_32x4d', 'resnext101_32x8d', 'wide_resnet50_2', 'wide_resnet101_2',
                        'resnext50_32x4d_comp', 'resnext101_32x8d_comp', 'wide_resnet50_2_comp', 'wide_resnet101_2_comp']

    model_urls = urls

    def __init__(self, name: str = 'resnet', layer: int = 18,
                 model: type[_ResNet] = _ResNet, **kwargs):
        super().__init__(name=name, layer=layer, model=model, **kwargs)

    def get_official_weights(self, **kwargs) -> OrderedDict[str, torch.Tensor]:
        _dict = super().get_official_weights(**kwargs)
        new_dict = OrderedDict()
        for i, (key, value) in enumerate(_dict.items()):
            prefix = 'features.' if i < len(_dict) - 2 else 'classifier.'
            new_dict[prefix + key] = value
        return new_dict

    @classmethod
    def get_name(cls, name: str, layer: int = None) -> str:
        prefix = ''
        if name.startswith('wide_'):
            prefix = 'wide_'
            name = name[5:]
        return prefix + super().get_name(name, layer=layer)
