_data = {
    'imagenet': {
        'mean': [0.485, 0.456, 0.406], # mean
        'std': [0.229, 0.224, 0.225], # std
    },
    'cifar10': {
        'mean': [0.49139968, 0.48215841, 0.44653091], # mean
        'std': [0.24703223, 0.24348513, 0.26158784], # std
    },
    'cifar100': {
        'mean': [0.50707516, 0.48654887, 0.44091784],
        'std': [0.26733429, 0.25643846, 0.27615047],
    },
    'mnist': {
        'mean': [0.13066047430038452],
        'std': [0.30810779333114624],
    },
}

def get_dataset_mean_std(dataset_name: str='') -> dict:
    # names = ['cifar10', 'cifar100', 'mnist']
    if dataset_name not in _data.keys():
        print(f"dataset available: {[i for i in _data.keys()]}")
        return None
    else:
        return _data[dataset_name]