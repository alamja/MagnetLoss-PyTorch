import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch import optim

import torchvision
from torchvision.datasets import MNIST, CIFAR10
from torchvision import transforms

from datasets.fashion import FASHION

import numpy
from utils.sampler import SubsetSequentialSampler

def load_dataset(args):
	'''
		Loads the dataset specified
	'''

	# MNIST dataset
	if args.mnist:
		trans_img = transforms.Compose([
				transforms.ToTensor()
			])

		print("Downloading MNIST data...")
		trainset = MNIST('./data', train=True, transform=trans_img, download=True)
		testset = MNIST('./data', train=False, transform=trans_img, download=True)

	# CIFAR-10 dataset
	if args.cifar10:
		# Data
		print('==> Preparing data..')
		transform_train = transforms.Compose([
		    transforms.RandomCrop(32, padding=4),
		    transforms.RandomHorizontalFlip(),
		    transforms.ToTensor(),
		    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
		])

		transform_test = transforms.Compose([
		    transforms.ToTensor(),
		    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
		])

		trainset = CIFAR10(root='./data', train=True, transform=transform_train, download=True)
		testset = CIFAR10(root='./data', train=False, transform=transform_test, download=True)

	if args.fashionmnist:

		normalize = transforms.Normalize(mean=[x/255.0 for x in [125.3, 123.0, 113.9]],
                                     	 std=[x/255.0 for x in [63.0, 62.1, 66.7]])

		transform = transforms.Compose([transforms.ToTensor(),
		                                transforms.Normalize((0.1307,), (0.3081,))])

		trainset = FASHION(root='./data',
								train=True,
								transform=transform,
								download=True
								)

		testset = FASHION(root='./data',
							   train=False,
							   transform=transform,
							   download=True)

	# Deep Metric Learning
	if args.magnet_loss:
		n_train = len(trainset)
		train_sampler = SubsetSequentialSampler(range(len(trainset)), range(args.batch_size))
		trainloader = DataLoader(trainset,
								 batch_size=args.batch_size,
								 shuffle=False,
								 num_workers=1,
								 sampler=train_sampler)

		testloader = DataLoader(testset,
								batch_size=args.batch_size,
								shuffle=True,
								num_workers=1)
	# Random sampling
	else:
		n_train = len(trainset)
		trainloader = DataLoader(trainset,
								 batch_size=args.batch_size,
								 shuffle=True,
								 num_workers=4)

		testloader = DataLoader(testset,
								batch_size=args.batch_size,
								shuffle=True,
								num_workers=4)

	return trainloader, testloader, trainset, testset, n_train
