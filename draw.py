import cv2
import numpy as np

ix, iy, k = 200, 200, -1
def mouse(event, x, y, flags, param):
    global ix, iy, k
    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        k = 1
        

cv2.namedWindow("draw")
cv2.setMouseCallback("draw", mouse)

cap = cv2.VideoCapture(0)


while True:
    _, frm = cap.read()

    frm = cv2.flip(frm, 1)

    cv2.imshow("draw", frm)

    if cv2.waitKey(1) == 27 or k == 1:
        old_gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(frm)
        break

cv2.destroyAllWindows()

old_pts = np.array([[ix, iy]], dtype=np.float32).reshape(-1,1,2)

color = (0,255,0)
c=0
while True:

    _, new_frm = cap.read()

    new_frm = cv2.flip(new_frm, 1)

    new_gray = cv2.cvtColor(new_frm ,cv2.COLOR_BGR2GRAY)

    new_pts,status,err = cv2.calcOpticalFlowPyrLK(old_gray, 
                         new_gray, 
                         old_pts, 
                         None, maxLevel=1,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                                         15, 0.08))

    key = cv2.waitKey(1)

    if key == ord('e'):
        mask = np.zeros_like(new_frm)

    elif key == ord('c'):
        color = (0,0,0)
        lst = list(color)
        c+=1
        lst[c%3] = 255
        color = tuple(lst)

    elif key == ord('g'):
        pass
    else:
        for i, j in zip(old_pts, new_pts):
            x,y = j.ravel()
            a, b = i.ravel()

            cv2.line(mask, (a,b), (x, y), color, 15)

    cv2.circle(new_frm, (x,y), 3, (255,255,0), 2)


    
    new_frm = cv2.addWeighted(new_frm ,0.8, mask, 0.2, 0.1)

    cv2.imshow("", new_frm)
    cv2.imshow("drawing", mask)

    old_gray = new_gray.copy()

    old_pts = new_pts.reshape(-1,1,2)

    if key == 27:
        break


cv2.destroyAllWindows()
cap.release()
