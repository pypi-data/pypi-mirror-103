# Factorization Machine models in PyTorch
  
This package provides a PyTorch implementation of Deep Factorization Machine ;odels and common datasets in Retail Recommendation.


## Available Datasets

* [Retail Case Study Data](https://www.kaggle.com/darpan25bajaj/retail-case-study-data/download)


## Available Models

| Model | Reference |
|-------|-----------|
| DeepFM | [H Guo, et al. DeepFM: A Factorization-Machine based Neural Network for CTR Prediction, 2017.](https://arxiv.org/abs/1703.04247) |
| xDeepFM | [J Lian, et al. xDeepFM: Combining Explicit and Implicit Feature Interactions for Recommender Systems, 2018.](https://arxiv.org/abs/1803.05170) |


## Environment

    
    conda env create -f environment_conda.yml
    source activate environment_conda
    

## Installation

    pip install deep-rec

## Example

    python main.py --device cpu --epoch 2 

## API Documentation

https://rixwew.github.io/deep-rec (en construcción)


## Licence

MIT