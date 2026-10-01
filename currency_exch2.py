import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb


def update_base_label(event):
    code = base_combobox.get()
    base_label.config(text=currencies[code])


def update_base2_label(event):
    code = base2_combobox.get()
    base2_label.config(text=currencies[code])


def update_target_label(event):
    code = target_combobox.get()
    target_label.config(text=currencies[code])


def exchange():
    target_code = target_combobox.get()
    base_code = base_combobox.get()
    base2_code = base2_combobox.get()

    if target_code and base_code and base2_code:
        try:
            result1 = requests.get(f"https://open.er-api.com/v6/latest/{base_code}")
            result1.raise_for_status()
            data1 = result1.json()

            result2 = requests.get(f"https://open.er-api.com/v6/latest/{base2_code}")
            result2.raise_for_status()
            data2 = result2.json()

            if target_code in data1['rates'] and target_code in data2['rates']:
                rate1 = data1['rates'][target_code]
                rate2 = data2['rates'][target_code]

                base_name = currencies[base_code]
                base2_name = currencies[base2_code]
                target_name = currencies[target_code]

                mb.showinfo(
                    'Курс обмена',
                    f'1 {base_name} = {rate1:.1f} {target_name}\n'
                    f'1 {base2_name} = {rate2:.1f} {target_name}'
                )
            else:
                mb.showerror('Ошибка', f'Валюта {target_code} не найдена')
        except Exception as e:
            mb.showerror('Ошибка', f'error 400 {e}')


currencies = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "CNY": "Юань",
    "RUB": "Российский рубль",
}

root = Tk()
root.title("Курсы обмена валют")
root.geometry("300x400")
root.resizable(False, False)

title_font = ("Segoe UI", 10, "bold")
label_font = ("Segoe UI", 9)
combo_font = ("Segoe UI", 9)
btn_font = ("Segoe UI", 9)

Label(text='Базовая валюта', font=title_font).pack(pady=(15, 8))
base_combobox = ttk.Combobox(values=list(currencies.keys()), font=combo_font,
                             state='readonly', width=22)
base_combobox.pack()
base_label = Label(text='', font=label_font, fg='gray30')
base_label.pack(pady=(6, 12))

Label(text='Вторая базовая валюта', font=title_font).pack(pady=(0, 8))
base2_combobox = ttk.Combobox(values=list(currencies.keys()), font=combo_font,
                              state='readonly', width=22)
base2_combobox.pack()
base2_label = Label(text='', font=label_font, fg='gray30')
base2_label.pack(pady=(6, 12))

Label(text='Целевая валюта', font=title_font).pack(pady=(0, 8))
target_combobox = ttk.Combobox(values=list(currencies.keys()), font=combo_font,
                               state='readonly', width=22)
target_combobox.pack()
target_label = Label(text='', font=label_font, fg='gray30')
target_label.pack(pady=(6, 15))

button = Button(text='Получить курс обмена', font=btn_font, width=22)
button.pack(pady=(5, 15))

base_combobox.bind("<<ComboboxSelected>>", update_base_label)
base2_combobox.bind("<<ComboboxSelected>>", update_base2_label)
target_combobox.bind("<<ComboboxSelected>>", update_target_label)

root.mainloop()