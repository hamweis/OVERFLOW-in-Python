import tkinter as tk
import time
from itertools import cycle
from tkinter import messagebox as mb

buttonliste={}
spielfeld={}
playerlist=["red", "yellow"]
playercycle=cycle(playerlist)

def createButtons(window):
    for i in range(0,100):
        buttonliste[i]=button = tk.Button(window, text=0, font=("Arial", 20), bg="black")
        buttonliste[i].grid(row=i//10, column=i%10)
        buttonliste[i].config(command= lambda b=buttonliste[i]:buttonPress(b))

#erstmal nicht benutzt
def createScore(window):
    scorep1=tk.Label(text=0, font=("Roboto",10))
    scorep2=tk.Label(text=0, font=("Roboto",10))
    scorep1.grid(row=10, column=0)
    scorep2.grid(row=10, column=9)



def createSpielfeld(size):
    feldindex=0
    for i in range(size):
        for j in range(size):
            spielfeld[feldindex]=0
            feldindex+=1

def nextPlayer():
      return next(playercycle)
aktuellerSpieler=str(nextPlayer()) # startspieler festlegen

def labelPlayerTurn():
    match aktuellerSpieler: 
        case "red":
                playerTurn=tk.Label(text="r", font=("Roboto",10))
        case "yellow":
                playerTurn=tk.Label(text="y", font=("Roboto",10))
    playerTurn.grid(row=10, column=0)

def buttonPress(button):

    #buttonindex ableiten
    indexBtnclicked=str(button).strip(".!button" )                #button gibt eine repräsentation von button als str aus - hier schneide ich alles außer der Zahl am Ende des Strings ab
    indexBtnclicked=((int(indexBtnclicked) if indexBtnclicked!="" else 1)-1)    #der allererste button hat leider keine zahl, also wird hier vorm printen gecheckt, ob der string nicht leer ist, sonst soll er eine 1 printen (das ganze wird mit 1 subtrahiert, um mit der indizierung der listen übereinzustimmen)
    
    global aktuellerSpieler                                     #'importiere' ersten spieler
    
    print(f"{aktuellerSpieler} hat den {indexBtnclicked}. Knopf gedrückt")                          #test
    
    #----------------------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------
    #spiellogik             
    if buttonliste[indexBtnclicked].cget("bg")==aktuellerSpieler or buttonliste[indexBtnclicked].cget("bg")=="black":           #wenn spieler auf falsches feld geklickt hat passiert garnichts
        spielfeld[indexBtnclicked]+=1                                                                                           #erst wird spielfeld im Hintergrund erhöht
        
        
        #drawOrspread(indexBtnclicked, aktuellerSpieler, indexBtnclicked)                                                        #parentind wird nicht mehr gemalt
        #drawOrspreadNEU(indexBtnclicked, aktuellerSpieler, indexBtnclicked)                                                     #ausstieg aus rekursion, aber dadurch Felder mit Value>countnachbarn möglich
        drawOrspreadNEUNEU(indexBtnclicked, aktuellerSpieler, indexBtnclicked)                                                  #ausstieg aus rekursion funktioniert, aber am ende trotzdem maximum recursion depth exceeded



        aktuellerSpieler=str(nextPlayer())  # cycled durch die spieler farbe
    labelPlayerTurn()                                                                                                           #ändert das Label, das den nächsten Spieler anzeigt
    
    #----------------------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------

    #test
    print(countNachbarn(indexBtnclicked))
    print(spielfeld[indexBtnclicked])
    print(indexNachbarn(indexBtnclicked))
    print("--------------------------------------------")
    


def drawOrspreadNEUNEU(indtocheck, farbe, parentind):                                                                  #gibt maximum recursion depth exceeded
        
        if spielfeld[indtocheck]!=countNachbarn(indtocheck):                                                    #True -> Draw            weiter-> in buttonPress -> nächster spieler
             drawButton(indtocheck, farbe)
        
        elif spielfeld[indtocheck]>=countNachbarn(indtocheck):                                                  #True -> Spread
            
            spielfeld[indtocheck]=0
            drawButton(indtocheck, "black")
            
            print(f"müsste spreaden: {indtocheck}")                                                            #test
            print(f"vorher gecheckt: {parentind}")                                                              #test
            
            for i in indexNachbarn(indtocheck):
                #parentind=indtocheck                                                #wenn unten bei drawOrspread nur Draw rauskommt- ist der parentind quasi egal - nur wenn eine tiefere rekursionsebene erreicht wird, kommt der parentind zum einsatz 
                if i!=parentind:
                    
                    print(f"checke {i}")
                    spielfeld[i]+=1
                    
                    
                    drawOrspreadNEUNEU(i, farbe, parentind=indtocheck)                          #hier passiert entweder rekursion oder der neue Knopf wird nur gemalt     
                else:
                    spielfeld[i]+=1
                    if spielfeld[i]>=countNachbarn(i):
                        drawOrspreadNEUNEU(i, farbe, parentind=indtocheck)
                    elif spielfeld[indtocheck]!=countNachbarn(indtocheck):
                        drawButton(i, farbe)

def drawOrspreadNEU(indtocheck, farbe, parentind):                                                                  #gibt maximum recursion depth exceeded
        
        if spielfeld[indtocheck]!=countNachbarn(indtocheck):                                                    #True -> Draw            weiter-> in buttonPress -> nächster spieler
             drawButton(indtocheck, farbe)
        
        elif spielfeld[indtocheck]>=countNachbarn(indtocheck):                                                  #True -> Spread
            
            spielfeld[indtocheck]=0
            drawButton(indtocheck, "black")
            
            print(f"müsste spreaden: {indtocheck}")                                                            #test
            print(f"vorher gecheckt: {parentind}")                                                              #test
            
            for i in indexNachbarn(indtocheck):
                #parentind=indtocheck                                                #wenn unten bei drawOrspread nur Draw rauskommt- ist der parentind quasi egal - nur wenn eine tiefere rekursionsebene erreicht wird, kommt der parentind zum einsatz 
                if i!=parentind:
                    
                    print(f"checke {i}")
                    spielfeld[i]+=1
                    
                    
                    drawOrspreadNEU(i, farbe, parentind=indtocheck)                          #hier passiert entweder rekursion oder der neue Knopf wird nur gemalt     
                else:
                    spielfeld[i]+=1
                    drawButton(i, farbe)

def drawOrspread(indtocheck, farbe, parentind):                                                                  #gibt maximum recursion depth exceeded
        
        if spielfeld[indtocheck]!=countNachbarn(indtocheck):                                                    #True -> Draw            weiter-> in buttonPress -> nächster spieler
             drawButton(indtocheck, farbe)
        
        elif spielfeld[indtocheck]>=countNachbarn(indtocheck):                                                  #True -> Spread
            
            spielfeld[indtocheck]=0
            drawButton(indtocheck, "black")
            
            print(f"müsste spreaden: {indtocheck}")                                                            #test
            print(f"vorher gecheckt: {parentind}")                                                              #test
            
            for i in indexNachbarn(indtocheck):
                #parentind=indtocheck                                                #wenn unten bei drawOrspread nur Draw rauskommt- ist der parentind quasi egal - nur wenn eine tiefere rekursionsebene erreicht wird, kommt der parentind zum einsatz 
                if i!=parentind:
                    
                    print(f"checke {i}")
                    spielfeld[i]+=1
                    
                    
                    drawOrspread(i, farbe, parentind=indtocheck)                          #hier passiert entweder rekursion oder der neue Knopf wird nur gemalt     
                else: pass
                    #spielfeld[i]+=1
                    #drawButton(i, farbe)

def drawButton(indexbtn, farbe):                                                                                #malt nur noch einen Knopf
    buttonliste[indexbtn].config(text=spielfeld[indexbtn],bg=farbe)                                                                             #TODO wäre cool, wenn man kurz die maximale Zahl mit der ursprungsfarbe sehen könnte                   


def countNachbarn(buttonindex):
        countnachbarn=4
        zeile=buttonindex//10
        spalte=buttonindex%10
        if zeile==0 or zeile==9: countnachbarn-=1
        if spalte==0 or spalte==9: countnachbarn-=1
        return countnachbarn

def indexNachbarn(buttonindex):
        #indNachbarn=[self.index-10 if not self.zeile==0 else None, self.index+10 if not self.zeile==9 else None,self.index-1 if not self.spalte==0 else None,self.index+1 if not self.spalte==9 else None ] # charmanterer One-Liner, aber er fügt werte hinzu, die dann wieder gelöscht werden müssten
        indNachbarn=[]
        zeile=buttonindex//10
        spalte=buttonindex%10
        if not zeile==0: # erster wert der liste ist index des Nachbarn oben, WENN sich das Spielfeld nicht in der nullten Zeile befindet
                indNachbarn.append(buttonindex-10)
        if not zeile==9: # zweiter wert ist index des Nachbarn unter, WENN sich das Spielfeld nicht in der letzten Zeile befindet
                indNachbarn.append(buttonindex+10)
        if not spalte==0:# dritter wert ist index des Nachbarn Links, WENN sich das Spielfeld nicht in der nullten Spalte  befindet
                indNachbarn.append(buttonindex-1)
        if not spalte==9: # vierter wert ist index des Nachbarn Rechts, WENN sich das Spielfeld nicht in der letzten Spalte  befindet
                indNachbarn.append(buttonindex+1)
        return indNachbarn

if __name__=="__main__":   
    main_window=tk.Tk()
    main_window.resizable(False,False)
    main_window.title("Overflow 0.2")

    #spielelemente erzeugen
    
    labelPlayerTurn()
    createSpielfeld(10)
    createButtons(main_window)
    
    #grundlogik muss noch erkennen, ob spiel schon gameover
    #dann: show message 

    main_window.mainloop()
