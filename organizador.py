
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


# Categorias e extensões dos arquivos
categorias = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".odt"],
    "Planilhas": [".xlsx", ".xls", ".csv", ".ods"],
    "Apresentacoes": [".pptx", ".ppt", ".odp"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Audios": [".mp3", ".wav", ".ogg", ".flac"],
    "Compactados": [".zip", ".rar", ".7z"],
    "Executaveis": [".exe", ".msi"],
    "Codigos": [".py", ".js", ".html", ".css", ".java", ".cpp"]
}


# Variável para armazenar a pasta selecionada
pasta_selecionada = ""


# Função para selecionar uma pasta
def selecionar_pasta():
    global pasta_selecionada

    pasta = filedialog.askdirectory(
        title="Selecione a pasta que deseja organizar"
    )

    if pasta:
        pasta_selecionada = pasta

        campo_pasta.config(state="normal")
        campo_pasta.delete(0, tk.END)
        campo_pasta.insert(0, pasta)
        campo_pasta.config(state="readonly")

        botao_organizar.config(state="normal")

        texto_status.config(
            text="Pasta selecionada com sucesso!",
            fg="#65E6A5"
        )


# Função para identificar a categoria do arquivo
def identificar_categoria(extensao):

    for categoria, extensoes in categorias.items():

        if extensao.lower() in extensoes:
            return categoria

    return "Outros"


# Função para organizar os arquivos
def organizar_arquivos():

    if not pasta_selecionada:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma pasta primeiro."
        )
        return

    confirmacao = messagebox.askyesno(
        "Confirmar organização",
        "Deseja organizar os arquivos desta pasta?\n\n"
        "Os arquivos serão movidos para novas pastas."
    )

    if not confirmacao:
        return

    total = 0
    erros = 0

    try:
        arquivos = os.listdir(pasta_selecionada)

        for arquivo in arquivos:

            caminho_arquivo = os.path.join(
                pasta_selecionada,
                arquivo
            )

            # Ignora pastas e outros itens que não sejam arquivos
            if not os.path.isfile(caminho_arquivo):
                continue

            # Obtém a extensão do arquivo
            nome, extensao = os.path.splitext(arquivo)

            # Identifica a categoria
            categoria = identificar_categoria(extensao)

            # Cria o caminho da pasta de destino
            pasta_destino = os.path.join(
                pasta_selecionada,
                categoria
            )

            # Cria a pasta caso ela não exista
            os.makedirs(pasta_destino, exist_ok=True)

            # Define o destino do arquivo
            destino = os.path.join(
                pasta_destino,
                arquivo
            )

            # Evita substituir arquivos existentes
            if os.path.exists(destino):
                erros += 1
                continue

            try:
                # Move o arquivo para a categoria correspondente
                shutil.move(caminho_arquivo, destino)
                total += 1

            except OSError:
                erros += 1

        # Atualiza a interface
        texto_status.config(
            text="Organização concluída!",
            fg="#65E6A5"
        )

        messagebox.showinfo(
            "Organização concluída",
            f"Arquivos organizados: {total}\n"
            f"Arquivos não movidos: {erros}\n\n"
            "Processo finalizado!"
        )

    except OSError as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível acessar a pasta:\n{erro}"
        )


# Configuração da janela principal
janela = tk.Tk()
janela.title("Organizador de Arquivos")
janela.geometry("500x550")
janela.resizable(False, False)
janela.configure(bg="#20232A")


# Título do programa
titulo = tk.Label(
    janela,
    text="ORGANIZADOR DE ARQUIVOS",
    font=("Arial", 18, "bold"),
    bg="#20232A",
    fg="white"
)
titulo.pack(pady=(30, 5))


# Subtítulo
subtitulo = tk.Label(
    janela,
    text="Organize seus arquivos automaticamente",
    font=("Arial", 10),
    bg="#20232A",
    fg="#B0B0B0"
)
subtitulo.pack(pady=(0, 25))


# Área principal
frame = tk.Frame(
    janela,
    bg="#2D323C",
    padx=20,
    pady=20
)
frame.pack(padx=30, fill="both")


# Orientação
tk.Label(
    frame,
    text="Selecione a pasta que deseja organizar:",
    font=("Arial", 11, "bold"),
    bg="#2D323C",
    fg="white"
).pack(anchor="w", pady=(0, 10))


# Campo para mostrar o caminho da pasta
campo_pasta = tk.Entry(
    frame,
    font=("Arial", 9),
    state="readonly",
    readonlybackground="#20232A",
    fg="white",
    relief="flat"
)
campo_pasta.pack(fill="x", ipady=9, pady=(0, 12))


# Botão para selecionar pasta
botao_selecionar = tk.Button(
    frame,
    text="SELECIONAR PASTA",
    font=("Arial", 10, "bold"),
    bg="#343A46",
    fg="white",
    activebackground="#454D5B",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=selecionar_pasta
)
botao_selecionar.pack(fill="x", ipady=8)


# Categorias disponíveis
tk.Label(
    frame,
    text="Categorias de organização:",
    font=("Arial", 11, "bold"),
    bg="#2D323C",
    fg="white"
).pack(anchor="w", pady=(20, 10))


categorias_texto = [
    "Imagens",
    "Documentos",
    "Planilhas",
    "Apresentações",
    "Vídeos",
    "Áudios",
    "Compactados",
    "Executáveis",
    "Códigos",
    "Outros"
]

# Exibe as categorias em duas colunas
frame_categorias = tk.Frame(frame, bg="#2D323C")
frame_categorias.pack(fill="x")

for indice, categoria in enumerate(categorias_texto):

    linha = indice // 2
    coluna = indice % 2

    tk.Label(
        frame_categorias,
        text=f"• {categoria}",
        font=("Arial", 10),
        bg="#2D323C",
        fg="#D0D0D0"
    ).grid(
        row=linha,
        column=coluna,
        sticky="w",
        padx=10,
        pady=4
    )


# Botão para organizar arquivos
botao_organizar = tk.Button(
    janela,
    text="ORGANIZAR ARQUIVOS",
    font=("Arial", 12, "bold"),
    bg="#6C45D9",
    fg="white",
    activebackground="#5433B5",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    state="disabled",
    command=organizar_arquivos
)
botao_organizar.pack(fill="x", padx=50, pady=25, ipady=12)


# Status do programa
texto_status = tk.Label(
    janela,
    text="Aguardando seleção de uma pasta...",
    font=("Arial", 9),
    bg="#20232A",
    fg="#B0B0B0"
)
texto_status.pack(pady=5)


# Rodapé
tk.Label(
    janela,
    text="Desenvolvido em Python com Tkinter",
    font=("Arial", 8),
    bg="#20232A",
    fg="#888888"
).pack(side="bottom", pady=15)


# Inicia a aplicação
janela.mainloop()
