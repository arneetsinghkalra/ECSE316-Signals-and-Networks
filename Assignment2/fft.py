import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cv2
import time
import math
import fouriertransform

def main():
    args = get_args()
    # Store values 
    mode = args.mode
    image_path = args.image
    # Get grayscale image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if mode == 1:
        run_fft(image)
    if mode == 2:
        denoise(image)
    if mode == 3:
        compress(image)
    if mode == 4:
        produce_plots()

def run_fft(image):
    # Obtain fft 2d
    fft_image = fouriertransform.fft_2d(pad_image(image))

    # Plot images
    figure, axes = plt.subplots(1, 2)
    axes[0].imshow(image, plt.gray)
    axes[1].imshow(np.abs(fft_image), norm=colors.LogNorm())
    plt.show()
    
def denoise(image):
    # Obtain fft_2d
    fft_image = fouriertransform.fft_2d(pad_image(image))

    # Remove high values
    ratio = 0.1
    width, height = fft_image.shape
    fft_image[int(ratio * width) : int((1 - ratio) * width)] = 0
    fft_image[:, int(ratio * height) : int((1 - ratio) * height)] = 0

    # Obtain inverse_fft_2d
    inverse_fft_image = fouriertransform.inverse_fft_2d(fft_image).real

    # Plot images
    figure, axes = plt.subplots(1, 2)
    axes[0].imshow(image, plt.gray)
    axes[1].imshow(inverse_fft_image[:image.shape[0], :image.shape[1]], plt.gray)
    plt.show()

def compress(image):
    # Obtain fft_2d
    fft_image = fouriertransform.fft_2d(pad_image(image))

    # Compress
    compress_factors = [0, 10, 25, 50, 75, 95]
    compressed_images = compress_image(image, fft_image, compress_factors)

    # Plot image compressions
    figure, axes = plt.subplots(2, 3)
    axes[0, 0].imshow(np.real(compressed_images[0])[:image.shape[0], :image.shape[1]], plt.gray)
    axes[0, 1].imshow(np.real(compressed_images[1])[:image.shape[0], :image.shape[1]], plt.gray)
    axes[0, 2].imshow(np.real(compressed_images[2])[:image.shape[0], :image.shape[1]], plt.gray)
    axes[1, 0].imshow(np.real(compressed_images[3])[:image.shape[0], :image.shape[1]], plt.gray)
    axes[1, 1].imshow(np.real(compressed_images[4])[:image.shape[0], :image.shape[1]], plt.gray)
    axes[1, 2].imshow(np.real(compressed_images[5])[:image.shape[0], :image.shape[1]], plt.gray)
    plt.show()

def compress_image(image, fft_image, compressed):
    # Get original image size
    size = image.shape[0] * image.shape[1]
    compressed_images = []
    inversed_compressed_images = []
    
    # Compress image by the appropriate factors
    for i in compressed:
        non_zero = int(size * (100 - i) / 100)
        print("Number of nonzero Fourier coefficients for {}% compression: {}".format(i, non_zero))
        low = np.percentile(fft_image, (100 - i) // 2)
        high = np.percentile(fft_image, 100 - (100 - i) // 2)
        compressed_images.append(fft_image * np.logical_or(fft_image <= low, fft_image >= high))
    
    # Obtain inverse_fft_2d
    for i in compressed_images:
        inversed_compressed_images.append(fouriertransform.inverse_fft_2d(i))

    return inversed_compressed_images

def produce_plots():
    # Generate Arrays of Random numbers
    test_arrays = [
        np.random.random((2 ** 5, 2 ** 5)),
        np.random.random((2 ** 6, 2 ** 6)),
        np.random.random((2 ** 7, 2 ** 7)),         # DFT Mean around 5.5s, var around 0.0119s
        np.random.random((2 ** 8, 2 ** 8)),         # DFT Mean around 42.838s, var around 1.19s
        np.random.random((2 ** 9, 2 ** 9)),       # DFT Mean around 372.367s, var around 5.299s (Super long)
        np.random.random((2** 10, 2** 10))        # (Going to take way too long to run)
    ]
    # Store results
    dimensions_array = []
    dft_mean_array = []
    dft_variance_array = []
    fft_mean_array = []
    fft_variance_array = []

    for array in test_arrays:
        # Store problem size and append to designated array
        dimension = array.shape[0]
        dimensions_array.append(dimension)

        dft_results = []
        fft_results = []
        for i in range(10):
            # Naive DFT Method
            start_time = time.time()
            fouriertransform.dft_2d(array)
            end_time = time.time()
            dft_results.append(end_time - start_time)

            # FFT Method
            start_time = time.time()
            fouriertransform.fft_2d(array)
            end_time = time.time()
            fft_results.append(end_time - start_time)
        
        # Store dft mean and variance
        dft_mean = np.mean(dft_results)
        dft_mean_array.append(dft_mean)
        dft_variance = np.var(dft_results)
        dft_variance_array.append(dft_variance)

        # Store fft mean and variance
        fft_mean = np.mean(fft_results)
        fft_mean_array.append(fft_mean)
        fft_variance = np.var(fft_results)
        fft_variance_array.append(fft_variance)

        # Print mean and variance
        print('Array Dimensions: {} by {}'.format(dimension, dimension))
        print("----------------------------------------")
        print("DFT Mean: ", dft_mean)
        print("FFT Mean: ", np.mean(fft_results))
        print("DFT Variance: ", dft_variance)
        print("FFT Variance: ", np.var(fft_results))
        print("----------------------------------------\n")

        # Plot Results
    # Error is standard deviation * 2
    dft_errors = [math.sqrt(i) * 2 for i in dft_variance_array]
    fft_errors = [math.sqrt(i) * 2 for i in fft_variance_array]

    plt.errorbar(dimensions_array, dft_mean_array, yerr = dft_errors,ecolor="red", label='DFT')
    plt.errorbar(dimensions_array, fft_mean_array, color = 'green', yerr = fft_errors, ecolor="red", label='FFT')
    plt.title('Mean Time vs Problem Size')
    plt.xlabel('Problem Size', fontsize=14)
    plt.ylabel('Runtime (s)', fontsize=14)
    plt.legend(loc = 'upper left')
    plt.grid(True)
    plt.show()
    

def pad_image(image):
    width = int(pow(2, math.ceil(math.log2(image.shape[0]))))
    height = int(pow(2, math.ceil(math.log2(image.shape[1]))))

    new_shape = width, height
    new_image = np.zeros(new_shape)
    new_image[:image.shape[0], :image.shape[1]] = image

    return new_image

def get_args():
    # Initialize parser
    parser = argparse.ArgumentParser(description="python fft.py [-m mode] [-i image]")

    # Adding optional arguments
    parser.add_argument(
        "-m", "--mode", type=int, dest='mode', default=1,
        help="- [1] (Default) for fast mode where the image is converted into its FFT form and displayed - [2] for denoising where the image is denoised by applying an FFT, truncating high frequencies and then displayed - [3] for compressing and saving the image - [4] for plotting the runtime graphs for the report"
    )
    parser.add_argument(
        "-i", "--image", dest='image', default = "moonlanding.png",
        help="image (optional): filename of the image we wish to take the DFT of. (Default: the file name of the image given to you for the assignment)"
    )

    return parser.parse_args()

if __name__ == "__main__":
    main()