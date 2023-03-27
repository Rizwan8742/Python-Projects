from tkinter import*
from PIL import Image,ImageTk
import requests
import api
class Mywheather():
    def __init__(self,root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("350x400+450+100")
        self.root.config(bg='sky blue')
        self.root.iconbitmap("icons/favicon.ico")
        #=====icons======
        self.search_icon = Image.open("icons/search.png")
        self.search_icon = self.search_icon.resize((15,15),Image.LANCZOS)
        self.search_icon = ImageTk.PhotoImage(self.search_icon)

        #====Varibale======
        self.var_search = StringVar()
        title = Label(self.root,text="Weather App",font=("goudy old style",30,"bold"),bg="#262626",fg='white').place(x=0,y=0,relwidth=1,height=60)

        lbl_city = Label(self.root,text="City Name",font=("Verdana",12),bg="#033958",fg='white',anchor="w",padx=5).place(x=0,y=60,relwidth=1,height=40)

        txt_city = Entry(self.root,textvariable=self.var_search,font=("goudy old style",15),bg="lightyellow",fg='#262626').place(x=102,y=68,width='200',height=25)

        btn_search = Button(self.root,cursor="hand2",image=self.search_icon,bg="#033958",activebackground="#033958",bd=0,command=self.get_latitude_longitude).place(x=310,y=68,width='30',height=25)

        #====Results====
        self.lbl_city = Label(self.root,font=("Verdana",12),bg='sky blue',fg='green')
        self.lbl_city.place(x=0,y=120,relwidth=1,height=20)

        self.lbl_icons = Label(self.root,font=("Verdana",12),bg='sky blue')
        self.lbl_icons.place(x=0,y=145,relwidth=1,height=100)

        self.lbl_temp = Label(self.root,font=("Verdana",12),bg='sky blue',fg='orange')
        self.lbl_temp.place(x=0,y=250,relwidth=1,height=20)

        self.lbl_wind = Label(self.root,font=("Verdana",12),bg='sky blue',fg='#262626')
        self.lbl_wind.place(x=0,y=275,relwidth=1,height=20)

        self.lbl_error =  Label(self.root,font=("Verdana",12),bg='sky blue',fg='red')
        self.lbl_error.place(x=0,y=295,relwidth=1,height=20)



        #======Footer=======

        lbl_footer = Label(self.root,text="Developed by Md Rizwan",font=("Verdana",12),bg="#033958",fg='white',pady=5).pack(side=BOTTOM,fill=X)

    def get_latitude_longitude(self):
        # city = self.var_search.get()

        #====validation====
        if self.var_search.get()=="":
            self.lbl_city.config(text="")
            self.lbl_icons.config(image="")
            self.lbl_temp.config(text="")
            self.lbl_wind.config(text="")

            self.lbl_error.config(text="City Name Required")
        else:
            city = self.var_search.get()
            api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}'.format(city)
            response = requests.get(api_url, headers={'X-Api-Key': 't7LjOk5yVoOP5vCEmWhdIVeYC8Wz2v2T4dWd1EME'})
            if response.status_code == requests.codes.ok:
                json = response.json()
                # print(response.text)
                for i in json:
                    if i['country'] == 'IN':
                        self.latitude = round(i['latitude'],2)  
                        self.longitude = round(i['longitude'],2)
                        print(self.latitude,self.longitude)
                        self.get_weather()
            else:
                print("Error:", response.status_code, response.text)


    def get_weather(self):
        api_key = api.api_key
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={api_key}"

        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            json = response.json()
            city_name = json["name"]
                
            country_name = json["sys"]["country"]
            icons = json["weather"][0]["icon"]
            temp_c = json["main"]["temp"] - 273.15
            temp_f = (json["main"]["temp"] - 273.15) * 9/5+32
            wind = json["weather"][0]["main"]

            self.lbl_city.config(text=city_name+" , "+country_name)
            #===new icons====
            self.icons = Image.open(f"icons/{icons}.png")
            self.icons = self.icons.resize((100,100),Image.LANCZOS)
            self.icons = ImageTk.PhotoImage(self.icons)

            self.lbl_icons.config(image=self.icons)

            deg = u"\N{DEGREE SIGN}"
            self.lbl_temp.config(text=str(round(temp_c,2))+deg+"C | "+str(round(temp_f,2))+deg+"F")
            self.lbl_wind.config(text=wind)
            # print(city_name,country,icons,temp_c,temp_f)
        else:
                self.lbl_city.config(text="")
                self.lbl_icons.config(text="")
                self.lbl_temp.config(text="")
                self.lbl_wind.config(text="")

                self.lbl_error.config(text="Invalid City Name")
                self
                
root = Tk()
obj = Mywheather(root)
root.mainloop() 