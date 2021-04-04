import numpy as np

def dft(signal):
    signal = np.asarray(signal, dtype=complex) # Put input as array with complex type
    N = signal.shape[0]   #Return number of rows in array

    #Instantiate array of zeros of length rows with complex type
    dft = np.zeros(N, dtype=complex)

    for k in range(N):
        for n in range(N):
            # DFT formula
            dft[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)

    return dft

def inverse_dft(X):
    X = np.asarray(X, dtype=complex)
    N = X.shape[0]
    inverse_dft = np.zeros(N, dtype=complex)

    for n in range(N):
        for k in range(N):
            inverse_dft[n] += X[k] * np.exp(2j * np.pi * k * n / N)

        inverse_dft[n] = inverse_dft[n] / N

    return inverse_dft

#Implementing 2d dft and inverse to use for mode 4
def dft_2d(signal):
    signal = np.asarray(signal, dtype=complex)

    # Store both dimensions of the array
    N = signal.shape[0]
    M = signal.shape[1]

    #Instantate arrays of 0s with same dimensions 
    row = np.zeros((N, M), dtype=complex) 
    dft_2d = np.zeros((M, N), dtype=complex) 
    
    # Compute the DFT of input and store it in row
    for n in range(N):
        row[n] = dft(signal[n])

    column = row.transpose()

    # Compute DFT of transposed array
    for m in range(M):
        dft_2d[m] = dft(column[m])

    return dft_2d.transpose()

def inverse_dft_2d(X):
    X = np.asarray(X, dtype=complex)
    # Store both dimensions of the array
    N = X.shape[0]
    M = X.shape[1]

    #Instantate arrays of 0s with same dimensions 
    row = np.zeros((N, M), dtype=complex)
    inverse_dft_2d = np.zeros((M, N), dtype=complex)

    for n in range(N):
        row[n] = inverse_dft(X[n])

    column = row.transpose()

    # Compute DFT of transposed array
    for m in range(M):
        inverse_dft_2d[m] = inverse_dft(column[m])

    return inverse_dft_2d.transpose()