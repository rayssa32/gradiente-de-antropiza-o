import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================
# DADOS
# =========================
dados = pd.DataFrame({
    "Municipio": [
        "Alfenas", "Itajubá", "Lavras", "Poços de Caldas",
        "Pouso Alegre", "Três Corações", "Varginha"
    ],
    "Shannon": [1.243, 0.948, 1.085, 1.190, 1.096, 0.991, 1.095],
    "Equitabilidade": [0.772, 0.589, 0.674, 0.739, 0.681, 0.616, 0.680]
})

# =========================
# GRADIENTE DE ANTROPIZAÇÃO
# =========================
ordem_gradiente = {
    "Lavras": 1,
    "Alfenas": 2,
    "Poços de Caldas": 3,
    "Varginha": 4,
    "Três Corações": 5,
    "Itajubá": 6,
    "Pouso Alegre": 7
}

dados["Gradiente"] = dados["Municipio"].map(ordem_gradiente)
dados = dados.sort_values("Gradiente")

# =========================
# NORMALIZAÇÃO DO SHANNON
# =========================
sh_min = dados["Shannon"].min()
sh_max = dados["Shannon"].max()

dados["Shannon_norm"] = (dados["Shannon"] - sh_min) / (sh_max - sh_min)

# Escala visual dos pontos
sizes = 300 + dados["Shannon_norm"] * 2000

# =========================
# FIGURA
# =========================
fig, ax = plt.subplots(figsize=(13, 6))

# Linha base do gradiente
ax.hlines(y=0, xmin=1, xmax=7, linewidth=3)

# Pontos
scatter = ax.scatter(
    dados["Gradiente"],
    np.zeros(len(dados)),
    s=sizes,
    c=dados["Equitabilidade"],
    cmap="viridis",
    edgecolor="black"
)

# Nome dos municípios e valores
for _, row in dados.iterrows():
    ax.text(
        row["Gradiente"],
        0.12,
        row["Municipio"],
        ha="center",
        fontsize=10,
        rotation=25
    )

    ax.text(
        row["Gradiente"],
        -0.15,
        f"H'={row['Shannon']:.3f}\nJ'={row['Equitabilidade']:.3f}",
        ha="center",
        fontsize=9
    )

# Rótulos superiores
ax.text(1, 0.30, "VEGETAÇÃO", ha="center", fontsize=10, fontweight="bold")
ax.text(3, 0.30, "AGRO/PASTAGEM", ha="center", fontsize=10, fontweight="bold")
ax.text(5, 0.30, "SOLO EXPOSTO", ha="center", fontsize=10, fontweight="bold")
ax.text(7, 0.30, "URBANO", ha="center", fontsize=10, fontweight="bold")

# Rótulos inferiores
ax.text(1, -0.35, "Maior equilíbrio", ha="center", fontsize=10)
ax.text(7, -0.35, "Maior antropização", ha="center", fontsize=10)

# Barra de cores com mais espaçamento
cbar = plt.colorbar(scatter, ax=ax, pad=0.08)
cbar.set_label("Equitabilidade (J')")

# Título
ax.set_title(
    "Gradiente de uso antrópico e diversidade da paisagem",
    fontsize=14
)

# Ajustes de escala e margens
ax.set_xlim(0.5, 7.8)
ax.set_ylim(-0.45, 0.45)

# Remover eixos
ax.set_xticks([])
ax.set_yticks([])

# Ajuste manual do layout
plt.subplots_adjust(
    left=0.05,
    right=0.88,
    bottom=0.18,
    top=0.85
)

# Salvar figura em alta resolução
plt.savefig(
    "figura_gradiente_antropizacao_diversidade.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
