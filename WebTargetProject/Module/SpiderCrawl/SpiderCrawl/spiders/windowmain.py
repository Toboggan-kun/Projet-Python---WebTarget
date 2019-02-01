# NOM DU PROJET         :       WEBTARGET
#
# AUTEURS               :
#                               STEPHANE KY
#                               CHALANA MENG
#                               CAROLINE TANG SONG
# CLASSE                :       3 SRC 3
# DATE                  :       11/01/2019
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkMessageBox

import crawler
from Tkinter import *
import os
from tkFileDialog import askopenfilename
import csv
from collections import namedtuple
import scrapy

isChecked1 = 0
isChecked2 = 0
global labelFrameCampagne
global labelFrameOptions
global labelNumberEmail
global listValidDomain
#global campagneNameValue
sendEmailFrame = ""
campagneNameValue = ""
labelNumberEmail = ""
sendEmailFrame = ""
entryDestination = ""
entrySource = ""
urlVal = ""
entryObject = ""
messageArea = ""
sendListEmailFrame = ""
listWithoutDouble = ""
newList = ""
emailsValue = []
cpt = 0 #VERIFIE SI LE LABEL NOM DE CAMPAGNE EST DEJA CREE
cpt2 = 0 #VERIFIE SI LE LABEL NOMBRE DE DESTINATAIRE EST DEJA CREE
cpt3 = 0 #VERIFIE SI LA LISTEBOX EXISTE DEJA OU NON (VERIFICATION DES MAILS VALIDES)
cpt4 = 0 #VERIFIE SI LA LISTEBOX EXISTE DEJA OU NON (VERIFICATION DES DOUBLONS)
cpt5 = 0 #VERIFIE SI LA LISTEBOX EXISTE DEJA OU NON (NEWLIST)
numberEmail = 0
listBox = ""
#MESSAGES D'ALTERTES
def errorMessagesDialog(message):
    tkMessageBox.showerror("Erreur", message)


def infoMessagesDialog(message):
    tkMessageBox.showinfo("Information", message)


def warningMessagesDialog(message):
    tkMessageBox.showwarning("Attention", message)
#MESSAGES D'ALERTES - FIN
#RENDRE DES COMPOSANTS VISIBLES OU NON
def hideComponent(component):
    component.pack_forget()

def showComponent(component, fill, padx, pady):
    component.pack(fill=fill, padx=padx, pady=pady)
#RENDRE DES COMPOSANTS VISIBLES OU NON - FIN

def campagneName(entryValue, createCampagneFrame, importOptionsFrame):
    global cpt
    global campagneNameValue
    #VERIFIE SI UN NOM DE CAMPAGNE A ETE INDIQUE
    #SI NON, AFFICHE UN MESSAGE D'ERREUR
    if len(entryValue.get()) == 0:
        errorMessagesDialog("Votre nom de campagne est vide.")

    #SINON ON AFFICHE L'ETAPE SUIVANTE
    else:
        hideComponent(createCampagneFrame)
        showComponent(importOptionsFrame, "both", 30, 0)
        value = entryCampagne.get()

        if cpt == 0:
            campagneNameValue = Label(window, text="Nom de campagne : " + value)
            campagneNameValue.pack()
            cpt += 1
        else:
            campagneNameValue.config(text="Nom de campgne : " + value)

def addURLDialog():
    global addURLWindow
    addURLWindow = Tk()
    addURLWindow.geometry("200x150")
    label = Label(addURLWindow, text="Veuillez saisir une URL : ")
    entryURL = Entry(addURLWindow)

    label.pack(side=TOP, pady=5)
    entryURL.pack(side=TOP, fill=X, padx=5, pady=5)
    global labelFrameMessage
    labelFrameMessage = LabelFrame(addURLWindow)
    global messageLabel
    messageLabel = Label(labelFrameMessage)
    labelFrameMessage.pack(fill=X, padx=5, pady=5)
    messageLabel.pack()

    buttonUndo = Button(addURLWindow, text="Annuler", command=lambda:addURLWindow.destroy())
    buttonValid = Button(addURLWindow, text="Valider", command=lambda:checkURL(entryURL, messageLabel))
    buttonUndo.pack(side=LEFT, padx=5, pady=5)
    buttonValid.pack(side=RIGHT, padx=5, pady=5)
    addURLWindow.mainloop()

def removeDouble(isChecked, isChecked2, listBox):

    global numberEmail
    global labelNumberEmail
    global cpt4
    global listValidDomain

    numberEmail = 0

    #global listBoth
    global listWithoutDouble

    #SI ON SOUHAITE ENLEVER LES DOUBLONS
    #ON ENREGISTRE LA LISTE INITIALE DANS UNE AUTRE LISTE ET ON RETIRE LES DOUBLONS
    if isChecked.get() == 1:
        hideComponent(listBox)
        if cpt4 == 0: #SI LA LISTE BOX N'EXISTE PAS

            listWithoutDouble = Listbox(labelFrameOptions)
            if isChecked2.get() == 1:
                hideComponent(listValidDomain)
                array = sorted(list(set(listValidDomain.get(0, END))))
            elif isChecked.get() == 1:
                try:
                    hideComponent(listValidDomain)
                except:
                    print "existe pas encore"
                array = sorted(list(set(listBox.get(0, END))))

            for data in array:
                listWithoutDouble.insert(END, data)

                numberEmail += 1

            #AFFICHE LA NOUVELLE LISTEBOX

            listWithoutDouble.pack(fill="both", padx=5, pady=10)
            labelNumberEmail.config(text="Nombre de destinataires : " + str(numberEmail))

            cpt4 += 1

            print listWithoutDouble.get(0, END)
        else: #SINON ON AFFICHE LA LISTBOX DEJA CREEE
            for data in sorted(list(set(listWithoutDouble.get(0, END)))):
                numberEmail += 1
            showComponent(listWithoutDouble, "both", 5, 10)
            labelNumberEmail.config(text="Nombre de destinataires : " + str(numberEmail))
    # SINON : ON REAFFICHE LE TABLEAU INITIAL
    elif isChecked.get() == 0 and isChecked2.get() == 1:
        hideComponent(listWithoutDouble)
        listValidDomain.delete(0, END)
        for data in list(listBox.get(0, END)):
            dataSplitted = data.split('@')
            toPing = dataSplitted[len(dataSplitted)-1]
            response = doPing(toPing)
            if response == 0:
                listValidDomain.insert(END, data)  # Recuperation de la derniere partie, apres le @
                numberEmail += 1
        labelNumberEmail.config(text="Nombre de destinataires : " + str(numberEmail))
        showComponent(listValidDomain, "both", 5, 10)
    else:

        hideComponent(listWithoutDouble)

        if isChecked2.get() == 1:
            showComponent(listValidDomain, "both", 5, 10)
            array1 = listBox.get(0, END)
        else:
            showComponent(listBox, "both", 5, 10)
            array1 = listValidDomain.get(0, END)
        for data in array1:
            numberEmail += 1
        labelNumberEmail.config(text="Nombre de destinataires : " + str(numberEmail))
def doPing(value):
    response = os.system("ping -w 5000 -n 1 " + value)
    return response
def checkIsValidMail(checked, checked2, listbox): #CETTE METHODE VA PINGER LE NOM DE DOMAINE DU MAIL
    global listWithoutDouble
    global numberEmail
    global labelNumberEmail
    global listBox
    global cpt3
    global listValidDomain
    print checked2.get()
    numberEmail = 0
    print listWithoutDouble
    if cpt3 == 0:
        listValidDomain = Listbox(labelFrameOptions)
        array = Listbox(labelFrameOptions)

    print checked.get()


    if checked.get() == 1: #EFFECTUE LE TRI DES MAILS VALIDES

        if checked2.get() == 1:
            array = list(listWithoutDouble.get(0, END))
            hideComponent(listWithoutDouble)
        else:
            array = list(listbox.get(0, END))
        for data in array:
            dataSplitted = data.split('@')
            toPing = dataSplitted[len(dataSplitted)-1]
            response = doPing(toPing)
            if response == 0:
                listValidDomain.insert(END, data)  # Recuperation de la derniere partie, apres le @
                numberEmail += 1

        labelNumberEmail.config(text="Nombre de destinataires : " + str(numberEmail))
        hideComponent(listBox)
        listValidDomain.pack(fill="both", padx=5, pady=10)
        cpt3 += 1
    elif checked.get() == 0 and checked2.get() == 1:
        hideComponent(listValidDomain)
        listWithoutDouble.delete(0, END)
        for data in sorted(list(set(listBox.get(0, END)))):
            listWithoutDouble.insert(END, data)
            numberEmail += 1
        showComponent(listWithoutDouble, "both", 5, 10)
    elif checked.get() == 0 and checked2.get() == 0:
        hideComponent(listValidDomain)
        showComponent(listBox, "both", 5, 10)
    else:

        hideComponent(listValidDomain)
        if checked.get() == 1:
            array1 = str(listBox)
            showComponent(listBox, "both", 5, 10)
        else:
            array1 = str(listValidDomain)
            showComponent(listValidDomain, "both", 5, 10)
        for data in array1:
            numberEmail += 1
        labelNumberEmail.config(text="Nombre de destinataires : " + str(numberEmail))


def addCSVValues(read, listBox):

    val = 0
    #listBox = Listbox(listBox)
    Header = namedtuple('Headers', 'EMails')
    listBox.delete(0, END)
    if read is not None:
        for data in map(Header._make, read):
            val += 1
            Listbox(listBox.insert(0, data.EMails))
    else:
        for data in listBox:

            val += 1
            listBox.insert(0, data)

    return val #RETOURNE LE NOMBRE D'EMAILS

def getUrl():
    global urlVal
    return urlVal


def checkURL(url, message):
    global urlVal
    urlVal = url.get()
    try:
        tmpUrl = re.search(r'(www\.)([\w]+\.?)\.[\w]+', url.get())
        data = tmpUrl.group(0)
    except:
        message.config(text="Verifiez l'orthographe de l'URL")
        message.config(fg="red")


    #tmpUrl = "http://www.thelin.net/laurent/labo/html/mailto.html"

    #PING L'URL
    response = doPing(data)

    #VERIFIE SI LE LABEL EXISTE DEJA POUR EVITER DE CREER DES DOUBLONS A CHAQUE LANCEMENT DE LA FONCTION
    if message.winfo_exists() != 1:
        message = Label(labelFrameMessage, text="Contact en cours avec" + url.get())
        message.pack(side=TOP, fill=X)

    #SI LE PING A FONCTIONNE : FERME LA FENETRE ET AFFICHE LES URLS TROUVEES
    if response == 0:

        path = os.getcwd()
        os.chdir(path + "\Module\SpiderCrawl\SpiderCrawl\spiders")
        os.system("scrapy crawl crawler")

        addURLWindow.destroy()
        listBox.delete(0, END)
        readCSVFile(listBox, 0, "test.csv")



    #SINON : AFFICHE UN MESSAGE D'ERREUR
    else:
        message.config(text="Impossible de contacter cet URL")
        message.config(fg="red")
    ifEmpty(listBox)
def nextStep(frame):
    global isChecked1, isChecked2, cpt5
    global sendEmailFrame
    global sendListEmailFrame
    global listBox
    global listWithoutDouble
    global listValidDomain
    global entryDestination
    global newList


    if isChecked1.get() == 1 and isChecked2.get() == 0:
        list = listWithoutDouble.get(0, END)

    elif isChecked1.get() == 0 and isChecked2.get() == 1:

        list = listValidDomain.get(0, END)

    elif isChecked1.get() == 1 and isChecked2.get() == 1:
        if listWithoutDouble.winfo_ismapped():
            list = listWithoutDouble.get(0, END)
        else:
            list = listValidDomain.get(0, END)
    else:
        list = listBox.get(0, END)

    if len(list) == 0: #SI LA LISTE EST VIDE
        errorMessagesDialog("Votre liste d'emails est vide.")
    else:

        hideComponent(frame)
        #showComponent(sendListEmailFrame, "both", 0, 0)
        #showComponent(sendEmailFrame, "both", 0, 0)
        sendEmailFrame.pack(side=RIGHT, fill="both", padx=5, expand=TRUE)
        sendListEmailFrame.pack(side=LEFT, fill=Y, padx=5)
        if cpt5 == 0:
            newList = Listbox(sendListEmailFrame)
            newList.pack(fill="both")
            for data in list:
                newList.insert(END, data)
            cpt5 += 1

        else:
            newList.delete(0, END)
            for data in list:
                newList.insert(END, data)






def readCSVFile(listBox, option, fileToRead):

    global read
    global cpt2
    global labelNumberEmail
    global numberEmail

    numberEmail = 0
    if option == 1:
        fileName = askopenfilename(initialdir="/", title="Choisir un fichier", filetypes=(("Fichiers CSV","*.csv"),("Tous les fichiers","*.*"))) #OUVRE L'EXPLORATEUR DE FICHIERS
        #SI RIEN N'EST CHOISI, AFFICHAGE D'UN MESSAGE D'INFORMATION
        if len(fileName) == 0:
            infoMessagesDialog("Vous n'avez pas choisi de fichier.")
    else:
        fileName = fileToRead

    #OUVRE LE FICHIER EN MODE LECTURE BINAIRE
    file = open(fileName, "rb")
    read = csv.reader(file, delimiter=",", quotechar="'")

    numberEmail = addCSVValues(read, listBox)

    if cpt2 == 0:
        labelNumberEmail = Label(window, text="Nombre de destinataires : " + str(numberEmail))
        labelNumberEmail.pack()
        cpt2 += 1
    else:
        labelNumberEmail.config(text="Nombre de destinataires : " + str(numberEmail))

    ifEmpty(listBox) #CHECK SI LA LISTE EST VIDE

def goToMainPage():
    hideComponent(labelFrameOptions)
    showComponent(labelFrameCampagne, "both", 30, 0)

def ifEmpty(listBox):

    if listBox.size() == 0:
        checkDouble.config(state=DISABLED)
        checkIsEmailValid.config(state=DISABLED)
    else:
        checkDouble.config(state=NORMAL)
        checkIsEmailValid.config(state=NORMAL)

def addEmailToEntry(list, entry):

    global emailsValue
    try:
        value = list.get(list.curselection())
    except:
        errorMessagesDialog("Vous n'avez pas selectione de valeur.")
    else:

        verify = value.split('@')
        verify = verify[len(verify) - 1]
        response = doPing(verify)
        if response != 0:
            errorMessagesDialog("Cet email est invalide ou reessayez.")
        else:
            entry.insert(END, value)
            entry.insert(END, ";")
            emailsValue.insert(0, value)
            print emailsValue


def sendEmail():


    global emailsValue
    global entrySource, entryObject, messageArea


    print emailsValue


    msg = MIMEMultipart()
    msg['From'] = entrySource.get()
    msg['To'] = '; '.join(emailsValue)
    msg['Subject'] = entryObject.get()
    msg.attach(MIMEText(messageArea.get("1.0", END)))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(entrySource.get(), 'Test?123')
    mailserver.sendmail(entrySource.get(), emailsValue, msg.as_string())
    mailserver.quit()

    infoMessagesDialog("Mail envoye ! ")



def returnToCampagneConfig():
    global sendListEmailFrame, sendEmailFrame, labelFrameOptions
    hideComponent(sendEmailFrame)
    hideComponent(sendListEmailFrame)
    showComponent(labelFrameOptions, "both", 0, 0)


class windowmain:
    global urlVal
    global sendListEmailFrame
    global sendEmailFrame
    global newList
    global entryDestination
    global entryObject, entrySource, messageArea


    #INITIALISATION DE LA FENETRE
    global window
    window = Tk()
    window.geometry("800x800")

    #TITRE PRINCIPAL
    title = Label(window, text="WebTarget")
    title.configure(font=('Calibri', 25, 'bold'))
    title.configure(height=2)
    title.pack(fill="both")

    campagneNameValue = ""
    labelCampagneName = Label(window, text=campagneNameValue)


    #1 - CREATION D'UN FICHIER DE CAMPAGNE
    global labelFrameCampagne

    labelFrameCampagne = LabelFrame(window, text="Creation d'une campagne", height=2)
    labelFrameCampagne.configure(font=('Calibri', 15))
    labelFrameCampagne.configure(height=2)
    labelFrameCampagne.pack(fill="both", padx=30)
    labelCreateCampagne = Label(labelFrameCampagne, text="Veuillez saisir un nom de campagne.")
    labelCreateCampagne.pack()
    global entryCampagne
    entryCampagne = Entry(labelFrameCampagne)
    entryCampagne.pack()


    labelCampagneName.pack()
    buttonCreateCampagne = Button(labelFrameCampagne, text="Valider", command=lambda:campagneName(entryCampagne, labelFrameCampagne, labelFrameOptions))
    buttonCreateCampagne.pack()

    # 1 - CREATION D'UN FICHIER DE CAMPAGNE FIN

    #2 - IMPORT D'EMAILS

    global labelFrameOptions

    labelFrameOptions = LabelFrame(window, text="Creation de votre liste de destinataires")
    labelFrameOptions.configure(font=('Calibri', 13))
    labelFrameOptions.pack(fill="both")
    labelFrameOptions.pack_forget()
    global listBox
    listBox = Listbox(labelFrameOptions)


    #CE LABEL VA SERVIR DE BOX POUR LES BOUTONS
    labelButtonBox = Label(labelFrameOptions)
    labelButtonBox.pack(fill=X, padx=0, pady=15)
    buttonImportCSV = Button(labelButtonBox, text="Importer des emails depuis un fichier CSV",
                             command=lambda: readCSVFile(listBox, 1, ""))
    buttonImportURL = Button(labelButtonBox, text="Importer depuis une URL", command=lambda: addURLDialog())
    buttonImportCSV.pack()
    buttonImportURL.pack()
    global isChecked1, isChecked2

    isChecked1 = IntVar()
    isChecked2 = IntVar()
    global checkDouble
    global checkIsEmailValid
    checkDouble = Checkbutton(labelButtonBox, text="Supprimer les doublons", variable=isChecked1, command=lambda:removeDouble(isChecked1, isChecked2, listBox))
    checkIsEmailValid = Checkbutton(labelButtonBox, text="Afficher les emails valides", variable=isChecked2, command=lambda:checkIsValidMail(isChecked2, isChecked1, listBox))

    ifEmpty(listBox)

    checkDouble.pack(side=BOTTOM)
    checkIsEmailValid.pack(side=BOTTOM)



    #PAGE ENVOI DE MAIL
    sendListEmailFrame = LabelFrame(window, text="Ma liste d'emails")
    sendListEmailFrame.configure(font=('Calibri', 13))


    sendEmailFrame = LabelFrame(window, text="Envoyer un email")
    sendEmailFrame.configure(font=('Calibri', 13))


    labelDestination = Label(sendEmailFrame, text="Destinataire(s)")
    entryDestination = Entry(sendEmailFrame)
    labelSource = Label(sendEmailFrame, text="Expediteur")
    entrySource = Entry(sendEmailFrame)
    entrySource.insert(0, "src3esgi@gmail.com")
    entrySource.config(state="disabled")
    labelObject = Label(sendEmailFrame, text="Objet")
    entryObject = Entry(sendEmailFrame)
    labelMessage = Label(sendEmailFrame, text="Message")
    messageArea = Text(sendEmailFrame)
    #buttonSend = Button(sendEmailFrame, text="Envoyer", command=lambda : sendEmail(entrySource.get(), entryObject.get(), messageArea.get()))

    buttonSend = Button(sendEmailFrame, text="Envoyer",
                        command=lambda: sendEmail())
    buttonAdd = Button(sendListEmailFrame, text="Ajouter", command=lambda:addEmailToEntry(newList, entryDestination))
    returnButton = Button(sendListEmailFrame, text="< Retour", command=lambda :returnToCampagneConfig())
    buttonAdd.pack()
    returnButton.pack()


    labelDestination.pack()
    entryDestination.pack(fill=X, padx=10)
    labelSource.pack()
    entrySource.pack(fill=X, padx=10)
    labelObject.pack()
    entryObject.pack(fill=X, padx=10)
    labelMessage.pack()
    messageArea.pack(fill=X, padx=10, expand=FALSE)
    buttonSend.pack(side=RIGHT, padx=10)

    buttonUndo = Button(labelFrameOptions, text="< Retour", command=lambda: goToMainPage())
    buttonContinue = Button(labelFrameOptions, text="Continuer >", command=lambda : nextStep(labelFrameOptions))

    buttonUndo.pack(side=LEFT)
    buttonContinue.pack(side=RIGHT)




    listBox.pack(fill="both", padx=5, pady=10)


    # 2 - IMPORT D'EMAILS FIN


    window.mainloop()


