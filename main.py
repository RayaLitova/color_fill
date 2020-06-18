from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk,ImageDraw,ImageFont
import time
import os
import random
import json
from getmac import get_mac_address as gma

default_best={"Mac":gma(),"Easy (8x8)": None, "Medium (8x8)": None, "Hard (8x8)": None, "Easy (16x16)": None, "Medium (16x16)": None, "Hard (16x16)": None}

try: 
	f=open("time.json","x")
	f.write(json.dumps(default_best))
	f.close()
except:
	bests=json.loads(open("time.json","r+").read())
	if(gma()!=bests["Mac"]):
		f.seek(0)
		f.write(json.dumps(bests))

f=open("time.json","r+")
bests=json.loads(f.read())
if(gma()!=bests["Mac"]):
	f.seek(0)
	f.write(json.dumps(default_best))
f.close()
keys=list(bests.keys())

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

def save():
	f=open("time.json",'w')
	f.write(json.dumps(bests))
	f.close()

def finish():
	global start
	stop=time.perf_counter()
	s=stop-start
	global v,hdns
	txt="Time: "
	a=lambda v: {1: "Easy", 2: "Medium"}.get(v, "Hard")
	if(bests[a(v.get())+" ({}x{})".format(hdns,hdns)]==None):
		bests[a(v.get())+" ({}x{})".format(hdns,hdns)]=round(s)
		save()
		txt="New Best Time: "
	if(bests[a(v.get())+" ({}x{})".format(hdns,hdns)]>s):
		bests[a(v.get())+" ({}x{})".format(hdns,hdns)]=round(s)
		save()
		txt="New Best Time: "

	m=0
	if(s>60):
		m=round_down(s/60)
		s-=m*60
	s=round(s)
	global root, canvas,picture,myimg,start_picture
	start_picture.resize((320,320))
	Label(root, text=txt+str(m)+":"+str(s)).pack(anchor="ne")
	picture = ImageTk.PhotoImage(start_picture)
	canvas.itemconfigure(myimg, image=picture)
	Button(root, text="Next", command=lambda: new_game(root)).pack()
	Button(root, text="Exit", command=lambda: exit(root)).pack()

def change_color(event):
	global colors,cc,clr,len_color,v
	if(min(colors)==len_color):
		finish()
	elif(int(clr.get()) not in colors and v.get()!=3):
		clr.set(min(colors))
	elif(v.get()==3):
		r=(random.choice(colors))
		while(r==len_color):
			r=(random.choice(colors))
		clr.set(r)

	cc=int(clr.get())

def click(event):
	x,y=event.x,event.y
	global size,pix,cc,picture,original,canvas,myimg,len_color
	sx=round_down(x/size)*int(size)
	sy=round_down(y/size)*int(size)
	global hdns
	index=round_down(y/size)*hdns+round_down(x/size)
	img=Image.open("blank.png")
	if(cc==colors[index] and colors[index]!=len_color):
		for i in range(sx,sx+int(size)+1,1):
			for j in range(sy,sy+int(size)+1,1):
				original.putpixel((i,j),pix[index])
		pix[index],colors[index]=len_color,len_color
		img.save("blank.png")
		picture = ImageTk.PhotoImage(original)
		canvas.itemconfigure(myimg, image=picture)
		change_color(1)

def game_start():
	global root
	root=Tk()
	img=Image.open("blank.png")
	global clr
	clr=StringVar()
	clr.set(0)
	global cc
	cc=0
	global v
	if(v.get()!=3):
		e=Entry(root,textvariable=clr).pack(anchor=W)
		Button(root,text="<Enter>", command=lambda: change_color(1)).pack(anchor=W)
	else:
		Label(root, textvariable=clr,font=("Ariel",20)).pack(anchor=W)
		Label(root,text="Press <Enter> to change color").pack(anchor=W)

	root.bind('<Return>', change_color)
	global picture,original,canvas,myimg
	canvas = Canvas(root, width = 340, height = 340)   
	canvas.bind("<Button-1>", click)    
	canvas.pack()
	original = Image.open("blank.png")
	picture = ImageTk.PhotoImage(original)
	myimg = canvas.create_image((0,0),image=picture, anchor="nw")
	Button(root, text="Cancel", command=lambda: new_game(root)).pack(side="top", anchor=E)
	global start
	start=time.perf_counter()
	root.mainloop()


def Open_img(i,root,s):
	global hdns,size
	hdns=s.get()
	size=320/hdns
	global img,start_picture
	if(i==1):
		name=filedialog.askopenfile(parent=root,mode='rb',title='Choose a file',filetypes=[
    		("PNG", "*.png"),
    		("JPEG", "*.jpg")])
		try:
			img = Image.open(name)
			start_picture=img
		except:
			print("Error :((")
	else:
		img=Image.open("pic.png")
		start_picture=img

	result = img.resize((hdns,hdns),resample=Image.BILINEAR)
	result.save('result.png')
	im=Image.open("result.png")
	global pix
	pix=[]
	for j in range(hdns):
		for i in range(hdns):
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
	global v
	if(v.get()!=1):
		d={}
		for i in range(len(used_colors)):
			r=random.randint(0,len_color-1)
			while r in d.values():
				r=random.randint(0,len_color-1)
			d.update( {i : r} )

		colors=([d.get(n, n) for n in colors])

	white = Image.new('RGB', (322, 322), (255, 255, 255)) 
	draw = ImageDraw.Draw(white) 
	for i in range(hdns+1):
		draw.line((i*(size),0, i*(size),320), fill="black")
		draw.line((0,i*(size),320, i*(size)), fill="black")
	c=0
	choose=lambda hdns:  {8: 15, 16: 10}.get(hdns, 5)
	font = ImageFont.truetype("arial.ttf", choose(hdns))
	for i in range(hdns):
		for j in range(hdns):
			draw.text((j*(320/hdns)+(320/hdns)/3-choose(hdns)/3,i*(320/hdns)+(320/hdns)/3-choose(hdns)/3),str(colors[c]),fill="black", font=font)
			c+=1
	white.save("blank.png")
	game_start()

def start_window():
	root=Tk()
	root.title("Color fill by Raya")
	root.geometry("300x520")
	img = ImageTk.PhotoImage(Image.open("logo.png"))
	Label(root,text="").pack()
	panel = Label(root, image = img)
	panel.pack()
	Label(root,text="\nBests: ",font=("Ariel", 15)).pack()
	for i in range(len(keys)-1):
		Label(root,text=str(keys[i+1])+": "+str(bests[keys[i+1]])+" sec").pack()
	s=IntVar()
	s.set(8)
	Label(root,text="Tile size:").pack(anchor=W)
	Radiobutton(root, text="8x8", variable=s, value=8).pack(anchor=W)
	Radiobutton(root, text="16x16", variable=s, value=16).pack(anchor=W)
	global v
	v = IntVar()
	v.set(1)
	Label(root,text="Difficulty:").pack(anchor=W)
	Radiobutton(root, text="Easy", variable=v, value=1).pack(anchor=W)
	Radiobutton(root, text="Medium", variable=v, value=2).pack(anchor=W)
	Radiobutton(root, text="Hard", variable=v, value=3).pack(anchor=W)
	Button(root,text="Browse file", command=lambda: Open_img(1,root,s)).pack()
	Button(root,text="Use default image", command=lambda: Open_img(0,root,s)).pack()
	root.mainloop()


start_window()