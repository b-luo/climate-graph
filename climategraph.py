import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Some simple climate models -- Bryan Luo")


#constants and global variables:
##################################
#range of time in years from 1900 to 2300
t=np.arange(1900,2300,1)
#amount to be eventually extracted, quantity in trillions
q1,q2,q3=1.5,2,15

#amount of skewing or error
n1,n2,n3=1.05,2.826,7.125

#time/year at which resource is half depleted
x1,x2,x3=2061,2005,2056

#rising exponential time constant
tau1,tau2,tau3=43.43,13.37,13.97

################################

def rdepl(q,n,t,x,tau):
        return (q*(10**12)*((2**n)-1)*
                np.exp((t-x)/tau))/(n*tau*(1+(2**n-1)*
                                           np.exp((t-x)/tau))**((n+1)/n))


def draw_fuel_extraction():
    a =f.add_subplot(111,xlabel='Year',title='Global Fuel Extraction')
    '''plt.subplot(1,1,1)
    plt.xlabel('Year')
    plt.title('Global Fossil Fuel Extraction')'''

    #Global Coal Extraction
    line1,=a.plot(t,rdepl(q1,n1,t,x1,tau1),'b-')

    #Global oil Extraction
    line2,=a.plot(t,rdepl(q2,n2,t,x2,tau2),'gx')

    #Global Natural Gas Extraction
    line3,=a.plot(t,rdepl(q2,n3,t,x3,tau3),'r--')

    #plt.legend([line1,line2,line3],['Coal in millions of short tons','Crude oil in billions of barrels','Natural gas in trillions of cubic feet'])
    
    f.legend([line1,line2,line3],['Coal in millions of short tons','Crude oil in billions of barrels',
                                  'Natural gas in trillions of cubic feet'],loc='center right')


#figure 2 shows the emission of carbon into the atmosphere
def draw_carbon_emission():
    '''plt.subplot()
    plt.xlabel('Year')
    plt.ylabel('Carbon emitted in billions of tons')
    plt.title('Carbon emissions due to Fossil Fuels Burning')'''
    
    a = f.add_subplot(111,xlabel='Year',title='Carbon emissions (in billions of tons) by burning fossil fuels')

    def ecoal(t):
        return 0.907*0.5*0.75*rdepl(q1,n1,t,x1,tau1)
    
    line1,=a.plot(t,ecoal(t),'b-',label='Emissions by coal')

    def eoil(t):
        return 0.136*0.84*0.75*rdepl(q2,n2,t,x2,tau2)
    
    line2,=a.plot(t,eoil(t),'gx',label='Emissions by crude oil')

    def egas(t):
        return 0.0189*0.76*0.75*rdepl(q3,n3,t,x3,tau3)
    
    line3,=a.plot(t,egas(t),'r--', label='Emissions by natural gas')
    f.legend([line1,line2,line3],['Emissions by coal','Emissions by crude oil','Emissions by natural gas'],loc='center right')

    #ffuel shows carbon emissions by all fossil fuels
    def ffuel(t):
        return ecoal(t)+eoil(t)+egas(t)


def draw_tmperature():
    #temperature function
    def tempGrowth(s,c0,c):
        return temp0+s*np.log2(c/c0)

    #original temperature in Celsius
    temp0 = 14.3

    #original carbon emission in ppm
    c0 = 368

    #climate sensitivity factor
    s1,s2,s3 = 2, 3, 4


    # evenly sampled carbon emission from 368 to 4*368 = 1472
    c = np.arange(368,1472, 1)
    '''plt.subplot()
    plt.ylabel('Temperature--degrees Celsius')
    plt.xlabel('Carbon Emission--ppm')'''

    # red dashes, blue solid line and green -.
    #plt.title('Temperature Change Caused by emission')
    #plt.text(350,20,r'$T=T_0+Slog_2(C/C0)$')
    a = f.add_subplot(111,xlabel='Carbon Emissions--ppm',ylabel='Temperature in degrees Celsius')

    line1,=a.plot(c, tempGrowth(s1,c0,c), 'r--')
    line2,=a.plot(c, tempGrowth(s2,c0,c), 'b-')
    line3,=a.plot(c, tempGrowth(s3,c0,c), 'g-.')
    f.legend([line1,line2,line3],['Climate sensitivity factor(s) s=2','s=3', 's=4'])

    #plt.subplots_adjust(left=None, bottom=None,  top=None, hspace=1)

    #plt.show()


def draw():
    canvas.figure.clf()
    show = rbVar.get()
    if show == 1:
        draw_fuel_extraction()
    elif show == 2:
        draw_carbon_emission()
    elif show == 3:
        draw_tmperature()
    canvas.show()
 
    
###############
#the figure area
f = Figure(figsize=(9,6), dpi=100)
canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().grid(row=0, rowspan=20, column=2)

#the gui layout
rbVar = Tk.IntVar()
rbtn1 = Tk.Radiobutton(root,text='Fuel Extraction',variable=rbVar,value=1).grid(row=0,sticky='w')
rbtn2 = Tk.Radiobutton(root,text='Carbon Emissions',variable=rbVar,value=2).grid(row=1,sticky='w')
rbtn3 = Tk.Radiobutton(root,text='Temperature',variable=rbVar,value=3).grid(row=2,sticky='w')

button = Tk.Button(root,text='Draw',command=draw).grid(row=3,sticky='w')

toolbar_frame = Tk.Frame(root)
toolbar_frame.grid(row=21,column=2)
toolbar = NavigationToolbar2TkAgg( canvas, toolbar_frame )
toolbar.update()

def on_key_event(event):
    print('you pressed %s'%event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)

def _quit():
    root.quit()     # stops main loop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=root, text='Quit', command=_quit)
button.grid(row=4, sticky='w')

Tk.mainloop()
##########

