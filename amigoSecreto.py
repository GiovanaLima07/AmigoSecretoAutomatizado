import tkinter as tk
from tkinter import messagebox
import smtplib
import random
from email.mime.text import MIMEText

#email do remetente 
REMETENTE = "automaticoamigosecreto@gmail.com"
SENHA = "gdsc vjde hcga iboi"

#função que armazena e validade informações do participante
participantes_do_sorteio = {}

def adicionar():
    nome = entry_nome.get()
    email = entry_email.get()

    if not nome or not email:
        messagebox.showwarning("Preencha todos os campos.")
        return

    if email in participantes_do_sorteio.values():
        messagebox.showerror("Este e-mail já foi cadastrado.")
        return

    participantes_do_sorteio[nome] = email
    i = lista_participantes.size() + 1
    lista_participantes.insert(tk.END, f"{i}. {nome}")

    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Função para sortear e enviar e-mails
def sortear_e_enviar():
    if len(participantes_do_sorteio) < 2 or len(participantes_do_sorteio) % 2 != 0:
        messagebox.showerror("Erro", "É necessário um número par de participantes (mínimo 2).")
        return

    nomes = list(participantes_do_sorteio.keys())
    sorteados = nomes[:]

    for _ in range(10): 
        random.shuffle(sorteados)
        pares = dict(zip(nomes, sorteados))
        if all(k != v for k, v in pares.items()):
            break

    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(REMETENTE, SENHA)
    except Exception as e:
        messagebox.showerror("Erro de conexão")
        return

    for participante, amigo in pares.items():
        destinatario = participantes_do_sorteio[participante]
        corpo = f"Parabens {participante},\n\nVocê tirou: {amigo} como seu amigo secreto!\n\nNão conte pra ninguém é segredo 😉"
        msg = MIMEText(corpo)
        msg['Subject'] = "Amigo Secreto 🎁"
        msg['From'] = REMETENTE
        msg['To'] = destinatario
        try:
            smtp.sendmail(REMETENTE, destinatario, msg.as_string())
        except Exception as e:
            messagebox.showerror("Erro ao enviar o email")
            smtp.quit()
            return

    smtp.quit()
    messagebox.showinfo("Sorteio finalizado", "e-mails enviados!")
    root.quit()

# --- Interface Tkinter ---
root = tk.Tk()
root.title("Amigo Secreto 🎁")

tk.Label(root, text="Nome:").grid(row=0, column=0, sticky="e")
entry_nome = tk.Entry(root, width=30)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Email:").grid(row=1, column=0, sticky="e")
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=1, column=1)

tk.Button(root, text="Adicionar Participante", command=adicionar).grid(row=2, column=0, columnspan=2, pady=10)

tk.Label(root, text="Participantes:").grid(row=3, column=0, columnspan=2)
lista_participantes = tk.Listbox(root, width=50, height=10)
lista_participantes.grid(row=4, column=0, columnspan=2)

tk.Button(root, text="Sortear e Enviar E-mails", command=sortear_e_enviar, bg="green", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
