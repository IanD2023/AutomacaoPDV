import os

def instalarTkinter():
   
    tkinter=os.popen('dpkg -l | grep python3-tk').read().rstrip('\n')

    if tkinter != "":
            
            return True

    else:
    
        if os.system("apt install python3-tk -y") == 0:
        
            tkinter=os.popen('dpkg -l | grep python3-tk').read().rstrip('\n')

            if tkinter != "":
                return True
            else: return False

        else:
            
            if os.system("apt install python3-tk -s") == 0:
        
                tkinter=os.popen('dpkg -l | grep python3-tk').read().rstrip('\n')

                if tkinter != "":
                    return True
                else: return False  

def instalarPillow():
    
    if os.system("apt install python3-pil python3-pil.imagetk -y") == 0:
    
        tkinter=os.popen('dpkg -l | grep python3-pil.imagetk').read().rstrip('\n')

        if tkinter != "":
            return True
        else: return False

    else:
        
        if os.system("apt install python3-pil python3-pil.imagetk -s") == 0:
    
            tkinter=os.popen('dpkg -l | grep python3-pil.imagetk').read().rstrip('\n')

            if tkinter != "":
                return True
            else: return False 

def instalarscreenchot():

    if os.system('apt-get install gnome-screenshot -y') == 0:

        screenshot=os.popen('dpkg -l | grep -i gnome-screenshot').read().rstrip('\n')
        if screenshot != "": return True
        else: return False

    else:

        if os.system('apt-get install gnome-screenshot --force-yes') == 0:

            screenshot=os.popen('dpkg -l | grep -i gnome-screenshot').read().rstrip('\n')
            
            if screenshot != "": return True
            else: return False
            
if instalarTkinter() != True:

    print("Erro ao instalar Tkinter")   

if instalarPillow() != True:

    print("Erro ao instalar Pillow") 


if instalarscreenchot() != True:

    print("Erro ao instalar Screnshot") 