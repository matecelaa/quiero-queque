import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def analisis_finales():
    df_matches = pd.read_csv(r"data\matches_1930_2022.csv")

    finales_data = df_matches[df_matches["Round"] == "Final"]
    columnas = [
        "home_team", "home_score", "away_team", "away_score", 
        "Notes", "home_red_card", "away_red_card", 
        "home_yellow_card_long", "away_yellow_card_long", "Year"
    ]
    finales = finales_data[columnas].fillna(0)
    lista_finales = finales.to_dict('records')

    #contadores
    goles_20, amarillas_20, rojas_20, num_finales_20 = 0, 0, 0, 0
    penales_20, extra_20, regular_20 = 0, 0, 0
    detalle_20 = [] 

    goles_21, amarillas_21, rojas_21, num_finales_21 = 0, 0, 0, 0
    penales_21, extra_21, regular_21 = 0, 0, 0
    detalle_21 = []

    for final in lista_finales:
        año = int(final['Year'])
        nota = str(final['Notes']).lower()
        
        # conteo de tarjetas
        am_p, ro_p = 0, 0
        if final['home_yellow_card_long'] != 0: am_p += str(final['home_yellow_card_long']).count(',') + 1
        if final['away_yellow_card_long'] != 0: am_p += str(final['away_yellow_card_long']).count(',') + 1
        if final['home_red_card'] != 0: ro_p += str(final['home_red_card']).count(',') + 1
        if final['away_red_card'] != 0: ro_p += str(final['away_red_card']).count(',') + 1

        # tipo de definicion del partido
        tipo_def = "Tiempo Regular"
        p_p, e_p, r_p = 0, 0, 0 
        if "penalty" in nota:
            tipo_def = "Penales"
            p_p = 1
        elif "extra time" in nota:
            tipo_def = "Tiempo Extra"
            e_p = 1
        else:
            r_p = 1

        goles_p = final['home_score'] + final['away_score']
        
        resumen_dict = {
            "año": año,
            "equipos": f"{final['home_team']} vs {final['away_team']}",
            "resultado": f"{int(final['home_score'])} - {int(final['away_score'])}",
            "tipo_def": tipo_def,
            "disciplina": f"{am_p} Am / {ro_p} Ro"
        }

       
        if 1978 <= año <= 1998:
            num_finales_20 += 1
            goles_20 += goles_p
            amarillas_20 += am_p
            rojas_20 += ro_p
            penales_20 += p_p
            extra_20 += e_p
            regular_20 += r_p
            detalle_20.append(resumen_dict)
            
        elif 2002 <= año <= 2022:
            num_finales_21 += 1
            goles_21 += goles_p
            amarillas_21 += am_p
            rojas_21 += ro_p
            penales_21 += p_p
            extra_21 += e_p
            regular_21 += r_p
            detalle_21.append(resumen_dict)

    #configuracion de los graficos para modo oscuri
    ## rcParams.update: Configura el estilo global de Matplotlib (colores de texto, ejes y fondo).
    BG_COLOR = '#1e1e1e'

    # grafico 1: comparativa siglo XX vs XXI
    plt.figure(figsize=(8, 5))
    # Forzamos el color del "cuadradito" del gráfico
    plt.gca().set_facecolor(BG_COLOR) 
    #gca: agarra la parte de adentro del cuadro
    #set facecolor: pinta esa parte de adentro.
    
    categorias = ["Siglo XX", "Siglo XXI"]
    total_goles = [goles_20, goles_21]
    total_tarjetas = [amarillas_20 + rojas_20, amarillas_21 + rojas_21]
    x = np.arange(len(categorias))
    ancho = 0.35

    plt.bar(x - ancho/2, total_goles, ancho, label="Goles Totales", color="#00d4ff", edgecolor="white")
    plt.bar(x + ancho/2, total_tarjetas, ancho, label="Tarjetas Totales", color="#ff4d4d", edgecolor="white")
    
    plt.title('Comparativa de Goles y Tarjetas por Siglo', color='white')
    plt.xticks(x, categorias, color='white')
    plt.yticks(color='white')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    plt.savefig('static/grafico_comparativo.png', facecolor=BG_COLOR)
    plt.close()

    # grafico 2: siglo XX
    plt.figure(figsize=(6, 4))
    plt.gca().set_facecolor(BG_COLOR)
    plt.bar(['Goles', 'Amarillas', 'Rojas'], [goles_20, amarillas_20, rojas_20], color=['#00f2ff', '#fbff00', '#ff0055'], edgecolor="white")
    plt.title('Estadísticas Siglo XX (1978-1998)', color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.savefig('static/grafico_siglo20.png', facecolor=BG_COLOR)
    plt.close()

    # grafico 3: siglo 21
    plt.figure(figsize=(6, 4))
    plt.gca().set_facecolor(BG_COLOR)
    plt.bar(['Goles', 'Amarillas', 'Rojas'], [goles_21, amarillas_21, rojas_21], color=['#00d4ff', '#fbff00', '#ff0055'], edgecolor="white")
    plt.title('Estadísticas Siglo XXI (2002-2022)', color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.savefig('static/grafico_siglo21.png', facecolor=BG_COLOR)
    plt.close()

    # grafico 4: tipo de definicion total
    plt.figure(figsize=(6, 4))
    plt.gca().set_facecolor(BG_COLOR)
    plt.bar(['Regular', 'T. Extra', 'Penales'], [regular_20+regular_21, extra_20+extra_21, penales_20+penales_21], color='#39ff14', edgecolor="white")
    plt.title('Cómo se definieron las Finales (Total)', color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.savefig('static/grafico_definiciones.png', facecolor=BG_COLOR)
    plt.close()

    return {
        "siglo20": {
            "goles_totales": goles_20,
            "promedio_goles": round(goles_20 / num_finales_20, 2) if num_finales_20 > 0 else 0,
            "amarillas": amarillas_20,
            "rojas": rojas_20,
            "definiciones": {"regular": regular_20, "extra": extra_20, "penales": penales_20},
            "partidos": detalle_20 
        },
        "siglo21": {
            "goles_totales": goles_21,
            "promedio_goles": round(goles_21 / num_finales_21, 2) if num_finales_21 > 0 else 0,
            "amarillas": amarillas_21,
            "rojas": rojas_21,
            "definiciones": {"regular": regular_21, "extra": extra_21, "penales": penales_21},
            "partidos": detalle_21
        }
    }