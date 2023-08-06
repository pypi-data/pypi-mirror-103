import torch

def tensor_to_rgb_image_without_normalization(tensor:torch.Tensor):
    """Pytorh Helper method to get RGB numpy array for plotting"""
    np_img = tensor.cpu().numpy().transpose((1, 2, 0))
    m1, m2 = np_img.min(axis=(0, 1)), np_img.max(axis=(0, 1)) # remove Normalization for visualization
    return (255.0 * (np_img - m1) / (m2 - m1)).astype("uint8")