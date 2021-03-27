import argparse

def main():
    args = get_args()
    #Store values
    mode = args.mode
    image = args.image


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
