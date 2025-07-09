import numpy as np
import cv2


def save_numpy_array_as_image(np_array, output_path):
    try:
        # Ensure the array is of type uint8 for saving as an image
        img_to_save = np_array.astype(np.uint8)
        cv2.imwrite(output_path, img_to_save)
        print(f"Successfully saved NumPy array as image to '{output_path}'")
    except Exception as e:
        print(f"An error occurred while saving numpy array to image: {e}")

def load_image_to_numpy_array(image_path):
    try:
        # Load the image using OpenCV. By default, it loads as BGR.
        img_array_bgr = cv2.imread(image_path)
        if img_array_bgr is None:
            print(f"Error: Could not load image from '{image_path}'. Check if path is correct and image exists.")
            return None
        print(f"Successfully loaded '{image_path}' to NumPy array (BGR format).")
        print(f"Loaded image array shape: {img_array_bgr.shape}")
        return img_array_bgr
    except Exception as e:
        print(f"An error occurred while loading image: {e}")
        return None

def calculateAvg(kernel, imgArr, pix, imgShape):
    offsetDiag = kernel // 2

    # Calculate the start and end coordinates for the kernel window
    start_x = pix["x"] - offsetDiag
    start_y = pix["y"] - offsetDiag
    end_x = pix["x"] + offsetDiag
    end_y = pix["y"] + offsetDiag

    sum_channels = [0.0, 0.0, 0.0] # Use floats for summation
    toDivide = 0

    # Iterate through the kernel window
    for y_coord in range(start_y, end_y + 1):
        for x_coord in range(start_x, end_x + 1):
            # Check for boundary conditions
            if 0 <= y_coord < imgShape[0] and 0 <= x_coord < imgShape[1]:
                currPix = imgArr[y_coord][x_coord]
                sum_channels[0] += currPix[0]
                sum_channels[1] += currPix[1]
                sum_channels[2] += currPix[2]
                toDivide += 1
            # else:
            #     # If a pixel is out of bounds, you might choose to pad (e.g., with zeros, replicate border, etc.)
            #     # For a simple average blur, skipping out-of-bounds pixels is common for "valid" padding,
            #     # but can lead to darker edges if not handled by reducing `toDivide` for those cases.
            #     # Your current implementation effectively skips them, which is okay for a basic blur.
    
    # Avoid division by zero if toDivide is 0 (shouldn't happen with valid kernels and images)
    if toDivide == 0:
        return [0.0, 0.0, 0.0] # Or the original pixel value, depending on desired behavior

    return [sum_channels[0] / toDivide, sum_channels[1] / toDivide, sum_channels[2] / toDivide]


if __name__ == "__main__":
    imgArr = load_image_to_numpy_array("./test.jpg")

    if imgArr is None:
        print("Image loading failed. Exiting.")
    else:
        imgShape = imgArr.shape

        kernel = 21 # 3x3 kernel for averaging
        
        # Initialize newImg with the same shape but with float type for accurate averaging
        # It's better to initialize it as float and then convert to uint8 before saving
        newImg = np.zeros_like(imgArr, dtype=np.float32) 

        for i in range(imgShape[0]): # Iterate over rows (y-coordinate)
            for j in range(imgShape[1]): # Iterate over columns (x-coordinate)
                # Pass the current pixel coordinates
                newImg[i][j] = calculateAvg(kernel, imgArr, {"y": i, "x": j}, imgShape)
        
        # Convert the processed image to uint8 before saving
        save_numpy_array_as_image(newImg, './test2.jpg')

"""

# Negative
    for i in range(0, 853):
        for j in range(0, 1280):
            temp = imgArr[i][j]
            temp[0] = 255 - temp[0]
            temp[1] = 255 - temp[1]
            temp[2] = 255 - temp[2]
            imgArr[i][j] = temp   



# Saturation
    sat = 100
    temp = [0, 0 ,0]

    def rgb_to_hsv_opencv_ranges(R, G, B):
        # 1. Normalize RGB to 0-1 range
        r_norm = R / 255.0
        g_norm = G / 255.0
        b_norm = B / 255.0

        # 2. Find Max, Min, and Delta
        C_max = max(r_norm, g_norm, b_norm)
        C_min = min(r_norm, g_norm, b_norm)
        delta = C_max - C_min

        # 3. Calculate Value (V)
        V_final = C_max

        # 4. Calculate Saturation (S)
        if C_max == 0:
            S_final = 0.0
        else:
            S_final = delta / C_max

        # 5. Calculate Hue (H)
        H_degrees = 0.0 # Default for grayscale/achromatic
        if delta == 0:
            H_degrees = 0.0 # Achromatic (grayscale)
        elif C_max == r_norm:
            H_degrees = 60 * (((g_norm - b_norm) / delta) % 6)
        elif C_max == g_norm:
            H_degrees = 60 * (((b_norm - r_norm) / delta) + 2)
        elif C_max == b_norm:
            H_degrees = 60 * (((r_norm - g_norm) / delta) + 4)

        # Ensure H is non-negative
        if H_degrees < 0:
            H_degrees += 360

        # 6. Scale for OpenCV Ranges
        H_opencv = int(H_degrees / 2)       # H: 0-179
        S_opencv = int(S_final * 255)       # S: 0-255
        V_opencv = int(V_final * 255)       # V: 0-255

        return (H_opencv, S_opencv, V_opencv)

    def hsv_to_rgb_opencv_ranges(H, S, V):
        # 1. Normalize H, S, V to common ranges (H: 0-360, S: 0-1, V: 0-1)
        h_norm = H * 2.0  # Scale H from 0-179 to 0-359.99... degrees
        s_norm = S / 255.0 # Scale S from 0-255 to 0-1
        v_norm = V / 255.0 # Scale V from 0-255 to 0-1

        r_final, g_final, b_final = 0.0, 0.0, 0.0

        if s_norm == 0:
            # Achromatic (grayscale) color
            r_final = v_norm
            g_final = v_norm
            b_final = v_norm
        else:
            # Calculate chroma (C)
            C = v_norm * s_norm
            
            # Calculate hue segment (H_prime)
            # H_prime is H in degrees divided by 60 to get a segment from 0 to 6
            H_prime = h_norm / 60.0

            # Calculate X (intermediate value)
            X = C * (1 - abs((H_prime % 2) - 1))

            # Determine RGB based on hue segment
            if 0 <= H_prime < 1:
                r_final, g_final, b_final = C, X, 0
            elif 1 <= H_prime < 2:
                r_final, g_final, b_final = X, C, 0
            elif 2 <= H_prime < 3:
                r_final, g_final, b_final = 0, C, X
            elif 3 <= H_prime < 4:
                r_final, g_final, b_final = 0, X, C
            elif 4 <= H_prime < 5:
                r_final, g_final, b_final = X, 0, C
            elif 5 <= H_prime < 6:
                r_final, g_final, b_final = C, 0, X
            
            # Calculate m (value to add back to each RGB component)
            m = v_norm - C

            r_final += m
            g_final += m
            b_final += m

        # Scale RGB back to 0-255 range and convert to int
        R_opencv = int(r_final * 255)
        G_opencv = int(g_final * 255)
        B_opencv = int(b_final * 255)

        # Ensure values are within 0-255 in case of floating point inaccuracies
        R_opencv = np.clip(R_opencv, 0, 255)
        G_opencv = np.clip(G_opencv, 0, 255)
        B_opencv = np.clip(B_opencv, 0, 255)

        return (B_opencv, G_opencv, R_opencv)
        
    for i in range(0, 853):
        for j in range(0, 1280):
            temp = imgArr[i][j]
            tem2 = rgb_to_hsv_opencv_ranges(temp[0], temp[1], temp[2])
            #temp = [tem2[0], tem2[1] - sat, tem2[2]]
            imgArr[i][j] = hsv_to_rgb_opencv_ranges(tem2[0], tem2[1] - sat, tem2[2])


# Darkness
    dark = 1 - 0.1
    for i in range(0, 853):
        for j in range(0, 1280):
            temp = imgArr[i][j]
            temp[0] = temp[0] - int(dark*temp[0])
            temp[1] = temp[1] - int(dark*temp[1])
            temp[2] = temp[2] - int(dark*temp[2])
            imgArr[i][j] = temp

         

# De pixel
    pixSize = 50
    temp = [0, 0 , 0]
    for i in range(0, 853):
        for j in range(0, 1280):
            if(j%pixSize == 0 or i%pixSize == 0):
                temp = imgArr[i][j]
            imgArr[i][j] = temp         

# Exposure
    exp = -50
    temp = [0, 0 ,0]
    def inc(a):
        b = np.int32(a) + exp
        if(b > 255):
            return 255
        elif  b < 0:
            return 0
        else:
            return b
    for i in range(0, 853):
        for j in range(0, 1280):
            temp = imgArr[i][j]
            temp[0] = inc(temp[0])
            temp[1] = inc(temp[1])
            temp[2] = inc(temp[2])
            imgArr[i][j] = temp               
"""    