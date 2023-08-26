from sre_parse import TYPE_FLAGS
import cv2
import numpy as np
from tqdm import tqdm
import time

class PointProcessing():
    # def __init__():

    #Negative Transformation
    def negative_transformation(self, image, color_type=None):
        # Gray Image
        if(len(image.shape)==2):    
            width, height = image.shape[0], image.shape[1]
            result = np.ones((width, height))*np.max(image)
            result = result-image
        # RGB Image
        elif(len(image.shape)==3 and color_type=="RGB"):    
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = np.ones((width, height, channel))
            for i in range(3):
                result[:, :, i] = result[:, :, i]*np.max(image[:, :, i])    # 각 채널 별 최대값
            result = result-image
        # HSI Image
        elif(len(image.shape)==3 and color_type=="HSI"):    
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = image.copy()
            for i in range(1, 3):   # Saturation, Intensity Channel만 Transform
                result[:,:,i] = np.max(image[:,:,i]) - result[:,:,i]
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.array(result, dtype='uint8')
    
    #Power Law Transformation
    def power_law_transformation(self, image, gamma, color_type=None):
        # Gray / RGB Image
        if(color_type=="GRAY" or color_type=="RGB"):
            result = np.array(255*(image/255)**gamma, dtype='uint8')
        # HSI Image
        elif(color_type=="HSI"):    # Saturation, Intensity Channel만 Transform
            result = np.array(image, dtype='uint8')
            # result[:,:,0] = np.array(255*(image[:,:,0]/255)**gamma)
            result[:,:,1] = np.array(255*(image[:,:,1]/255)**gamma)
            result[:,:,2] = np.array(255*(image[:,:,2]/255)**gamma, dtype='uint8')
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return result

    #Histogram Equalization using openCV
    def histogram_equalization_cv(self, image, color_type=None):
        result = cv2.equalizeHist(image)
        return result

    #Histogram Equalization
    def histogram_equalization(self, image, color_type=None):
        if(color_type=="GRAY"):
            channel = image
        elif(color_type=="HSI"):
            channel = image[:,:,2]

        width, height = channel.shape[0], channel.shape[1]
        max = np.max(channel) + 1
        min = np.min(channel)
        num_pixel = width*height

        #scale histogram
        hist = np.zeros(max)
        #cdf of scale histogram
        sum_hist = np.zeros(max)
        #normalized sum
        norm_hist = np.zeros(max)

        result = np.zeros((width, height))
        sum = 0
        for i in range(width):
            for j in range(height):
                hist[channel[i][j]] += 1    # intensity 값에 따라 매핑
        min = sum_hist[min]
        for i in range(max):
            sum+=hist[i]
            sum_hist[i] = sum
            norm_hist[i] = np.around((max-1)*(sum_hist[i]-min)/(num_pixel-min)) # MinMax Normalization

        # Rearrange    
        for i in range(width):
            for j in range(height):
                result[i][j] = norm_hist[channel[i][j]]

        if(color_type=="GRAY"):
            return np.array(result, dtype='uint8')
        elif(color_type=="HSI"):
            result_hsi = image
            result_hsi[:,:,2] = result
            result_hsi = cv2.cvtColor(result_hsi, cv2.COLOR_HSV2RGB)
            return result_hsi

        
class AreaProcessing():
    # def __init__():
        
    #Mean Filter(Average Filter)
    def mean_filter(self, image, size, color_type=None):
        total_size = size**2
        radius = int((size-1)/2)
        # Gray Image
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j] = np.sum(image[i:i+size,j:j+size])/total_size
        # RGB Image
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = np.zeros((width-2*radius, height-2*radius, channel))
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        result[i,j,ch] = np.sum(image[i:i+size,j:j+size,ch])/total_size
        # HSI Image
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j,2] = np.sum(image[i:i+size,j:j+size,2])/total_size
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.array(result, dtype='uint8')

    #Median Filter
    def median_filter(self, image, size, color_type=None):
        radius = int((size-1)/2)
        # Gray Image
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j] = np.median(image[i:i+size,j:j+size])
        # RGB Image
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = np.zeros((width-2*radius, height-2*radius, channel))
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        result[i,j,ch] = np.median(image[i:i+size,j:j+size,ch])
        # HSI Image
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j,2] = np.median(image[i:i+size,j:j+size,2])
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.array(result, dtype='uint8')
    
    #Gaussian Filter
    def gaussian_filter(self, image, size, sigma, color_type=None):
        kernel1d = cv2.getGaussianKernel(size, sigma)
        kernel2d = np.outer(kernel1d, kernel1d.transpose())
        radius = int((size-1)/2)
        # Gray Image
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j] = np.sum(np.multiply(image[i:i+size,j:j+size], kernel2d))
        # RGB Image
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = np.zeros((width-2*radius, height-2*radius, channel))
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        result[i,j,ch] = np.sum(np.multiply(image[i:i+size,j:j+size,ch], kernel2d))
        # HSI Image
        elif(len(image.shape)==3 and color_type=="HSI"):    # Intensity만 Transform
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j,2] = np.sum(np.multiply(image[i:i+size,j:j+size,2], kernel2d))
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.array(result, dtype='uint8')
    
    #High-Boost Filter
    def highboost_filter(self, image, alpha, highpass, color_type=None):
        size = 3
        radius = int((size-1)/2)
        if(highpass==4):
            kernel = np.zeros((size, size))
            kernel[radius-1, radius] = kernel[radius+1, radius] = -1
            kernel[radius, radius-1] = kernel[radius, radius+1] = -1
            kernel[radius, radius] = 4 + alpha
        elif(highpass==8):
            kernel = -np.ones((size, size))
            kernel[radius, radius] = 8 + alpha
        
        # Gray Image
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j] = np.sum(np.multiply(image[i:i+size,j:j+size], kernel))
        # RGB Image
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        result[i,j,ch] = np.sum(np.multiply(image[i:i+size,j:j+size,ch], kernel))
        # HSI Image
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j,2] = np.sum(np.multiply(image[i:i+size,j:j+size,2], kernel))
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.clip(np.array(result, dtype='uint8'), 0, 255)

class EdgeDetection():
    # def __init__():
    
    #Prewitt Operator
    def prewitt_operator(self, image, threshold, background, color_type=None):
        size = 3
        radius = 1
        prewitt_hor = np.array([[-1, 0, 1],
                                [-1, 0, 1],
                                [-1, 0, 1]])
        prewitt_ver = np.array([[1, 1, 1],
                                [0, 0, 0],
                                [-1, -1, -1]])
        threshold = 50*threshold

        # Gray Image
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    horizon = np.sum(np.multiply(image[i:i+size,j:j+size], prewitt_hor))
                    vertical = np.sum(np.multiply(image[i:i+size,j:j+size], prewitt_ver))
                    magnitude = np.sqrt(horizon**2 + vertical**2)
                    if magnitude>=threshold:
                        result[i,j] = 255
                    elif(background=='X'):
                        result[i,j] = 0
                    else:
                        result[i,j] = image[i+1, j+1]   #0으로 설정하면 테두리만 나옴
            return np.array(result, dtype='uint8')
        # RGB Image
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        horizon = np.sum(np.multiply(image[i:i+size,j:j+size,ch], prewitt_hor))
                        vertical = np.sum(np.multiply(image[i:i+size,j:j+size,ch], prewitt_ver))
                        magnitude = np.sqrt(horizon**2 + vertical**2)
                        if magnitude>=threshold:
                            result[i, j, ch] = 255
                        elif(background=='X'):
                            result[i, j, ch] = 0
            return np.array(result, dtype='uint8')
        # HSI Image
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    horizon = np.sum(np.multiply(image[i:i+size,j:j+size,2], prewitt_hor))
                    vertical = np.sum(np.multiply(image[i:i+size,j:j+size,2], prewitt_ver))
                    magnitude = np.sqrt(horizon**2 + vertical**2)
                    if magnitude>=threshold:
                        result[i,j,0], result[i,j,1], result[i,j,2] = 0, 0, 255
                    elif(background=='X'):
                        result[i,j,0], result[i,j,1], result[i,j,2] = 0, 0, 0
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
            return np.array(result, dtype='uint8')
    
    #Sobel Operator
    def sobel_operator(self, image, threshold, background, color_type=None):
        size = 3
        radius = 1
        sobel_hor = np.array([[-1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]])
        sobel_ver = np.array([[1, 2, 1],
                                [0, 0, 0],
                                [-1, -2, -1]])
        threshold = 50*threshold
        # Gray Image
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    horizon = np.sum(np.multiply(image[i:i+size,j:j+size], sobel_hor))
                    vertical = np.sum(np.multiply(image[i:i+size,j:j+size], sobel_ver))
                    magnitude = np.sqrt(horizon**2 + vertical**2)
                    if magnitude>=threshold:
                        result[i,j] = 255
                    elif(background=='X'):
                        result[i,j] = 0
                    else:
                        result[i,j] = image[i+1, j+1]   #0으로 설정하면 테두리만 나옴
            return np.array(result, dtype='uint8')
        # RGB Image
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        horizon = np.sum(np.multiply(image[i:i+size,j:j+size,ch], sobel_hor))
                        vertical = np.sum(np.multiply(image[i:i+size,j:j+size,ch], sobel_ver))
                        magnitude = np.sqrt(horizon**2 + vertical**2)
                        if magnitude>=threshold:
                            result[i, j, ch] = 255
                        elif(background=='X'):
                            result[i, j, ch] = 0
            return np.array(result, dtype='uint8')
        # HSI Image
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    horizon = np.sum(np.multiply(image[i:i+size,j:j+size,2], sobel_hor))
                    vertical = np.sum(np.multiply(image[i:i+size,j:j+size,2], sobel_ver))
                    magnitude = np.sqrt(horizon**2 + vertical**2)
                    if magnitude>=threshold:
                        result[i,j,0], result[i,j,1], result[i,j,2] = 0, 0, 255
                    elif(background=='X'):
                        result[i,j,0], result[i,j,1], result[i,j,2] = 0, 0, 0
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
            return np.array(result, dtype='uint8')

    #LoG Operator
    def LoG_operator(self, image, size, sigma, color_type=None):
        # HSI Image
        if(len(image.shape)==3 and color_type=="HSI"):
            blur = cv2.GaussianBlur(image[:,:,2], (size, size), sigma)
            result = cv2.Laplacian(blur, cv2.CV_8U, ksize=size)
        # Gray / RGB Image
        else:
            blur = cv2.GaussianBlur(image, (size, size), sigma)
            result = cv2.Laplacian(blur, cv2.CV_8U, ksize=size)
        return result
        
    #Canny Operator
    def canny_operator(self, image, min_threshold, max_threshold, color_type=None):
        # HSI Image
        if(len(image.shape)==3 and color_type=="HSI"):
            result = cv2.Canny(image[:,:,2], min_threshold, max_threshold)
        # Gray / RGB Image
        else:   
            result = cv2.Canny(image, min_threshold, max_threshold)
        return result
class FrameProcessing():
    # def __init__():
    def find_lowest_point(self, prev, next, x, y, w, z, radius):
        """
            주변 8개의 중심점 중 가장 유사한 Block의 중심을 찾는 함수입니다.
            유사도는 픽셀의 오차 제곱합을 이용합니다.
        """
        min_x, min_y = w, z
        try:
            residual = np.sum(np.multiply(next[min_x-1:min_x+2, min_y-1:min_y+2]-prev[x-1:x+2, y-1:y+2],next[min_x-1:min_x+2, min_y-1:min_y+2]-prev[x-1:x+2, y-1:y+2]))
            for (cx, cy) in [(w-radius, z+radius),(w, z+radius),(w+radius, z+radius),
                             (w-radius, z),(z+radius, z),
                             (w-radius, z-radius),(w, z-radius),(w+radius, z-radius)]:
                try:
                    new_residual = np.sum(np.multiply(next[cx-1:cx+2, cy-1:cy+2]-prev[x-1:x+2, y-1:y+2],next[cx-1:cx+2, cy-1:cy+2]-prev[x-1:x+2, y-1:y+2]))
                    if new_residual < residual:
                        min_x, min_y = cx, cy
                        residual = new_residual
                except:
                    pass
        except:
            pass
        return min_x, min_y
    
    #3-Step Search
    def three_step_search(self, frames, radius=4):
        color = np.random.randint(0,255,(200,3))
        lines = None  #추적 선을 그릴 이미지 저장 변수
        prev = None  # 이전 프레임 저장 변수
        
        new_frames = []
        for i in range(frames.shape[0]):
            img_draw = frames[i].copy()
            gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            if prev is None:
                prev = gray
                # 추적선 그릴 이미지를 프레임 크기에 맞게 생성
                lines = np.zeros_like(frames[i])
                # 추적 시작을 위한 코너 검출
                prevPt = cv2.goodFeaturesToTrack(prev, 200, 0.01, 10)
            else:
                next = gray
                for j, point in enumerate(prevPt):
                    a, b = int(point[0, 0].copy()), int(point[0, 1].copy())
                    c, d = self.find_lowest_point(prev, next, a, b, a, b, radius)
                    c, d = self.find_lowest_point(prev, next, a, b, c, d, int(radius/2))
                    c, d = self.find_lowest_point(prev, next, a, b, c, d, int(radius/4))
                    try:
                        # 이전 코너와 새로운 코너에 선그리기
                        cv2.line(lines, (int(a), int(b)), (int(c),int(d)), color[i].tolist(), 2)
                        # 새로운 코너에 점 그리기
                        cv2.circle(img_draw, (int(c),int(d)), 2, color[i].tolist(), -1)
                    except:
                        pass
                    prevPt[j, 0, 0], prevPt[j, 0, 1] = c, d
                # 누적된 추적 선을 출력 이미지에 합성
                img_draw = cv2.add(img_draw, lines)
                prev = next
            new_frames.append(img_draw)
        return np.array(new_frames, dtype='uint8')
    #Lucas_kanade
    def lucas_kanade(self, frames):
        """
            [참조] https://docs.opencv.org/3.4/dc/d6b/group__video__track.html#ga473e4b886d0bcc6b65831eb88ed93323
        """
        # 추적 경로를 그리기 위한 랜덤 색상
        color = np.random.randint(0,255,(200,3))
        lines = None  #추적 선을 그릴 이미지 저장 변수
        prev = None  # 이전 프레임 저장 변수
        # calcOpticalFlowPyrLK 중지 요건 설정
        termcriteria =  (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        new_frames = []
        for i in range(frames.shape[0]):
            img_draw = frames[i].copy()
            gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            if prev is None:
                prev = gray
                # 추적선 그릴 이미지를 프레임 크기에 맞게 생성
                lines = np.zeros_like(frames[i])
                # 추적 시작을 위한 코너 검출  ---①
                prevPt = cv2.goodFeaturesToTrack(prev, 200, 0.01, 10)
            else:
                next = gray
                # 옵티컬 플로우로 다음 프레임의 코너점  찾기 ---②
                nextPt, status, err = cv2.calcOpticalFlowPyrLK(prev, next, \
                                                prevPt, None, criteria=termcriteria)
                # 대응점이 있는 코너, 움직인 코너 선별 ---③
                prevMv = prevPt[status==1]
                nextMv = nextPt[status==1]
                for i,(p, n) in enumerate(zip(prevMv, nextMv)):
                    px,py = p.ravel()
                    nx,ny = n.ravel()
                    # 이전 코너와 새로운 코너에 선그리기 ---④
                    cv2.line(lines, (int(px), int(py)), (int(nx),int(ny)), color[i].tolist(), 2)
                    # 새로운 코너에 점 그리기
                    cv2.circle(img_draw, (int(nx),int(ny)), 2, color[i].tolist(), -1)
                # 누적된 추적 선을 출력 이미지에 합성 ---⑤
                img_draw = cv2.add(img_draw, lines)
                # 다음 프레임을 위한 프레임과 코너점 이월
                prev = next
                prevPt = nextMv.reshape(-1,1,2)
            new_frames.append(img_draw)
        return np.array(new_frames, dtype='uint8')
    #Gunar_farneback
    def gunar_farneback(self, frames):
        """
            cv2.calcOpticalFlowFarneback(prev, next, flow, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags)
            • prev, nex: 이전 영상과 현재 영상. 그레이스케일 영상.
            • flow: (출력) 계산된 옵티컬플로우. np.ndarray. shape=(h, w, 2), dtype=np.float32.
            • pyr_scale: 피라미드 영상을 만들 때 축소 비율. (e.g.) 0.5
            • levels: 피라미드 영상 개수. (e.g.) 3
            • winsize: 평균 윈도우 크기. (e.g.) 13
            • iterations: 각 피라미드 레벨에서 알고리즘 반복 횟수. (e.g.) 10
            • poly_n: 다항식 확장을 위한 이웃 픽셀 크기. 보통 5 또는 7.
            • poly_sigma: 가우시안 표준편차. 보통 poly_n = 5이면 1.1, poly_n = 7이면 1.5.
            • flags: 0, cv2.OPTFLOW_USE_INITIAL_FLOW, cv2.OPTFLOW_FARNEBACK_GAUSSIAN

            [참조] https://deep-learning-study.tistory.com/278
        """
        prev = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        hsv = np.zeros_like(frames[0])
        hsv[...,1] = 255
        new_frames = []
        for i in range(frames.shape[0]):
            if i==0:
                pass
            else:
                next = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
                # flow = cv2.calcOpticalFlowFarneback(prev, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                flow = cv2.calcOpticalFlowFarneback(prev, next, None, 0.5, 3, 5, 10, 5, 1.1, 0)
                mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                hsv[...,0] = ang*180/np.pi/2
                hsv[...,2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
                bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
                new_frames.append(bgr)
                prev = next
        return np.array(new_frames, dtype='uint8')

class ObjectDetection():
    #Frame RGB -> HSV
    def frames_rgb_to_hsv(self, frames):
        g_frames = []
        for frame in frames:
            g_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
        return np.array(g_frames, dtype='uint8')
    #Frame HSV -> RGB
    def frames_hsv_to_rgb(self, frames):
        g_frames = []
        for frame in frames:
            g_frames.append(cv2.cvtColor(frame, cv2.COLOR_HSV2BGR))
        return np.array(g_frames, dtype='uint8')
    #Delete Background
    def delete_background(self, frames):
        avg = np.zeros_like(frames[0], dtype='uint64')
        i=0
        # 프레임들의 평균 값 추출
        for frame in frames:
            i+=1
            avg += frame
        # 배경(프레임들의 평균 값) 제거
        avg = np.array(avg / i, dtype='uint8') 
        for j, frame in enumerate(frames):
            frames[j] =  frame - avg
        return frames
    #Thresholding video
    def thresholding(self, frames, thres_min, thres_max):
        for i, frame in enumerate(frames):
            _, frames[i] = cv2.threshold(frame, thres_min, 255, cv2.THRESH_TOZERO)
            _, frames[i] = cv2.threshold(frame, thres_max, 0, cv2.THRESH_TOZERO_INV)
        return frames
    #Connect Components
    def connect_components(self, frames, original_frames, area_min):
        for k, frame in enumerate(frames):
            cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(frame[:,:,2])
            for i in range(1, cnt):
                (x, y, w, h, area) = stats[i]
                if area < area_min:
                    continue
                cv2.rectangle(original_frames[k], (x, y), (x+w, y+h), (0,0,255), 2)
        return original_frames
    #Hand Detection
    def hand_detection(self, frames):
        hsv_frames = self.frames_rgb_to_hsv(frames)
        back_deleted_frames = self.delete_background(hsv_frames[:,:,:,2].copy())    # Intensity에서 배경 제거
        hsv_frames[:,:,:,2] = self.thresholding(back_deleted_frames, 100, 240)      # Thresholding
        
        hsv_frames = self.frames_hsv_to_rgb(hsv_frames)
        connected_frames = self.connect_components(hsv_frames, frames, 3000)        # Component 연결

        # return hsv_frames
        return connected_frames
    #Vehicle Detection
    def vehicle_detection(self, frames):
        hsv_frames = self.frames_rgb_to_hsv(frames)
        back_deleted_frames = self.delete_background(hsv_frames[:,:,:,2].copy())
        hsv_frames[:,:,:,2] = self.thresholding(back_deleted_frames, 70, 185)
        
        hsv_frames = self.frames_hsv_to_rgb(hsv_frames)
        connected_frames = self.connect_components(hsv_frames, frames, 120)

        return connected_frames

if __name__ == '__main__':
    pass