import os
import settings

import matplotlib.pyplot as plt
from PIL import Image


# experiment_name = 'mini_imagenet_learn_miniimagenet_features'
experiment_name = 'celeba_imagenet_features'
# experiment_name = 'cactus_celeba_original3'
clusters_address = os.path.join(settings.PROJECT_ROOT_ADDRESS, 'models/sml/cache/', experiment_name, 'clusters_50')


for cluster_file in sorted([os.path.join(clusters_address, f) for f in os.listdir(clusters_address)]):
    lines = open(cluster_file).readlines()
    num_lines = len(lines)
    ncols = 5
    nrows = 5
    fig, axes = plt.subplots(
        nrows,
        ncols,
        sharex='all',
        sharey='all',
    )
    print(num_lines)

    for row in range(nrows):
        for col in range(ncols):
            index = row * ncols + col
            if index == num_lines:
                break
            try:
                line = lines[index][:-1]
            except:
                break
            class_name = line[:line.rindex('/')]
            class_name = class_name[class_name.rindex('/') + 1:]
            img = Image.open(line)
            axes[row, col].imshow(img)
            axes[row, col].set_xlabel(class_name)

    plt.show()
    input('show next?')

