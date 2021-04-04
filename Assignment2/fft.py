import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cv2
import time
import fouriertransform
import math

def main():
    args = get_args() 
    #Store values
    mode = args.mode
    image_path = args.image

    # Get Image, grayscale so it is a 2D Array
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Resize image if need be
    image = resize_image(image)

    if mode == 1:
        run_fft()
    if mode == 2:
        run_denoised_fft()
    if mode == 3:
        compress()
    if mode == 4:
        produce_plots()
    

def run_fft():
    print("run fft")
    
def run_denoised_fft():
    print("run denoised fft")

def compress():
    print("compress")

def produce_plots():

    # Generate Arrays of Random numbers
    test_arrays = [np.random.random((2 ** 5, 2 ** 5)),
              np.random.random((2 ** 6, 2 ** 6)),
              np.random.random((2 ** 7, 2 ** 7)),         # DFT Mean around 5.5s, var around 0.0119s
              np.random.random((2 ** 8, 2 ** 8))          # DFT Mean around 42.838s, var around 1.19s
              #np.random.random((2 ** 9, 2 ** 9)),        # DFT Mean around 372.367s, var around 5.299s (Super long)
              #np.random.random((2** 10, 2** 10))         # (Going to take way too long to run)
              ]

    # Store results
    dimensions_array = []
    dft_mean_array = []
    dft_variance_array = []

    for array in test_arrays:
        # Store problem size and append to designated array
        dimension = array.shape[0]
        dimensions_array.append(dimension)

        dft_results = []
        # fft_rssults = []
        

        for i in range(1, 10):
            # Naive DFT Method
            start_time = time.time()
            fouriertransform.dft_2d(array)
            end_time = time.time()
            dft_results.append(end_time - start_time)

            # TODO: FFT Timing here
            # Naive DFT Method
            #start_time = time.time()
            #fouriertransform.fft_2d(array)
            #end_time = time.time()
            #fft_results.append(end_time - start_time)
        
        # Store mean and variance
        dft_mean = np.mean(dft_results)
        dft_variance = np.var(dft_results)

        dft_mean_array.append(dft_mean)
        dft_variance_array.append(dft_variance)


        # Print mean and variance
        print('Array Dimensions: {} by {}'.format(dimension, dimension))
        print("----------------------------------------")
        print("DFT Mean: ", dft_mean)
        print("DFT Variance: ", dft_variance)

        #print("FFT Mean: ", np.mean(fft_results))
        #print("FFT Variance: ", np.var(fft_results))
        print("----------------------------------------\n")

    # Plot Results
    # Error is standard deviation * 2
    errors = [math.sqrt(i) * 2 for i in dft_variance_array]

    plt.errorbar(dimensions_array, dft_mean_array, yerr = errors, label='DFT')
    plt.title('Mean Time vs Problem Size')
    plt.xlabel('Problem Size', fontsize=14)
    plt.ylabel('Runtime (s)', fontsize=14)
    plt.legend(loc = 'upper left')
    plt.grid(True)
    plt.show()



# Additional Helper Methods:
def resize_image(image):
    width, height = image.shape

    # If width is not a power of 2
    if not (width and (not (width & (width - 1)))):
        # Change value to next power of 2
        width = int(2 ** np.ceil(np.log2(width)))

    # If height is not a power of 2
    if not (height and (not (height & (height - 1)))):
        height = int(2 ** np.ceil(np.log2(height)))
    
    # Resize Image
    return cv2.resize(image, (width,height))


def get_args():
    # Initialize parser
    parser = argparse.ArgumentParser(description="python fft.py [-m mode] [-i image]")

    # Adding optional arguments
    parser.add_argument("-m", "--mode", type=int, dest='mode', default=1,
                        help="- [1] (Default) for fast mode where the image is converted into its FFT form and displayed - [2] for denoising where the image is denoised by applying an FFT, truncating high frequencies and then displayed - [3] for compressing and saving the image- [4] for plotting the runtime graphs for the report"
                        )
    parser.add_argument("-i", "--image", dest='image', default = "moonlanding.png",
                        help="image (optional): filename of the image we wish to take the DFT of. (Default: the file name of the image given to you for the assignment)"
                        )

    return parser.parse_args()


if __name__ == "__main__":
    main()
