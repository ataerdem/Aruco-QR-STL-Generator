import Part
from FreeCAD import Vector
from xml.dom import minidom

def generate_aruco(base_thickness, cut_thickness, aruco_dir, stl_size, checkerboard_back=True, checkerboard_thickness=1, checkerboard_size=(10,10)):
	"""

	Creates two plates given a valid black and white svg. Works with https://chev.me/arucogen/. The purpose is to make it easier to 3d print qr codes and aruco markers. The function does NOT handle incorrectly formatted svgs and may produce unexpected results.

	Parameters:
	base_thickness (float): Thickness of the white base
	cut_thickness (float): Thickness of the black plate
	aruco_dir (str): The directory of the svg that represents the image
	stl_size (tuple): The size of the resulting object in milimeters (width, height)
	checkerboard_back (bool): Crates a checkerboard pattern at the back when True. True by default. Might be useful for 3d printing.
	checkerboard_thickness (float): The depth of the checkerboard pattern
	checkerboard_size (tuple): Number of squares on the checkerboard pattern (width, height)

	Returns:
	None

	"""
	aruco_parsed = minidom.parse(aruco_dir)

	svg = aruco_parsed.getElementsByTagName("svg")[0]
	svg_width, svg_height = svg.getAttribute("viewBox").split()[-2:]
	stl_size = (float(svg.getAttribute("width")[:-2]), float(svg.getAttribute("height")[:-2]))
	scale = (stl_size[0]/float(svg_width), stl_size[1]/float(svg_height))

	white_plate = Part.makeBox(stl_size[0],stl_size[1],base_thickness,Vector(0,0,cut_thickness))
	base_plate = Part.makeBox(stl_size[0],stl_size[1],cut_thickness,Vector(0,0,0))
	
	attributes = ["x", "y", "width", "height", "fill"]
	for rect in svg.getElementsByTagName("rect"):
		x,y,width,height,color = (rect.getAttribute(att) for att in attributes)
		if color == "black": continue
		to_cut = Part.makeBox(float(width)*scale[0],float(height)*scale[1],cut_thickness,Vector(float(x)*scale[0],float(y)*scale[1],0))
		base_plate = base_plate.cut(to_cut)
	
	if checkerboard_back:

		num_rects = checkerboard_size
		rect_width, rect_height = (stl_size[0]/num_rects[0], stl_size[1]/num_rects[1])
		for i in range(num_rects[0]):
			for j in range(num_rects[1]):
				if (i+j)%2 == 0 : continue
				to_cut = Part.makeBox(rect_width,rect_height,checkerboard_thickness,Vector(rect_width*i,rect_height*j,base_thickness+cut_thickness-checkerboard_thickness))
				white_plate = white_plate.cut(to_cut)

	Part.show(base_plate)
	Part.show(white_plate)

if __name__ == "__main__":
	aruco_dir = input("Image dir: \n")

	width, height = float(input("Width: \n")), float(input("Height: \n"))
	stl_size = (width, height) #mm width, height
	white_thickness = float(input("White thickness: \n")) #mm
	black_thickness = float(input("Black thickness: \n"))
	checkerboard = True if input("Use checkerboard? (y/n): \n") == "y" else False
	if checkerboard:
		checkerboard_thickness = float(input("Checkerboard thickness: \n"))
	else:
		checkerboard_thickness = 0

	generate_aruco(white_thickness, black_thickness, aruco_dir, stl_size, checkerboard, checkerboard_thickness)
