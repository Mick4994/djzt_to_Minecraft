import cv2
import numpy as np

block_name = []
for i in range(26):
    for j in range(26):
        for k in range(26):
            block_name.append('block'+str(i)+'_'+str(j)+'_'+str(k)+'.png')

texture_file = './texture/'

texture_list = []
for i in range(26):
    for j in range(26):
        for k in range(26):
            texture = np.array([[i*10,j*10,k*10] for s in range(4*4)],dtype=np.uint8)
            texture_list.append(np.reshape(texture,(4,4,3)))
            print('building:{:.2f}%'.format((i*26*26+j*26+k)/(26*26*26)*100),end='\r')
print('\n---------------------------------------------------------------------------')

for i in range(len(texture_list)):
    cv2.imwrite(texture_file + block_name[i], texture_list[i])
    print('saving:{:.2f}%'.format(i/(26*26*26)*100),end='\r')
print('\n')
            # cv2.imshow('img',texture_list[-1])
            # cv2.waitKey(1)
# cv2.destroyAllWindows()

# texture = np.array([[120,120,120] for s in range(64*64)],dtype=np.uint8)
# texture = np.reshape(texture,(64,64,3))
# img = texture
# print(img.shape)
# img = np.ones((256,256,3),dtype=np.uint8)
# img = img

# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()