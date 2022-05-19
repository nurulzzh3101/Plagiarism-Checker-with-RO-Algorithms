#!/usr/bin/env python
# IMPORT MODULE 
import mysql.connector 
import nltk
import string
import re
from nltk import word_tokenize
import numpy as np
from nltk.stem import PorterStemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from functools import reduce
import cv2,os
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font 
import cgitb 
from nltk.corpus import stopwords


# CONNECT TO DATABASE
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cek_plagiat"
)



# MEMBUAT CLASS TKINKER SampleApp SEBAGAI PEMBUNGKUS TAMPILAN
class SampleApp(tk.Tk):
    
    # fungsi untuk membungkus tampilan dalam 1 Tkinter
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Cek Plagiarisme Berita")
        self.geometry('1920x2160')
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Main_Page, View_Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Main_Page")

    # FUNGSI UNTUK MENAMPILKAN HALAMAN YANG DIPANGGIL
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()




# MEMBUAT CLASS Input_Page SEBAGAI HALAMAN PERTAMA DAN INPUT DATA TEKS
# MENYIMPAN INPUT DATA TEKS KE DATABASE 
class Main_Page(tk.Frame):

    # fungsi untuk membungkus tampilan dalam 1 Tkinter
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="AliceBlue")
        
        # fungsi hapus (untuk hapus teks1)
        def clear():
            dataset1.delete("1.0", 'end')

        # fungsi hapus (untuk hapus teks1,teks2)
        def clear_allTeks():
            dataset1.delete("1.0", 'end')
            dataset2.delete("1.0", 'end')
            
        
        # fungsi hapus (untuk hapus teks2)
        def clear2():
            dataset2.delete("1.0", 'end')
        
        def clear_allData():
            dataset1.delete("1.0", 'end')
            dataset2.delete("1.0", 'end')
            box_totalKataSama.config(text="")
            box_totalCharTeks.config(text="")
            box_totalCharSama.config(text="")
            box_persen.config(text="")
            box_klasif.config(text="")
            sql = "DELETE FROM data_input_ambil"
            cursor = db.cursor(buffered=True)
            cursor.execute(sql)
        
        
        
        # membuat tampilan (content halaman Input_Page)  
        judul = tk.Label(self, text="CEK PLAGIARISME BERITA", bg="teal", fg='white', 
                         width=80,height=3, font=('Times', 30, 'bold underline'))
        judul.place(x=0, y=0)
        
        
        lbl = tk.Label(self, text="Masukkan Teks 1 :", width=15, height=1, fg="white", 
                       bg="black", font=('Sans-serif', 12, 'bold'))
        lbl.place(x=50, y=155)
        
        dataset1=tk.Text(self,width=180,height=24,bg='LightGoldenRodYellow',
                         font=('Sans-serif', 9))
        dataset1.place(x=50, y=180)
        
        cleareButton1 = tk.Button(self, text='Hapus', command=clear, fg='black', bg='Gold',
                                  activebackground='dark Gray',font=('Sans-serif', 10, 'bold'))
        cleareButton1.place(x=1265, y=540)
        
        
        lbl2 = tk.Label(self, text="Masukkan Teks 2 :", width=15, height=1, fg="white", 
                        bg="black", font=('Sans-serif', 12, 'bold'))
        lbl2.place(x=50, y=560)
        
        dataset2=tk.Text(self,width=180,height=24,bg='LightGoldenRodYellow',
                         font=('Sans-serif', 9))
        dataset2.place(x=50, y=585)        
        
        cleareButton2 = tk.Button(self, text='Hapus', command=clear2, fg='Black', 
                                  bg='Gold', activebackground='dark Gray',
                                  font=('Sans-serif', 10, 'bold'))
        cleareButton2.place(x=1265, y=945)
        
        
        # membuat fungsi untuk pemrosesan algoritma_RO
        def algoritma_RO():
    # TAHAP 1 : PRE-PROCESSING TEXT 
            # GET DATA DARI INPUT TEXT
            print("INPUT TEKS :")
            dataTeks1 = dataset1.get("1.0",'end-1c')
            dataTeks2 = dataset2.get("1.0",'end-1c')
            print(dataTeks1)
            print(dataTeks2)
                                 
            # CASE FOLDING : LOWERCASE TEKS
            print("\nLOWERCASE :")
            lower1 = dataTeks1.lower()
            lower2 = dataTeks2.lower()
            print(lower1)
            print(lower2)
            
            # PUNCTUATION TEKS
            print("\nPUNCTUATION :")
            punc1 = "".join([char for char in lower1 if char not in string.punctuation])
            punc2 = "".join([char for char in lower2 if char not in string.punctuation])
            print(punc1)
            print(punc2)
            
            # STEMMING TEKS
            print("\nSTEMMING :")
            factory = StemmerFactory()
            stemmer = factory.create_stemmer()
            stem1 = stemmer.stem(punc1)
            stem2 = stemmer.stem(punc2)
            print(stem1)
            print(stem2)
                      
            # TOKENISASI TEKS
            print("\nTOKENISASI :")
            token1 = word_tokenize(stem1)
            token2 = word_tokenize(stem2)
            print(token1,token2)            
                
            # WHITESPACE REMOVAL TEKS 
            print("\nWHITESPACE REMOVAL TEKS :")
            space1 = (stem1.replace(" ",""))
            space2 = (stem2.replace(" ",""))
            print(space1,space2)
            
            
    # TAHAP 2 : PERHITUNGAN PERSENTASE MENGGUNAKAN ALGORITMA RO
        # SEQUENCE (STRING) MATCHING
            # MENGHITUNG KARAKTER TOTAL DARI 2 BUAH TEKS 
            print("\n KARAKTER TOTAL 2 TEKS :")
            word1 = len(space1)
            word2 = len(space2)
            print(word1)
            print(word2)
            char_teks_total = word1+word2
            print(char_teks_total)
            
            
        # MENGHITUNG SUB-SEQUENCE (SUB-STRING)                   
            # MENCARI KATA YANG SAMA DARI 2 TEKS 
            print("\nKATA YANG SAMA :")
            sama = []
            i = 0
            for i in token1 :
                if i in token2  :
                    sama.append(i)
            print(sama)
            
            # MENGHITUNG TOTAL KATA DARI KATA YANG SAMA 
            jumlah_kata_sama = len(sama)
            print(jumlah_kata_sama)
                        
            # WHITESPACE REMOVAL PADA KATA YANG SAMA
            print("\nWHITESPACE REMOVAL KATA SAMA :")
            kata_sama = np.array(sama, dtype=list) 
            space_sama = "".join(kata_sama)
            print(space_sama)

            # MENGHITUNG CHAR TOTAL PADA KATA YANG SAMA 
            print("\nCHAR TOTAL KATA SAMA :")
            char_kata_total = len(space_sama)
            print(char_kata_total)
            
            # MENGHITUNG NILAI SIMILARITY STRING MENGGUNAKAN ALGORITMA RO
            print("\nNILAI SIMILARITY :")
            nilai_similarity = (2*char_kata_total) / (char_teks_total)
            print(nilai_similarity)

            # MENGHITUNG PERSENTASE SIMILARITY STRING
            print("\nPERSENTASE NILAI SIMILARITY :")
            persen_similarity = (nilai_similarity*100)
            persentase_akhir = round(persen_similarity)
            print(str(persentase_akhir) +"%")
            

    # TAHAP 3 : MENGKLASIFIKASIKAN JENIS PLAGIARISME
            print("\nKLASIFIKASI : ")
            kelompok = ""
            if (persentase_akhir==0) :
                kelompok = "Kedua Teks Berbeda atau TidaK Ada Kesamaan"
            elif (persentase_akhir>=1 and persentase_akhir <15) :
                   kelompok = "Kedua Teks Memiliki Sedikit Kesamaan"
            elif (persentase_akhir>=15 and persentase_akhir <=50) :
                kelompok = "Kedua Teks Memiliki Tingkat Plagiarisme Sedang"
            elif (persentase_akhir>50 and persentase_akhir <=99) :
                kelompok = "Kedua Teks Mendekati Plagiarisme"
            elif (persentase_akhir==100) :
                kelompok = "Kedua Teks Termasuk Plagiarisme"
            print(kelompok)
            
            
    # SET DATA KE DATABASE   
        # GET DATA DARI DATABASE = tabel data_input_ambil
            cursor = db.cursor(buffered=True)
            cursor2 = db.cursor(buffered=True)
            sql1 = "SELECT teks1 FROM data_input_ambil"
            sql2 = "SELECT teks2 FROM data_input_ambil" 
            cursor.execute(sql1)
            cursor2.execute(sql2)
            result1 = cursor.fetchall()
            result2 = cursor2.fetchall()
            
            # EDIT DATA PADA DATABASE = tabel data_input_ambil
            if cursor.rowcount >0 :
                query1 = "DELETE FROM data_input_ambil"
                cursor3 = db.cursor()
                cursor3.execute(query1)
                val = (dataTeks1,dataTeks2, jumlah_kata_sama,char_teks_total,char_kata_total,persentase_akhir,kelompok)
                query2 = "INSERT INTO data_input_ambil(teks1,teks2,total_kata_sama,total_char_teks,char_kata,persen,kelas) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor4 = db.cursor()
                cursor4.execute(query2,val)
            else :
                val = (dataTeks1,dataTeks2, jumlah_kata_sama,char_teks_total,char_kata_total,persentase_akhir,kelompok)
                query = "INSERT INTO data_input_ambil(teks1,teks2,total_kata_sama,total_char_teks,char_kata,persen,kelas) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor3 = db.cursor()
                cursor3.execute(query,val)
            
        # GET DATA DARI DATABASE = tabel data_simpan
            cursor_1 = db.cursor(buffered=True)
            cursor_2 = db.cursor(buffered=True)
            sql_1 = "SELECT teks1 FROM data_simpan"
            sql_2 = "SELECT teks2 FROM data_simpan" 
            cursor_1.execute(sql1)
            cursor_2.execute(sql2)
            result_1 = cursor_1.fetchall()
            result_2 = cursor_2.fetchall()
            
            # EDIT DATA PADA DATABASE = tabel data_simpan
            if cursor_1.rowcount >=0 :
                val = (dataTeks1,dataTeks2,jumlah_kata_sama, char_teks_total,char_kata_total,persentase_akhir,kelompok)
                query2 = "INSERT INTO data_simpan(teks1,teks2,total_kata_sama,total_char_teks,char_kata,persen,kelas) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor3 = db.cursor()
                cursor3.execute(query2,val)

            # melakukan perubahan pada database
            db.commit()
            
            list3 = str(jumlah_kata_sama)
            list4 = str(char_teks_total)
            list5 = str(char_kata_total)
            list6 = str(persentase_akhir)
            list7 = str(kelompok)
            
            punc3 = "".join([char for char in list3 if char not in string.punctuation])
            punc4 = "".join([char for char in list4 if char not in string.punctuation])
            punc5 = "".join([char for char in list5 if char not in string.punctuation])
            punc6 = "".join([char for char in list6 if char not in string.punctuation])
            punc7 = "".join([char for char in list7 if char not in string.punctuation])
            
            box_totalKataSama.config(text=punc3+" Kata")
            box_totalCharTeks.config(text=punc4+" Kata")
            box_totalCharSama.config(text=punc5+" Karakter")
            box_persen.config(text=punc6+"%")
            box_klasif.config(text=punc7)
            
          
            
        # membuat tampilan (content halaman Input_Page)  
        button1 = tk.Button(self, text="Cek Plagiarisme",
                            command=lambda:algoritma_RO(), fg='white', bg='DarkSlateGrey', 
                            activebackground='dark Gray',font=('Sans-serif', 11, 'bold'))
        button1.place(x=1350, y=185)
        
        button2 = tk.Button(self, text="Hapus Semua Teks",
                            command=lambda: clear_allTeks(), fg='white', bg='DarkSlateGrey', 
                            font=('Sans-serif', 11, 'bold'))
        button2.place(x=50, y=957)
        
        label3= tk.Label(self, text="Jumlah Total Kata Pada Kata yang Sama :", width=40, 
                         height=1, fg="white", bg="Black", font=('Sans-serif', 11, 'bold'))
        label3.place(x=1350, y=250) 
        box_totalKataSama = tk.Label(self, text="", width=40, height=1, 
                                     fg="black", bg="PaleGoldenRod",font=('Sans-serif', 11, 'bold'))
        box_totalKataSama.place(x=1350, y=275) 
        
        
        label4= tk.Label(self, text="Jumlah Total Kata Pada 2 Teks :", width=40, height=1, 
                         fg="white", bg="black", font=('Sans-serif', 11, 'bold'))
        label4.place(x=1350, y=350)
        box_totalCharTeks =tk.Label(self, text="", width=40, height=1, 
                                     fg="black", bg="PaleGoldenRod",font=('Sans-serif', 11, 'bold'))
        box_totalCharTeks.place(x=1350, y=375)
        
        
        label5= tk.Label(self, text="Jumlah Total Karakter Pada Kata yang Sama :", width=40, 
                         height=1, fg="white", bg="black", font=('Sans-serif', 11, 'bold'))
        label5.place(x=1350, y=450)
        box_totalCharSama = tk.Label(self, text="", width=40, height=1, 
                                     fg="black", bg="PaleGoldenRod",font=('Sans-serif', 11, 'bold'))
        box_totalCharSama.place(x=1350, y=475)
        
        
        label6= tk.Label(self, text="Persentase Kemiripan Teks :", width=30, height=2, 
                         fg="white", bg="black", font=('Sans-serif', 12, 'bold'))
        label6.place(x=1350, y=600)
        box_persen = tk.Label(self, text="", width=30, height=2, 
                                     fg="black", bg="PaleGoldenRod",font=('Sans-serif', 12, 'bold'))
        box_persen.place(x=1350, y=645)
        
        
        label7= tk.Label(self, text="Klasifikasi Jenis Kemiripan Teks:", width=40, 
                         height=2, fg="white", bg="black", font=('Sans-serif', 12, 'bold'))
        label7.place(x=1350, y=700)
        box_klasif =tk.Label(self, text="", width=57, height=2, 
                                     fg="black", bg="PaleGoldenRod",font=('Sans-serif', 9, 'bold'))
        box_klasif.place(x=1350,y=745)
        
        
        pesan = tk.Label(self, text="Apakah Anda Ingin Mengecek Plagiarisme Berita Lainnya ?", 
                         width=45, height=1, fg="black", bg="Yellow", 
                         font=('Sans-serif', 11, 'bold'))
        pesan.place(x=1350, y=930)
        
        
        button1 = tk.Button(self, text="Cek Plagiarisme Lainnya",
                            command=lambda: clear_allData(),
                            fg='white', bg='DarkSlateGrey', font=('Sans-serif', 10, 'bold'))
        button1.place(x=1350, y=970)
        
        button2 = tk.Button(self, text="Exit",
                            command=lambda: app.destroy(), fg='white', bg='DarkSlateGrey', 
                            font=('Sans-serif', 10, 'bold'))
        button2.place(x=1550, y=970)
        
        
class View_Page(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="AliceBlue")
        
# MENJALANKAN DAN MENAMPILKAN TKINTER dari class SampleApp  
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

