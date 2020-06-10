from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk,ImageDraw,ImageFont
import time
import os

def round_down(num):
	a=round(num)
	if(a>num):
		a-=1
	return a

def new_game(root):
	root.destroy()
	start_window()

def exit(root):
	root.destroy()
	os.remove("blank.png")
	os.remove("result.png")

def finish():
	global start
	stop=time.perf_counter()
	s=stop-start
	m=0
	if(s>60):
		m=round_down(s/60)
		s-=m*60
	s=round(s)
	global root, canvas,picture,myimg,start_picture
	start_picture.resize((320,320))
	Label(root, text="Time: "+str(m)+":"+str(s)).pack(anchor="ne")
	picture = ImageTk.PhotoImage(start_picture)
	canvas.itemconfigure(myimg, image=picture)
	Button(root, text="Next", command=lambda: new_game(root)).pack()
	Button(root, text="Exit", command=lambda: exit(root)).pack()

def change_color():
	global colors,cc,clr,len_color
	if(min(colors)==len_color):
		finish()
	if(int(clr.get()) not in colors):
		clr.set(min(colors))
	cc=int(clr.get())

def click(event):
	x,y=event.x,event.y
	global size,pix,cc,picture,original,canvas,myimg
	sx=round_down(x/size)*int(size)
	sy=round_down(y/size)*int(size)
	global hdns
	index=round_down(y/size)*hdns+round_down(x/size)
	img=Image.open("blank.png")
	if(cc==colors[index]):
		for i in range(sx,sx+int(size)+1,1):
			for j in range(sy,sy+int(size)+1,1):
				original.putpixel((i,j),pix[index])
		global len_color
		pix[index],colors[index]=len_color,len_color
		img.save("blank.png")
		picture = ImageTk.PhotoImage(original)
		canvas.itemconfigure(myimg, image=picture)
		change_color()

def game_start():
	global root
	root=Tk()
	img=Image.open("blank.png")
	global clr
	clr=StringVar()
	clr.set(0)
	global cc
	cc=0
	e=Entry(root,textvariable=clr).pack(anchor=NW)
	Button(root,text="change", command=lambda: change_color()).pack(anchor=NW)

	global picture,original,canvas,myimg
	canvas = Canvas(root, width = 340, height = 340)   
	canvas.bind("<Button-1>", click)    
	canvas.pack()
	original = Image.open("blank.png")
	picture = ImageTk.PhotoImage(original)
	myimg = canvas.create_image((0,0),image=picture, anchor="nw")
	global start
	start=time.perf_counter()
	root.mainloop()


def Open_img(i,root,v):
	global hdns,size
	hdns=v
	size=320/hdns
	global img,start_picture
	if(i==1):
		name=filedialog.askopenfile(parent=root,mode='rb',title='Choose a file',filetypes=[
    		("PNG", "*.png"),
    		("JPEG", "*.jpg"),
    		("All files", "*")])
		try:
			img = Image.open(name)
			start_picture=img
		except:
			print("Error :((")
	else:
		img=Image.open("pic.png")
		start_picture=img

	result = img.resize((v,v),resample=Image.BILINEAR)
	result.save('result.png')
	im=Image.open("result.png")
	global pix
	pix=[]
	for j in range(v):
		for i in range(v):
			pix.append(im.getpixel((i,j)))
	for i in range(len(pix)):
		for j in range(len(pix)):
			if(abs(pix[i][0]-pix[j][0])<=20 and abs(pix[i][1]-pix[j][1])<=20 and abs(pix[i][2]-pix[j][2])<=20):
				pix[j]=pix[i]
				break

	root.destroy()
	global colors
	colors=[]
	used_colors=[]
	for i in pix:
		if i in used_colors:
			colors.append(used_colors.index(i))
		else:
			used_colors.append(i)
			colors.append(len(used_colors)-1)
	global len_color
	len_color=len(used_colors)

	white = Image.new('RGB', (322, 322), (255, 255, 255)) 
	draw = ImageDraw.Draw(white) 
	for i in range(v+1):
		draw.line((i*(320/v),0, i*(320/v),320), fill="black")
		draw.line((0,i*(320/v),320, i*(320/v)), fill="black")
	c=0
	choose=lambda v:  {8: 15, 16: 10}.get(v, 5)
	font = ImageFont.truetype("arial.ttf", choose(v))
	for i in range(v):
		for j in range(v):
			draw.text((j*(320/v)+(320/v)/3-choose(v)/3,i*(320/v)+(320/v)/3-choose(v)/3),str(colors[c]),fill="black", font=font)
			c+=1
	white.save("blank.png")
	game_start()

def start_window():
	root=Tk()
	root.title("Color fill by Raya")
	root.geometry("300x250")
	img = ImageTk.PhotoImage(Image.open("logo.png"))
	panel = Label(root, image = img)
	panel.pack()
	v = IntVar()
	v.set(8)
	Radiobutton(root, text="Easy", variable=v, value=8).pack(anchor=W)
	Radiobutton(root, text="Medium", variable=v, value=16).pack(anchor=W)
	Radiobutton(root, text="Hard", variable=v, value=24).pack(anchor=W)
	Button(root,text="Browse file", command=lambda: Open_img(1,root,v.get())).pack()
	Button(root,text="Use default image", command=lambda: Open_img(0,root,v.get())).pack()
	root.mainloop()


start_window()