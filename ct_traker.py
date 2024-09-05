import os
import datetime
import sys
import tkinter as tk
from tkinter import font, messagebox, PhotoImage
from tkinter import ttk
import pandas as pd
from cryptography.fernet import Fernet


# Função para obter o caminho absoluto do recurso (útil para PyInstaller)
def resource_path(relative_path):
    """ Obtém o caminho absoluto do recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Função para carregar a chave de criptografia
def load_key():
    key_path = resource_path("secret.key")
    return open(key_path, "rb").read()


# Inicializar Fernet com a chave carregada
key = load_key()
cipher_suite = Fernet(key)

# Arquivo para armazenar a última execução
USAGE_FILE = "C:/Dados CT/last_use.txt"

# Definir a data e hora de expiração
expiration_date = datetime.datetime(2025, 1, 1, 00, 0, 0)  # Exemplo: ano: mês: dia: hora: min: sec


def encrypt_message(message):
    return cipher_suite.encrypt(message.encode())


def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message).decode()


def check_last_use():
    current_date = datetime.datetime.now()

    # Verificar se a data atual é posterior ou igual à data de expiração
    if current_date >= expiration_date:
        messagebox.showinfo("Expiração", "Este programa expirou. Por favor, entre em contato para renovação.")
        sys.exit()

    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "rb") as file:
            encrypted_last_use = file.read()

        last_use = decrypt_message(encrypted_last_use)
        last_use_date = datetime.datetime.strptime(last_use, "%Y-%m-%d %H:%M:%S")

        # Verificar se a data atual é anterior ou igual à última data de uso
        if current_date <= last_use_date:
            messagebox.showinfo("Tentativa de burla", "Tentativa de burlar o sistema detectada. O programa expirou.")
            sys.exit()

    # Atualizar o arquivo com a data e hora atual
    encrypted_current_date = encrypt_message(current_date.strftime("%Y-%m-%d %H:%M:%S"))
    with open(USAGE_FILE, "wb") as file:
        file.write(encrypted_current_date)


def create_interface():
    window = tk.Tk()
    window.title("Controle de entradas e saídas")
    window.configure(bg="#dae0da")

    # Verificar expiração baseada na data e última execução
    check_last_use()

    # Definir o ícone da janela
    img_path = resource_path("cfc.png")
    img = PhotoImage(file=img_path)
    window.iconphoto(False, img)

    # Definição da fonte
    century_gothic_bold = font.Font(family="Century Gothic", size=12, weight="bold")
    century_gothic_normal = font.Font(family="Century Gothic", size=12)
    century_gothic_title = font.Font(family="Century Gothic", size=14, weight="bold")
    century_gothic_small = font.Font(family="Century Gothic", size=8)

    # Criação do Notebook
    notebook = ttk.Notebook(window)
    notebook.pack(pady=10, expand=True)

    # Frame da aba principal (Exibir Dados)
    main_frame = tk.Frame(notebook, bg="#dae0da")
    notebook.add(main_frame, text="Exibir Dados")

    header = tk.Label(main_frame, text="CONTROLE DE ENTRADAS E SAÍDAS", font=century_gothic_title, fg="#62b856",
                      bg="#dae0da")
    header.pack(pady=10)

    frame = tk.Frame(main_frame, bg="#dae0da")
    frame.pack(pady=10)

    label_nome = tk.Label(frame, text="Nome:", font=century_gothic_bold, bg="#dae0da")
    label_nome.grid(row=0, column=0, padx=5, pady=5)

    entry_nome = tk.Entry(frame, width=30, font=century_gothic_normal)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    label_placa = tk.Label(frame, text="Placa:", font=century_gothic_bold, bg="#dae0da")
    label_placa.grid(row=0, column=2, padx=5, pady=5)

    entry_placa = tk.Entry(frame, width=15, font=century_gothic_normal)
    entry_placa.grid(row=0, column=3, padx=5, pady=5)

    search_button = tk.Button(frame, text="Pesquisar", font=century_gothic_normal,
                              command=lambda: search_data(entry_nome, entry_placa, result_entries, vehicle_listbox,
                                                          edit_button))
    search_button.grid(row=0, column=4, padx=5, pady=5)

    separator = tk.Frame(main_frame, height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=10)

    result_frame = tk.Frame(main_frame, bg="#dae0da")
    result_frame.pack(pady=10)

    result_labels = [
        "Nome:",
        "Marca do Veículo:",
        "Modelo:",
        "Placa:",
        "Cor:"
    ]

    result_entries = {}

    for idx, text in enumerate(result_labels):
        label = tk.Label(result_frame, text=text, font=century_gothic_bold, bg="#dae0da")
        label.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=5)

        entry = tk.Label(result_frame, text="", font=century_gothic_normal, anchor="w", width=40, relief=tk.SUNKEN)
        entry.grid(row=idx, column=1, padx=5, pady=5)

        result_entries[text] = entry

    vehicle_listbox = tk.Listbox(result_frame, font=century_gothic_normal, width=50, height=6)
    vehicle_listbox.grid(row=len(result_labels), column=0, columnspan=2, pady=5)

    edit_button = tk.Button(main_frame, text="Alterar Dados", font=century_gothic_normal,
                            command=lambda: edit_data(current_person_id, century_gothic_bold, century_gothic_normal))
    edit_button.pack(pady=10)
    edit_button.config(state=tk.DISABLED)  # Inicialmente desativar o botão

    # Frame da aba de cadastro
    cadastro_frame = tk.Frame(notebook, bg="#dae0da")
    notebook.add(cadastro_frame, text="Cadastro de Pessoas")

    cadastro_header = tk.Label(cadastro_frame, text="Cadastro de Pessoas", font=century_gothic_title, fg="#62b856",
                               bg="#dae0da")
    cadastro_header.pack(pady=10)

    cadastro_form = tk.Frame(cadastro_frame, bg="#dae0da")
    cadastro_form.pack(pady=10)

    cadastro_labels = ["Nome:", "Marca do Veículo:", "Modelo:", "Placa:", "Cor:"]
    cadastro_entries = {}

    for idx, text in enumerate(cadastro_labels):
        label = tk.Label(cadastro_form, text=text, font=century_gothic_bold, bg="#dae0da")
        label.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=5)

        entry = tk.Entry(cadastro_form, font=century_gothic_normal, width=40)
        entry.grid(row=idx, column=1, padx=5, pady=5)

        cadastro_entries[text] = entry

    save_button = tk.Button(cadastro_frame, text="Salvar", font=century_gothic_normal,
                            command=lambda: save_data(cadastro_entries))
    save_button.pack(pady=10)

    # Rodapé
    footer = tk.Label(window, text="Developed by Edu Zaminelli", font=century_gothic_small, bg="#dae0da")
    footer.pack(side=tk.BOTTOM, pady=0)

    # Centralização da janela
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    # Bind teclas Enter e Esc
    window.bind('<Return>',
                lambda event: search_data(entry_nome, entry_placa, result_entries, vehicle_listbox, edit_button))
    window.bind('<Escape>', lambda event: clear_search(result_entries, vehicle_listbox, edit_button))

    window.mainloop()


def create_folder_and_file():
    folder_path = "C:/Dados CT"
    people_file_path = os.path.join(folder_path, "pessoas.xlsx")
    vehicles_file_path = os.path.join(folder_path, "veiculos.xlsx")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.exists(people_file_path):
        df_people = pd.DataFrame(columns=["ID", "Nome"])
        df_people.to_excel(people_file_path, index=False)

    if not os.path.exists(vehicles_file_path):
        df_vehicles = pd.DataFrame(columns=["ID_Veiculo", "ID_Pessoa", "Marca do Veículo", "Modelo", "Placa", "Cor"])
        df_vehicles.to_excel(vehicles_file_path, index=False)

    return people_file_path, vehicles_file_path


def add_vehicle_window(vehicle_listbox, century_gothic_bold, century_gothic_normal):
    add_window = tk.Toplevel()
    add_window.title("Adicionar Veículo")

    # Definir o ícone da janela
    img_path = resource_path("cfc.png")
    img = PhotoImage(file=img_path)
    add_window.iconphoto(False, img)

    labels = ["Marca do Veículo:", "Modelo:", "Placa:", "Cor:"]
    entries = {}

    for idx, text in enumerate(labels):
        label = tk.Label(add_window, text=text, font=century_gothic_bold)
        label.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=5)

        entry = tk.Entry(add_window, font=century_gothic_normal, width=40)
        entry.grid(row=idx, column=1, padx=5, pady=5)

        entries[text] = entry

    save_button = tk.Button(add_window, text="Salvar", font=century_gothic_normal,
                            command=lambda: save_new_vehicle(entries, vehicle_listbox, add_window))
    save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    add_window.mainloop()


def save_new_vehicle(entries, vehicle_listbox, add_window):
    data = {key: entry.get().upper() for key, entry in entries.items()}
    people_file_path, vehicles_file_path = create_folder_and_file()
    df_people = pd.read_excel(people_file_path)
    df_vehicles = pd.read_excel(vehicles_file_path)

    if data["Placa:"] in df_vehicles["Placa"].values:
        person_id = df_vehicles.loc[df_vehicles["Placa"] == data["Placa:"], "ID_Pessoa"].values[0]
        person_name = df_people.loc[df_people["ID"] == person_id, "Nome"].values[0]
        messagebox.showinfo("Info", f"A placa já está cadastrada para {person_name}.")
    else:
        if all(data.values()):
            vehicle_listbox.insert(tk.END,
                                   f"{data['Marca do Veículo:']} - {data['Modelo:']} - {data['Placa:']} - {data['Cor:']}")
            add_window.destroy()  # Fechar a janela após salvar
        else:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios.")


def delete_vehicle(vehicle_listbox):
    selected_vehicle = vehicle_listbox.curselection()
    if selected_vehicle:
        vehicle_listbox.delete(selected_vehicle)


def save_data(entries):
    data = {key: entry.get().upper() for key, entry in entries.items()}
    people_file_path, vehicles_file_path = create_folder_and_file()

    df_people = pd.read_excel(people_file_path)
    df_vehicles = pd.read_excel(vehicles_file_path)

    if data["Placa:"] in df_vehicles["Placa"].values:
        person_id = df_vehicles.loc[df_vehicles["Placa"] == data["Placa:"], "ID_Pessoa"].values[0]
        person_name = df_people.loc[df_people["ID"] == person_id, "Nome"].values[0]
        messagebox.showinfo("Info", f"A placa já está cadastrada para {person_name}.")
    else:
        if not data["Nome:"]:
            messagebox.showwarning("Aviso", "O campo 'Nome' é obrigatório.")
            return

        if df_people.empty:
            person_id = 1
        else:
            person_id = df_people["ID"].max() + 1

        new_person = pd.DataFrame([{"ID": person_id, "Nome": data["Nome:"]}])
        df_people = pd.concat([df_people, new_person], ignore_index=True)
        df_people.to_excel(people_file_path, index=False)

        vehicle_data = {
            "ID_Veiculo": len(df_vehicles) + 1,
            "ID_Pessoa": person_id,
            "Marca do Veículo": data["Marca do Veículo:"],
            "Modelo": data["Modelo:"],
            "Placa": data["Placa:"],
            "Cor": data["Cor:"]
        }

        new_vehicle = pd.DataFrame([vehicle_data])
        df_vehicles = pd.concat([df_vehicles, new_vehicle], ignore_index=True)
        df_vehicles.to_excel(vehicles_file_path, index=False)

        messagebox.showinfo("Info", "Dados salvos com sucesso!")
        clear_entries(entries)  # Limpar os campos de entrada após salvar


def search_data(entry_nome, entry_placa, result_entries, vehicle_listbox, edit_button):
    nome = entry_nome.get().strip().upper()
    placa = entry_placa.get().strip().upper()

    people_file_path, vehicles_file_path = create_folder_and_file()

    df_people = pd.read_excel(people_file_path)
    df_vehicles = pd.read_excel(vehicles_file_path)

    global current_person_id
    person = None
    vehicles = pd.DataFrame()

    if nome:
        person = df_people[df_people["Nome"].str.contains(nome, case=False, na=False)]
    elif placa:
        vehicles = df_vehicles[df_vehicles["Placa"].str.contains(placa, case=False, na=False)]
        if not vehicles.empty:
            person_id = vehicles.iloc[0]["ID_Pessoa"]
            person = df_people[df_people["ID"] == person_id]

    vehicle_listbox.delete(0, tk.END)  # Limpar a Listbox antes de preencher com novos dados

    if person is not None and not person.empty:
        person = person.iloc[0]
        current_person_id = person["ID"]
        result_entries["Nome:"].config(text=person["Nome"])

        vehicles = df_vehicles[df_vehicles["ID_Pessoa"] == person["ID"]]

        if len(vehicles) == 1:
            vehicle = vehicles.iloc[0]
            result_entries["Marca do Veículo:"].config(text=vehicle["Marca do Veículo"])
            result_entries["Modelo:"].config(text=vehicle["Modelo"])
            result_entries["Placa:"].config(text=vehicle["Placa"])
            result_entries["Cor:"].config(text=vehicle["Cor"])
        else:
            # Exibir o veículo correspondente à placa primeiro, se houver uma pesquisa por placa
            if placa:
                primary_vehicle = vehicles[vehicles["Placa"].str.contains(placa, case=False, na=False)].iloc[0]
                result_entries["Marca do Veículo:"].config(text=primary_vehicle["Marca do Veículo"])
                result_entries["Modelo:"].config(text=primary_vehicle["Modelo"])
                result_entries["Placa:"].config(text=primary_vehicle["Placa"])
                result_entries["Cor:"].config(text=primary_vehicle["Cor"])
                vehicles = vehicles[vehicles["Placa"] != primary_vehicle["Placa"]]

            else:
                first_vehicle = vehicles.iloc[0]
                result_entries["Marca do Veículo:"].config(text=first_vehicle["Marca do Veículo"])
                result_entries["Modelo:"].config(text=first_vehicle["Modelo"])
                result_entries["Placa:"].config(text=first_vehicle["Placa"])
                result_entries["Cor:"].config(text=first_vehicle["Cor"])

            for idx, vehicle in vehicles.iterrows():
                vehicle_listbox.insert(tk.END,
                                       f"{vehicle['Marca do Veículo']} - {vehicle['Modelo']} - {vehicle['Placa']} - {vehicle['Cor']}")

        edit_button.config(state=tk.NORMAL)  # Habilitar o botão de edição após uma pesquisa bem-sucedida

        entry_nome.delete(0, tk.END)
        entry_placa.delete(0, tk.END)
    else:
        messagebox.showinfo("Info", "Nenhuma correspondência encontrada.")
        clear_search(result_entries, vehicle_listbox, edit_button)  # Limpar campos se nenhuma correspondência for encontrada
        entry_nome.delete(0, tk.END)
        entry_placa.delete(0, tk.END)
        edit_button.config(state=tk.DISABLED)  # Desativar o botão de edição se nenhuma correspondência for encontrada


def edit_data(person_id, century_gothic_bold, century_gothic_normal):
    people_file_path, vehicles_file_path = create_folder_and_file()

    df_people = pd.read_excel(people_file_path)
    df_vehicles = pd.read_excel(vehicles_file_path)

    person = df_people[df_people["ID"] == person_id].iloc[0]
    vehicles = df_vehicles[df_vehicles["ID_Pessoa"] == person_id]

    edit_window = tk.Toplevel()
    edit_window.title("Editar Dados")

    # Definir o ícone da janela
    img_path = resource_path("cfc.png")
    img = PhotoImage(file=img_path)
    edit_window.iconphoto(False, img)

    edit_labels = ["Nome:", "Marca do Veículo:", "Modelo:", "Placa:", "Cor:"]
    edit_entries = {}

    for idx, text in enumerate(edit_labels):
        label = tk.Label(edit_window, text=text, font=century_gothic_bold)
        label.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=5)

        entry = tk.Entry(edit_window, font=century_gothic_normal, width=40)
        entry.grid(row=idx, column=1, padx=5, pady=5)

        if text == "Nome:":
            entry.insert(0, person["Nome"])
        elif text == "Marca do Veículo:":
            entry.insert(0, vehicles.iloc[0]["Marca do Veículo"] if not vehicles.empty else "")
        elif text == "Modelo:":
            entry.insert(0, vehicles.iloc[0]["Modelo"] if not vehicles.empty else "")
        elif text == "Placa:":
            entry.insert(0, vehicles.iloc[0]["Placa"] if not vehicles.empty else "")
        elif text == "Cor:":
            entry.insert(0, vehicles.iloc[0]["Cor"] if not vehicles.empty else "")

        edit_entries[text] = entry

    vehicle_listbox = tk.Listbox(edit_window, font=century_gothic_normal, width=50, height=6)
    vehicle_listbox.grid(row=len(edit_labels), column=0, columnspan=2, pady=5)

    for idx, vehicle in vehicles.iterrows():
        vehicle_listbox.insert(tk.END,
                               f"{vehicle['Marca do Veículo']} - {vehicle['Modelo']} - {vehicle['Placa']} - {vehicle['Cor']}")

    add_vehicle_button = tk.Button(edit_window, text="Adicionar Veículo", font=century_gothic_normal,
                                   command=lambda: add_vehicle_window(vehicle_listbox, century_gothic_bold,
                                                                      century_gothic_normal))
    add_vehicle_button.grid(row=len(edit_labels) + 1, column=0, padx=5, pady=5)

    delete_vehicle_button = tk.Button(edit_window, text="Excluir Veículo", font=century_gothic_normal,
                                      command=lambda: delete_vehicle(vehicle_listbox))
    delete_vehicle_button.grid(row=len(edit_labels) + 1, column=1, padx=5, pady=5)

    save_button = tk.Button(edit_window, text="Salvar", font=century_gothic_normal,
                            command=lambda: save_edited_data(person_id, edit_entries, vehicle_listbox, edit_window))
    save_button.grid(row=len(edit_labels) + 2, column=0, columnspan=2, pady=10)

    delete_person_button = tk.Button(edit_window, text="Excluir Pessoa", font=century_gothic_normal,
                                     command=lambda: delete_person(person_id, edit_window))
    delete_person_button.grid(row=len(edit_labels) + 3, column=0, columnspan=2, pady=10)

    edit_window.mainloop()


def delete_person(person_id, edit_window):
    people_file_path, vehicles_file_path = create_folder_and_file()

    df_people = pd.read_excel(people_file_path)
    df_vehicles = pd.read_excel(vehicles_file_path)

    df_people = df_people[df_people["ID"] != person_id]
    df_vehicles = df_vehicles[df_vehicles["ID_Pessoa"] != person_id]

    df_people.to_excel(people_file_path, index=False)
    df_vehicles.to_excel(vehicles_file_path, index=False)

    messagebox.showinfo("Info", "Pessoa e veículos associados excluídos com sucesso!")
    edit_window.destroy()  # Fechar a janela após excluir


def save_edited_data(person_id, entries, vehicle_listbox, edit_window):
    data = {key: entry.get().upper() for key, entry in entries.items()}
    people_file_path, vehicles_file_path = create_folder_and_file()

    df_people = pd.read_excel(people_file_path)
    df_vehicles = pd.read_excel(vehicles_file_path)

    df_people.loc[df_people["ID"] == person_id, "Nome"] = data["Nome:"]

    df_vehicles = df_vehicles[df_vehicles["ID_Pessoa"] != person_id]  # Remover veículos existentes da pessoa

    for i in range(vehicle_listbox.size()):
        vehicle_details = vehicle_listbox.get(i).split(" - ")
        vehicle_data = {
            "ID_Veiculo": len(df_vehicles) + 1,
            "ID_Pessoa": person_id,
            "Marca do Veículo": vehicle_details[0],
            "Modelo": vehicle_details[1],
            "Placa": vehicle_details[2],
            "Cor": vehicle_details[3]
        }
        df_vehicles = pd.concat([df_vehicles, pd.DataFrame([vehicle_data])], ignore_index=True)

    df_people.to_excel(people_file_path, index=False)
    df_vehicles.to_excel(vehicles_file_path, index=False)

    messagebox.showinfo("Info", "Dados alterados com sucesso!")
    edit_window.destroy()  # Fechar a janela após salvar


def clear_entries(entries):
    for entry in entries.values():
        entry.delete(0, tk.END)


def clear_search(result_entries, vehicle_listbox, edit_button):
    for entry in result_entries.values():
        entry.config(text="")
    vehicle_listbox.delete(0, tk.END)
    edit_button.config(state=tk.DISABLED)


people_file_path, vehicles_file_path = create_folder_and_file()
create_interface()
