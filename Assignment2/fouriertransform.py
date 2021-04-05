import numpy as np

def dft(signal):
    signal = np.asarray(signal, dtype=complex) # Put input as array with complex type
    N = signal.shape[0]   # Return number of rows in array

    # Instantiate array of zeros of length rows with complex type
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

def dft_2d(signal):
    signal = np.asarray(signal, dtype=complex)

    # Store both dimensions of the array
    N = signal.shape[0]
    M = signal.shape[1]

    # Instantate arrays of 0s with same dimensions 
    row = np.zeros((N, M), dtype=complex) 
    dft_2d = np.zeros((M, N), dtype=complex) 
    
    # Compute the dft of input and store it in row
    for n in range(N):
        row[n] = dft(signal[n])

    column = row.transpose()

    # Compute dft of transposed array
    for m in range(M):
        dft_2d[m] = dft(column[m])

    return dft_2d.transpose()

def inverse_dft_2d(X):
    X = np.asarray(X, dtype=complex)
    # Store both dimensions of the array
    N = X.shape[0]
    M = X.shape[1]

    # Instantate arrays of 0s with same dimensions 
    row = np.zeros((N, M), dtype=complex)
    inverse_dft_2d = np.zeros((M, N), dtype=complex)

    for n in range(N):
        row[n] = inverse_dft(X[n])

    column = row.transpose()

    # Compute dft of transposed array
    for m in range(M):
        inverse_dft_2d[m] = inverse_dft(column[m])

    return inverse_dft_2d.transpose()

def fft(signal):
    threshold = 16
    signal = np.asarray(signal, dtype=complex)
    N = signal.shape[0]

    if N > threshold:
        even = fft(signal[::2])
        odd = fft(signal[1::2])
        result = np.zeros(N, dtype=complex)
        for n in range(N):
            result[n] = even[n % (N // 2)] + np.exp(-2j * np.pi * n / N) * odd[n % (N // 2)]
        return result
    else:
        return dft(signal)

def inverse_fft(signal):
    threshold = 16
    signal = np.asarray(signal, dtype=complex)
    N = signal.shape[0]

    if N > threshold:
        even = inverse_fft(signal[::2])
        odd = inverse_fft(signal[1::2])
        result = np.zeros(N, dtype=complex)
        for n in range(N):
            result[n] = (N // 2) * even[n % (N // 2)] + np.exp(2j * np.pi * n / N) * (N // 2) * odd[n % (N // 2)]
            result[n] = result[n] / N

        return result
    else:
        return inverse_dft(signal)

def fft_2d(signal):
    signal = np.asarray(signal, dtype=complex)
    width, height = signal.shape
    result = np.zeros((width, height), dtype=complex)

    for i in range(height):
        result[:, i] = fft(signal[:, i])
    for i in range(width):
        result[i, :] = fft(result[i, :])

    return result

def inverse_fft_2d(signal):
    signal = np.asarray(signal, dtype=complex)
    width, height = signal.shape
    result = np.zeros((width, height), dtype=complex)

    for i in range(width):
        result[i, :] = inverse_fft(signal[i, :])
    for i in range(height):
        result[:, i] = inverse_fft(result[:, i])

    return result