from lab import modules_lab as mod # Here I have my lab modules
from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('coins.png')
pixels = img.load()

width, height = img.size

img2 = Image.new('L', (width,height), "black")
pixels2 = img2.load()

img3 = Image.new('L', (width,height), 'black')
pixels3 = img3.load()

# Converting from RGB to GS
mod.rgb_to_gs(pixels, pixels2, height, width)
#img2.show()

# Applying sobel masks that minimizes angle errors according to:
# "Procesamiento digital de imagenes con MATLAB y Simulink"
# ISBN: 978-607-707-030-6
sobelx = np.array([[-3.0,0.0,3.0]
				,[-10.0,0.0,10.0]
				,[-3.0,0.0,3.0]])
sobely = np.array([[-3.0,-10.0,-3.0]
					,[0.0,0.0,0.0]
					,[3.0,10.0,3.0]])
#begin, end = -1, 2
magnitudes = np.zeros((width,height), dtype = float)
angles = np.zeros((width,height), dtype = float)

for y in range(height): # Rows
	for x in range(width):	# Columns
		#filterx = 0.0
		#filtery = 0.0
		
		filterx, filtery = mod.apply_edge_mask(pixels2, height, 
		width, y, x, sobelx, sobely)
		
		'''
		for a in range(begin, end):
			for b in range(begin, end):
				# First row and first column
				if y == 0 and x == 0 and a >= 0 and b >= 0:
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])
				# First row and any column in between
				elif y == 0 and x > 0 and x < width and b >= 0 and (x + a) < width:	
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])
				# First row and last column
				elif y == 0 and x == width and a <= 0 and b >= 0:
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])
				# Any row in between and first column
				elif y > 0 and y < height and x == 0 and a >= 0 and (y + b) < height:
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])		
				# Any row in between any column in between
				elif y > 0 and y < height and x > 0 and x < width and (x + a) < width and (y + b) < height:
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])	
				# Any row in between and last column
				elif y > 0 and y < height and x == width and a <= 0:
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])
				# Last row and first column
				elif y == height and x == 0 and a >= 0 and b <= 0:
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])		
				# Last row and any column in between
				elif y == height and x > 0 and x <= width and b <= 0 and (x + a) < width:
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])	
				# Last row and last column
				elif y == height-1 and x == width-1 and a <= 0 and b <= 0:
					filterx += (pixels2[x+a,y+b] * sobelx[a+1,b+1])
					filtery += (pixels2[x+a,y+b] * sobely[a+1,b+1])
					'''
						
		Xpow = pow(filterx, 2)
		Ypow = pow(filtery, 2)
		magnitudes[x,y] = math.sqrt(Xpow + Ypow)
		angles[x,y] = math.atan2(filtery, filterx)
		if x == 0 and y == 0:
			min = magnitudes[x,y]
			max = magnitudes[x,y]
		else:
			if magnitudes[x,y] < min:
				min = magnitudes[x,y]
			
			if magnitudes[x,y] > max:
				max = magnitudes[x,y]
				

# Creating list for histogram
histogram = []
bins = 50.0
for x in range(int(bins)):
	# Storing bins and initializing counters ==>(bins, counters)
	if x == bins - 1:
		histogram.append([255, 0])
	else:
		histogram.append([(255 / bins)*(x + 1), 0])

# Normalizing magnitudes and counting the corresponding pixels
max_hist = 0
max2_hist = 0
for x in range(height):
	for y in range(width):
		pixels3[y,x] = (magnitudes[y,x] - min) * (255 / max)
		magnitudes[y,x] = pixels3[y,x]
		for z in range(int(bins)):
			if magnitudes[y,x] <= histogram[z][0]:
				histogram[z][1] += 1
				if histogram[z][1] > max_hist:
					max_hist = histogram[z][1]
				break

# Getting the second maximum value of bins			
for z in range(int(bins)):
	if histogram[z][1] > max2_hist and histogram[z][1] < max_hist:
		max2_hist = histogram[z][1]

img3.show()
#print histogram , max_hist , max2_hist

# Histogram	
for x in range(height):
	for y in range(width):
		for z in range(int(bins)):
			if max_hist > ((height * width) * 0.7):
				if magnitudes[y,x] >= histogram[z][0] and histogram[z][1] < (max2_hist * 0.20):
					pixels[y,x] = (255, 255, 0)
					break
			else:
				if histogram[z][1] < (max_hist * 0.20):
					if magnitudes[y,x] >= histogram[z][0]:
						#print histogram[z][1], max_hist*0.1
						pixels[y,x] = (0, 255, 255)
						break


# Plotting histogram
values = np.zeros(1,int)

for x in range(height):	#Rows
	for y in range(width):	#Columns
		values = np.insert(values,0,magnitudes[y,x])
		

n, bins, patches = plt.hist(values, 50, facecolor = 'g')
#plt.show()	



'''
# Plotting edges
print 'Choose cut limit:'
limit = int(raw_input('> '))

for x in range(height):
	for y in range(width):
		if magnitudes[y,x] > limit:
			pixels[y,x] = (0,255,0)
			
'''

img.show()
plt.show()
