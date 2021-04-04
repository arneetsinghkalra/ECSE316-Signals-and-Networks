import argparse
import numpy as np
import matplotlib as plot
import cv2
import fouriertransform

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
    print("compress")



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
