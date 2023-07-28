import pandas as pd
import random
from datetime import datetime, timedelta

def generate_random_date(start_year, end_year):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date

def generate_price(start_range,end_range):
    price = random.uniform(start_range,end_range)
    formated_price = f"{price:.2f}"
    return float(formated_price)

categoria_produto = {
    "Alimentos":[
        "Maçã",
        "Banana",
        "Laranja",
        "Uva",
        "Alho",
        "Cebola",
        "Tomate",
        "Chocolate",
        "Geleia",
        "Ovo"],
    "Cosméticos":[
        "Shampoo",
        "Tônico facial",
        "Corretivo",
        "Base",
        "Blush",
        "Perfume",
        "Desodorante",
        "Esmalte",
        "Iluminador",
        "Lápis de olho"
    ],
    "Roupas":[
        "Camiseta",
        "Bermuda",
        "Vestido",
        "Jeans",
        "Boné",
        "Chapéu",
        "Gorro",
        "Sutiã",
        "Luvas",
        "Meias"
    ],
    "Eletrodomésticos":[
        "Geladeira",
        "Fogão",
        "Micro-ondas",
        "Máquina de lavar roupa",
        "Secadora de roupas",
        "Aspirador de pó",
        "Batedeira",
        "Torradeira",
        "Forno elétrico",
        "Ar-condicionado"
    ],
    "Ferramentas Manuais":[
        "Tesoura",
        "Martelo",
        "Nível",
        "Chave estrela",
        "Esquadro",
        "Formão",
        "Pregos",
        "Enxada",
        "Grampo",
        "Serra" 
    ]
}

filiais = ["SP","MG","RJ","ES","PR","MS"]
formas_pagamento = ["Crédito","Débito","Boleto","Pix"]
metodo_entrega = ["Retirada","PAC","Sedex"]



df = pd.DataFrame()



for i in range(7892):
    new_df = pd.DataFrame()
    categoria = random.choice(list(categoria_produto.keys()))
    new_df["Nome"] = [random.choice(categoria_produto[categoria])]
    new_df["Categoria"] = [categoria]
    if categoria == "Alimentos":
        preco = generate_price(1,12)
    elif categoria == "Cosméticos":
        preco = generate_price(20,75)
    elif categoria == "Roupas":
        preco = generate_price(50,300)
    elif categoria == "Eletrodomésticos":
        preco = generate_price(500,3000)
    elif categoria == "Ferramentas Manuais":
        preco = generate_price(10,50)
    unidades = random.randint(1,50)
    new_df["Preço"] = [preco]
    new_df["Unidades Vendidas"] = [unidades]
    new_df["Total"] = [float(f"{(preco*unidades):.2f}")]
    new_df["Filial"] = [random.choice(filiais)]
    new_df["Forma de Pagamento"] = [random.choice(formas_pagamento)]
    new_df["Método de Entrega"] = [random.choice(metodo_entrega)]
    new_df["Data"] = [generate_random_date(2010,2022)]
    df = pd.concat([df,new_df],axis=0)


df.to_csv("products.csv",encoding="utf-8")
