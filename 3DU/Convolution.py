import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np


def read_image(path:str) -> np.ndarray:
    """
    function that reads image as np.ndarray with given path
    """
    return img.imread(path)


def convoluiton(image:np.ndarray, kernel:int) -> np.ndarray:
    """
    function that applies convolution on image with given kernel size
    convolution with kernel
    [[ 1 ... 1 ]
     [ .  1  . ]
     [ 1 ... 1 ]]
    """
    #check if kernel is odd
    if kernel%2==0:
        return print("Kernel can only be odd number")
    #initializing image to write
    new_image = np.empty(image.shape)
    #iterating thru all pixels in original image
    start_range = int((kernel-1)/2)
    end_range = image.shape[0]-int((kernel-1)/2)
    for row in range(start_range, end_range):
        for column in range(start_range, end_range):
            #iterating thru kernel
            kernel_row_start = row - int((kernel-1)/2)
            kernel_row_end = row + int((kernel-1)/2)
            kernel_col_start = column - int((kernel-1)/2)
            kernel_col_end = column + int((kernel-1)/2)
            sum_of_kernel = 0
            for k_row in range(kernel_row_start, kernel_row_end):
                for k_col in range(kernel_col_start, kernel_col_end):
                    sum_of_kernel = sum_of_kernel + image[k_row][k_col]
            new_image[row][column] = sum_of_kernel/(kernel*kernel)

    return new_image

def show_image(image:np.ndarray, new_image:np.ndarray) -> None:
    """
    shows given image
    """
    figure, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    ax1.imshow(image)
    ax2.imshow(new_image)
    figure.show()
    plt.show()


if __name__ == "__main__":
    image = read_image("./image.png")
    new_image = convoluiton(image, 11)
    show_image(image, new_image)
