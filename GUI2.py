# library untuk GUI
import tkinter as tk
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ambil dari database
import sqlite3

# memasukan fungsi perhitungan
from saham import kalkulasi

# menghhubungkan databasecle
conn = sqlite3.connect("database.db")
c = conn.cursor()

# deklarasi global variable buat saham
emitenYangDicari = []
listSaham = []

# hubungkan database ke combobox subsektor
def combo_Sektor():

    # conn = sqlite3.connect("database.db")
    # cur = conn.cursor()

    # query = cur.execute("SELECT DISTINCT Nama_Sektor FROM Data")

    # cb_sek = []
    # for row in cur.fetchall():
    #     cb_sek.append(row[0])
    return['transportation']

    # cur.close()
    # conn.close()
# bitxh=combo_Sektor()
# print(bitxh['communications'])
# import sys
# sys.exit()

def combo_SubSektor(event):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    query = cur.execute(
        f"SELECT DISTINCT Nama_SubSektor FROM Data WHERE Nama_Sektor = '{event.widget.get()}'"
    )

    ss_sek = []
    for row in cur.fetchall():
        ss_sek.append(row[0])

    cb_subsek["values"] = ss_sek

    cur.close()
    conn.close()


# hubungkan database ke combobox emiten
def combo_Emiten(event):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    query = cur.execute(
        f"SELECT DISTINCT Nama_Emiten FROM Data WHERE Nama_SubSektor ='{event.widget.get()}'"
    )

    for row in cur.fetchall():
        emitenYangDicari.append(row[0])

    cb_em["values"] = emitenYangDicari

    cur.close()
    conn.close()


# main window
main = tk.Tk()
main.title("Optimasi Saham Markowitz")
main.geometry("1000x1000")

# frame label
main_frame = LabelFrame(main, text="Investasi Saham", font=("roboto", 20))
main_frame.place(
    x=50,
    y=50,
)

# inv label
inv_label = Label(main_frame, text="Total Modal", font=("roboto", 12))
inv_label.grid(row=0, column=0, padx=10, pady=10)
# inv entry
inv_entry = Entry(main_frame, width=25)
inv_entry.grid(row=0, column=1, padx=10, pady=10)

# fungsi isi tabel
def View():
    if (
        listSaham == []
        or inv_entry.get() == ""
        or cb_sek.get() == ""
        or cb_subsek.get() == ""
    ):
        return tk.messagebox.showerror("Perhatian", "Silahkan Isi Semuanya")

    biaya = int(inv_entry.get())
    (
        anggaran,
        lot,
        sisaUang,
        persensaham,
        expectedReturn,
        volatility,
        sharpeRatio,
        harga_terbaru,
    ) = kalkulasi(listSaham, biaya)

    for datas in main_tree.get_children():
        datanya = main_tree.item(datas, "values")
        main_tree.item(
            datas,
            text="",
            values=(
                datanya[0],
                datanya[1],
                datanya[2],
                datanya[3],
                harga_terbaru[datanya[3] + ".JK"],
                f'Rp.{anggaran[datanya[3]+".JK"]}',
                f'{persensaham[datanya[3]+".JK"]}%',
                f'{lot[datanya[3]+".JK"]}',
            ),
        )

    cb_em.set("")
    cb_em["values"] = [""]
    cb_sek.set("")
    cb_subsek.set("")
    cb_subsek["values"] = [""]
    listSaham.clear()

    sis_label.config(text=f"Sisa uang nya : Rp.{sisaUang}")
    re_label.config(text=f"Expected Annual Return : {round(expectedReturn*100)}%")
    vol_label.config(text=f"Annual Volatility : {round(volatility*100)}")
    sar_label.config(text=f"Sharpe Ratio : {round(sharpeRatio)}")


# keterangan hasil Return
re_label = Label(main, font=("roboto", 12))
re_label.place(x=50, y=500)

vol_label = Label(main, font=("roboto", 12))
vol_label.place(x=50, y=520)

sis_label = Label(main, font=("roboto", 12))
sis_label.place(x=50, y=540)

sar_label = Label(main, font=("roboto", 12))
sar_label.place(x=50, y=560)

# inv button
inv_but = Button(main_frame, text="Proses", command=View)
inv_but.grid(row=0, column=2, padx=10, pady=10)

# fungsi tambah
def tambahSaham():
    if sis_label.cget("text") != "":
        for i in main_tree.get_children():
            main_tree.delete(i)
        sis_label.config(text="")
        re_label.config(text="")
        vol_label.config(text="")
        sar_label.config(text="")

    emitenYangDicari.remove(cb_em.get())
    cb_em["values"] = emitenYangDicari
    listSaham.append(cb_em.get())

    main_tree.insert(
        parent="",
        index="end",
        iid=len(main_tree.get_children()),
        text="",
        values=(
            len(main_tree.get_children()) + 1,
            cb_sek.get(),
            cb_subsek.get(),
            cb_em.get(),
        ),
    )
    cb_em.set("")


# tombol tambah
tambah_but = Button(main_frame, text="Tambah", command=tambahSaham)
tambah_but.grid(row=2, column=2, padx=10, pady=10)

# fungsi hapus


def hapusTabel():
    for i in main_tree.get_children():
        datanya = main_tree.item(i, "values")[3]
        print(listSaham)
        if listSaham != []:
            listSaham.remove(datanya)
        main_tree.delete(i)
    sis_label.config(text="")
    re_label.config(text="")
    vol_label.config(text="")
    sar_label.config(text="")
    cb_em["values"] = [""]
    cb_em.set("")
    cb_subsek["values"] = [""]
    cb_subsek.set("")
    cb_sek.set("")


# tombol hapus
hapus_but = Button(main_frame, text="Hapus Semua", command=hapusTabel)
hapus_but.grid(row=3, column=2, padx=10, pady=10)

# combobox
# sektor
sek_label = Label(main_frame, text="Sektor")
sek_label.grid(row=1, column=0, padx=10, pady=10)

cb_sek = ttk.Combobox(main_frame, width=25, state="readonly", values=combo_Sektor())
cb_sek.grid(row=1, column=1, padx=10, pady=10)
# cb_sek.bind("<<ComboboxSelected>>", combo_SubSektor)
cb_sek.current(0)

# subsektor
ss_label = Label(main_frame, text="Sub Sektor")
ss_label.grid(row=2, column=0, padx=10, pady=10)

cb_subsek = ttk.Combobox(main_frame, width=25, state="readonly", values=['marine shipping'])
cb_subsek.grid(row=2, column=1, padx=10, pady=10)
cb_subsek.bind("<<ComboboxSelected>>", combo_Emiten)
cb_subsek.current(0)

# Emiten
em_label = Label(main_frame, text="Emiten")
em_label.grid(row=3, column=0, padx=10, pady=10)

cb_em = ttk.Combobox(main_frame, width=25, state="readonly")
cb_em.grid(row=3, column=1, padx=10, pady=10)


# setting tabel
style = ttk.Style()
style.theme_use("default")
style.configure(
    "TreeView",
    backgroud="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3",
)
# select berubah warna jika cursor select itemnya
style.map("TreeView", background=[("selected", "#347083")])

# frame tabel
tree_frame = Frame(
    main,
)
tree_frame.place(x=50, y=270)

# scroll bar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# membuat tabel
main_tree = ttk.Treeview(
    tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended"
)
main_tree.pack()

# setting scroll bar
tree_scroll.config(command=main_tree.yview)

# membuat kolom
main_tree["columns"] = (
    "ID",
    "Sektor",
    "Subsektor",
    "Emiten",
    "Harga",
    "Total Modal",
    "Alokasi",
    "Lot",
)

# format kolom
main_tree.column("#0", width=0, stretch=NO)
main_tree.column("ID", width=50, anchor=CENTER)
main_tree.column("Sektor", width=150, anchor=CENTER)
main_tree.column("Subsektor", width=160, anchor=CENTER)
main_tree.column("Emiten", width=80, anchor=CENTER)
main_tree.column("Harga", width=100, anchor=CENTER)
main_tree.column("Total Modal", width=120, anchor=CENTER)
main_tree.column("Alokasi", width=100, anchor=CENTER)
main_tree.column("Lot", width=80, anchor=CENTER)

# judul kolom
main_tree.heading("#0", text="", anchor=W)
main_tree.heading("ID", text="ID", anchor=CENTER)
main_tree.heading("Sektor", text="Sektor", anchor=CENTER)
main_tree.heading("Subsektor", text="Subsektor", anchor=CENTER)
main_tree.heading("Emiten", text="Emiten", anchor=CENTER)
main_tree.heading("Harga", text="Harga", anchor=CENTER)
main_tree.heading("Total Modal", text="Total Modal", anchor=CENTER)
main_tree.heading("Alokasi", text="Alokasi", anchor=CENTER)
main_tree.heading("Lot", text="Lot", anchor=CENTER)



main.mainloop()
