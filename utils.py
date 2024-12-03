import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import torch
import torch.nn as nn


def load_images(path):
    with open(path, "rb") as f:
        magic_num = int.from_bytes(f.read(4), "big")
        image_num = int.from_bytes(f.read(4), "big")
        row_num = int.from_bytes(f.read(4), "big")
        col_num = int.from_bytes(f.read(4), "big")
        arr_int = list(bytearray(f.read()))

    return np.array(arr_int).reshape((image_num, row_num, col_num))


def load_labels(path):
    with open(path, "rb") as f:
        magic_num = int.from_bytes(f.read(4), "big")
        label_num = int.from_bytes(f.read(4), "big")
        arr_int = list(bytearray(f.read()))

    return np.array(arr_int)


def categorize(images, labels):
    label_types = np.unique(labels)

    return {
        label_type: images[np.where(labels == label_type)[0]]
        for label_type in label_types
    }


def generate_sum_combination(array, digit_sum):
    combs = np.array(list(product(array, repeat=digit_sum)))

    return {
        num: combs[np.where(np.sum(combs, axis=1) == num)]
        for num in range(digit_sum * 9 + 1)
    }


def pick_image_accord_sum_combination(label_image, combination, num):
    images = []

    for digit in combination:
        images_len = len(label_image[digit])
        images.append(label_image[digit][np.random.choice(images_len, num)])

    return np.moveaxis(images, 0, 1)


def sum_dataset(images, labels, size, digit_sum=3):
    label_image = categorize(images, labels)
    sum_combinations = generate_sum_combination(range(10), digit_sum)

    new_images = []
    new_labels = []

    for label, combs in sum_combinations.items():
        for comb in combs:
            new_images.extend(
                pick_image_accord_sum_combination(label_image, comb, size)
            )
            new_labels.extend(np.full(size, label))

    new_images = np.array(new_images)
    new_labels = np.array(new_labels)

    return new_images.reshape(-1, digit_sum, 28, 28), new_labels.reshape(-1)


# def sum_dataset(images, labels, size, num_digit):

#     random_indices = np.random.choice(len(images), (size, num_digit))

#     images_sum = np.array(images[random_indices])
#     labels_sum = np.sum(labels[random_indices], axis=1)

#     return images_sum, labels_sum


def add_blank(images, labels, num_zero):
    zero_indices = np.random.choice(len(images), num_zero)

    images[zero_indices] = np.zeros((images.shape[1], images.shape[2]))
    labels[zero_indices] = 0


# sum_combinations = generate_sum_combination(range(10), 6)

# for num, combs in sum_combinations.items():
#     print(f"{num}: {len(combs)}")


# def plot_data(data, row, col):
#     images, labels = data
#     digit_num = images.shape[1]

#     fig, axes = plt.subplots(row, col * (digit_num + 1), figsize=(15, row))
#     data_acc = 0
#     i = 0

#     axes = axes.flatten()
#     for a, ax in enumerate(axes):
#         if i < digit_num:
#             ax.imshow(images[data_acc][i], cmap="gray")
#             i += 1
#         else:
#             ax.text(
#                 0.5,
#                 0.5,
#                 labels[data_acc],
#                 fontsize=50,
#                 ha="center",  # Horizontal alignment: center
#                 va="center",  # Vertical alignment: center
#                 transform=ax.transAxes,
#             )  # Use axis coordinates (0 to 1)
#             data_acc += 1
#             i = 0
#         ax.axis("off")

#     fig.tight_layout()


# images = load_images(
#     r"C:\Users\trand\longg\code\python\deep learning\mnist\pytorch\mnist\test\t10k-images.idx3-ubyte"
# )
# labels = load_labels(
#     r"C:\Users\trand\longg\code\python\deep learning\mnist\pytorch\mnist\test\t10k-labels.idx1-ubyte"
# )


# test_image, test_label = sum_dataset(images, labels, 3000, 2)
# print(test_image.shape)
# print(test_label.shape)

# print(test_label)

# # plot_data((test_image, test_label), 5, 4)
# plt.hist(test_label, bins=3)
# plt.tick_params(axis="both", which="major", labelsize=12)
# plt.xticks([0, 1, 2])

# plt.show()
