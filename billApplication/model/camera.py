import numpy as np
import cv2
import tkinter.messagebox as messagebox

def _cornerPoints(bw: np.ndarray) -> np.ndarray:
    # detect contour of paper
    contours,_ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea)

    # detect corners
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * perimeter, True)

    return approx

def _getMask(frame: np.ndarray) -> np.ndarray:
    '''detects a paper by the use of GrabCut'''
    print(frame.shape)
    small = cv2.resize(frame, (0,0), fx=0.2, fy=0.2) 
    print(small.shape)
    #CLAHE adjustment
    lab = cv2.cvtColor(small, cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l,a,b))
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Repeated Closing operation to remove text from the document.
    kernel = np.ones((5,5),np.uint8)
    img = cv2.morphologyEx(bgr, cv2.MORPH_CLOSE, kernel, iterations= 3)

    mask = np.zeros(img.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    pad = 10
    rect = (pad,pad,img.shape[1]-2*pad,img.shape[0]-2*pad)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==cv2.GC_BGD)|(mask==cv2.GC_PR_BGD),0,1).astype('uint8')
    
    mask2 = cv2.resize(mask2, (frame.shape[1], frame.shape[0]))
    print(mask2.shape)
    return mask2

def _order_points(pts: np.ndarray):
    '''Rearrange coordinates to order:
      top-left, bottom-left, bottom-right, top-right'''
    rect = np.zeros((4, 2), dtype='float32')
    #pts = np.array(pts)
    s = pts.sum(axis=2)
    # Top-left point will have the smallest sum.
    rect[0] = pts[np.argmin(s)]
    # Bottom-right point will have the largest sum.
    rect[2] = pts[np.argmax(s)]
 
    diff = np.diff(pts, axis=2)
    # Bottom-left will have the largest difference.
    rect[1] = pts[np.argmax(diff)]
    # Top-right point will have the smallest difference.
    rect[3] = pts[np.argmin(diff)]
    # Return the ordered coordinates.
    return rect.astype('int').tolist()

def _transformImg(frame: np.ndarray, corners: list) -> np.ndarray:
    pts = _order_points(corners)
    (tl, bl, br, tr) = pts
    # Finding the maximum width.
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # Finding the maximum height.
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # Final destination co-ordinates.
    destination_corners = [[0, 0], [0, maxHeight], [maxWidth, maxHeight], [maxWidth, 0]]

    M = cv2.getPerspectiveTransform(np.float32(pts), np.float32(destination_corners))
    # Perspective transform using homography.
    final = cv2.warpPerspective(frame, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv2.INTER_LINEAR)
    return final
  
def _grabImage(port: int = 0) -> np.ndarray:
    '''opens the camera and show current frame
     ESC -> returns None, ENTER the current image'''

    vid = cv2.VideoCapture(port) # define a video capture object
    value = None
    while(True): 
        ret, frame = vid.read()
        cv2.imshow("Camera", frame) 
        
        key = cv2.waitKey(10)
        if key == 27: # ASCI ESCAPE = 27 
            # return nothing
            break

        if key == 13:# ASCI ENTER = 13
            # returns the captured frame
            value = frame
            break
    
    vid.release() # After the loop release the cap object 
    cv2.destroyWindow("Camera") # Destroy all the windows
    return value


def getBill() -> np.ndarray:
    '''to be written'''
    while True:
        img = _grabImage()
        if img is None: 
            return None
        cv2.imshow("Frame", img)
        cv2.waitKey(1)

        mask = _getMask(frame=img)
        corners = _cornerPoints(bw = mask)
        cv2.destroyWindow("Frame")
        if len(corners) != 4:
            messagebox.showerror("Error", "Bill not found!")
            continue

        bill = _transformImg(frame=img, corners=corners)
        cv2.imshow("Bill", bill)
        result = messagebox.askquestion("Ask for Result", "Are you satisfied with the result?")
        cv2.destroyWindow("Bill")
        if result == "yes": 
            # ask for rotation
            while result == "yes":
                result = messagebox.askquestion("Rotation?", "Rotation needed?")
                if result == "yes": bill = cv2.rotate(bill, cv2.ROTATE_90_CLOCKWISE)
                cv2.imshow("Bill", bill)
            cv2.destroyWindow("Bill")
            return bill
        if result == "no":
            continue



if __name__ == '__main__':

    import tkinter as tk

    root = tk.Tk()

    tk.Button(root, text="Get Bill", command=getBill).pack()

    root.mainloop()

