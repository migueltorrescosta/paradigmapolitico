import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Paradigma Politico", page_icon="⚛️", layout="wide")

# Colours the five answer buttons, from "Discordo totalmente" to "Concordo totalmente".
st.markdown(
    """
    <style>
    .st-key-answers button { color: #FFFFFF; border: none; }
    .st-key-answers [data-testid="stColumn"]:nth-child(1) button { background-color: #8B0000; }
    .st-key-answers [data-testid="stColumn"]:nth-child(2) button { background-color: #FF6347; }
    .st-key-answers [data-testid="stColumn"]:nth-child(3) button { background-color: #FFD700; color: #000000; }
    .st-key-answers [data-testid="stColumn"]:nth-child(4) button { background-color: #556B2F; }
    .st-key-answers [data-testid="stColumn"]:nth-child(5) button { background-color: #006400; }
    </style>
    """,
    unsafe_allow_html=True,
)

# The CSV lists 20 economic, then 20 social, then 20 political questions.
AXIS_SIZE = 20
OPTIONS = {"Discordo totalmente": -2, "Discordo parcialmente": -1, "Neutro ou Ambíguo": 0, "Concordo parcialmente": 1, "Concordo totalmente": 2}

party_answers = pd.read_csv("paradigma_politico.csv", index_col="Pergunta")
multipliers = party_answers.pop("Multiplicador")
is_short = party_answers.pop("Curto") == 1
questions = party_answers.index.tolist()
short_questions = party_answers.index[is_short].tolist()
# The full test asks the short questions first, so "Continuar Teste" carries on from the short test.
full_questions = short_questions + party_answers.index[~is_short].tolist()

# Party details as of April 2025.
PARTIES = {
    "AD": {
        "cor": "orange",
        "site": "https://ad2024.pt/",
        "partido": "Aliança Democrática - Coligação PPD-PSD/CDS-PP",
        "lider": "Luís Montenegro (Presidente PPD/PSD)",
        "fundacao": "PPD/PSD: 6 de maio de 1974 (Coligação AD reeditada em 2023)",
        "espectro": "Centro-direita",
        "ideologias": "Conservadorismo Liberal, Democracia Cristã, Liberalismo Económico",
        "prioridades": "Redução de Impostos (IRS/IRC), Manutenção do Estado Social, Crescimento Económico, Controlo da Dívida Pública",
        "descricao": "Coligação de centro-direita liderada pelo Partido Social Democrata (PPD/PSD), integrando também o CDS-PP. Defende uma economia de mercado com responsabilidade social, reformas para aumentar a competitividade e a estabilidade governativa.",
        "programa_url": "https://ad2025.pt/programa-eleitoral/",
        "wiki_url": "https://pt.wikipedia.org/wiki/AD_%E2%80%94_ALIAN%C3%87A_DEMOCR%C3%81TICA_(2024-Presente)",
    },
    "ADN": {
        "cor": "darkgrey",
        "site": "https://adn.com.pt/",
        "partido": "Alternativa Democrática Nacional",
        "lider": "Bruno Fialho (Presidente)",
        "fundacao": "2015 (como PDR), 2021 (ADN)",
        "espectro": "Extrema-direita",
        "ideologias": "Conservadorismo, Nacionalismo, Anti-globalismo, Anti-establishment",
        "prioridades": "Combate à corrupção, Redução do Estado, Soberania Nacional, Anti-vacinas , Oposição a 'agendas globais'",
        "descricao": "Anterior Partido Democrático Republicano. Partido conservador e nacionalista, muito crítico do sistema político atual, do papel do estado na sociedade, de organizações/agendas internacionais (Organizaçãp Mundial da Saúde, clima, etc.) e de consensos científicos.",
        "programa_url": "https://adn.com.pt/programa-eleitoral/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Alternativa_Democr%C3%A1tica_Nacional",
    },
    "BE": {
        "cor": "#FFC0CB",
        "site": "https://www.bloco.org/",
        "partido": "Bloco de Esquerda",
        "lider": "Mariana Mortágua (Coordenadora)",
        "fundacao": "1999",
        "espectro": "Extrema-esquerda",
        "ideologias": "Socialismo, Anti-capitalismo, Progressismo, Direitos das Minorias",
        "prioridades": "Reforço dos Serviços Públicos (SNS, Escola), Direitos Laborais, Redistribuição dos rendimentos, Nacionalizações",
        "descricao": "Partido de esquerda radical, crítico do liberalismo e defensor de alternativas socialistas e ecológicas. Resultou da fusão de vários movimentos de esquerda. Forte ênfase nos direitos das minorias e na justiça social.",
        "programa_url": "https://www.bloco.org/programa",
        "wiki_url": "https://pt.wikipedia.org/wiki/Bloco_de_Esquerda",
    },
    "CDU": {
        "cor": "#EE0000",
        "site": "https://www.cdu.pt/",
        "partido": "Coligação Democrática Unitária (Partido Comunista Português + Partido Ecologista Os Verdes)",
        "lider": "Paulo Raimundo (Secretário-Geral PCP)",
        "fundacao": "PCP: 1921 (Coligação CDU: 1987)",
        "espectro": "Extrema-esquerda",
        "ideologias": "Comunismo (Marxismo-Leninismo - PCP), Ecossocialismo (PEV)",
        "prioridades": "Direitos dos Trabalhadores, Serviços Públicos Universais e Gratuitos, Nacionalizações, Soberania Nacional, Oposição à NATO e União Europeia",
        "descricao": "Aliança permanente entre o Partido Comunista Português (PCP) e o Partido Ecologista \"Os Verdes\" (PEV). Defende os interesses dos trabalhadores, o reforço do sector público e a soberania nacional. O PCP mantém uma linha marxista-leninista.",
        "programa_url": "https://www.cdu.pt/legislativas2025/compromisso-eleitoral-do-pcp",
        "wiki_url": "https://pt.wikipedia.org/wiki/Coliga%C3%A7%C3%A3o_Democr%C3%A1tica_Unit%C3%A1ria",
    },
    "Chega": {
        "cor": "blue",
        "site": "https://partidochega.pt/",
        "partido": "Chega",
        "lider": "André Ventura (Presidente)",
        "fundacao": "2019",
        "espectro": "Extrema-direita",
        "ideologias": "Conservadorismo cristão, Nacionalismo, Anti-imigração, Anti-corrupção",
        "prioridades": "Diminuição da Imigração, Combate à Corrupção e ao Sistema, Reforço da Segurança e Autoridade do Estado, Redução de Impostos",
        "descricao": "Partido de direita radical com discurso centrado na defesa da identidade nacional, segurança, críticas ao sistema político e posições anti-imigração. Defende valores conservadores, nacionalistas e liberalismo económico.",
        "programa_url": "https://partidochega.pt/programa/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Chega_(partido_pol%C3%ADtico)",
    },
    "IL": {
        "cor": "cyan",
        "site": "https://iniciativaliberal.pt/",
        "partido": "Iniciativa Liberal",
        "lider": "Rui Rocha (Presidente)",
        "fundacao": "2017",
        "espectro": "Direita",
        "ideologias": "Liberalismo (Clássico e Económico), Libertarianismo (influências)",
        "prioridades": "Redução de Impostos e Burocracia, Liberdade Económica e Individual, Reforma do Estado, Privatizações",
        "descricao": "Partido liberal que defende uma intervenção limitada do Estado na economia e na sociedade. Propõe a liberalização e desregulação do mercado, privatização da maioria das empresas públicas, impostos significativamente mais baixos e maior liberdade de escolha individual.",
        "programa_url": "https://iniciativaliberal.pt/programas/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Iniciativa_Liberal",
    },
    "JPP": {
        "cor": "#7FFFD4",
        "site": "https://juntospelopovo.pt/",
        "partido": "Juntos Pelo Povo",
        "lider": "Lina Pereira (Presidente), Élvio Sousa (Secretário Geral)",
        "fundacao": "2015",
        "espectro": "Centro (Regionalista)",
        "ideologias": "Regionalismo (Madeira), Social-democracia (local), Liberalismo, Autonomismo",
        "prioridades": "Interesses da Madeira, Regionalismo, Centrismo, Transparência",
        "descricao": "Partido com forte base na Madeira, focado na defesa dos interesses da região e na luta por maior autonomia. Adota posições pragmáticas e de centro localmente.",
        "programa_url": "https://juntospelopovo.pt/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Juntos_pelo_Povo",
    },
    "Livre": {
        "cor": "#7FFF00",
        "site": "https://partidolivre.pt/",
        "partido": "Livre",
        "lider": "Rui Tavares, Isabel Mendes Lopes (Porta-vozes)",
        "fundacao": "2014",
        "espectro": "Esquerda",
        "ideologias": "Socialismo, Progressismo, Ecologia, Europeísmo, Direitos das Minorias",
        "prioridades": "Redistribuição de Rendimentos, Combate às Alterações Climáticas, Direitos de Minorias, Habitação, Rendimento Básico Incondicional (RBI)",
        "descricao": "Partido de esquerda com forte ênfase na ecologia, direitos humanos, aprofundamento democrático e maior integração europeia. Defende políticas sociais inclusivas e um modelo económico socialista e com enfâse na sustentabilidade. Conhecido pelo seu modelo de liderança com porta-vozes rotativos.",
        "programa_url": "https://programa.partidolivre.pt/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Livre_(partido_pol%C3%ADtico)",
    },
    "Nova Direita": {
        "cor": "lightskyblue",
        "site": "https://novadireita.pt/",
        "partido": "Nova Direita",
        "lider": "Ossanda Liber (Presidente)",
        "fundacao": "2023",
        "espectro": "Direita",
        "ideologias": "Conservadorismo cristão, Anti-imigração, Liberalismo económico, Nacionalismo",
        "prioridades": "Diminuição da imigração, Redução de impostos, Segurança, Defesa da família tradicional, Controlo da Dívida Pública",
        "descricao": "Partido fundado por dissidentes do CDS-PP. Apresenta-se como conservador nos costumes e liberal na economia, defendendo valores da direita.",
        "programa_url": "https://novadireita.pt/legislativas-2025/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Nova_Direita_(Portugal)",
    },
    "PAN": {
        "cor": "forestgreen",
        "site": "https://2024.pan.com.pt/",
        "partido": "Pessoas-Animais-Natureza",
        "lider": "Inês Sousa Real (Porta-Voz)",
        "fundacao": "2011",
        "espectro": "Centro-esquerda",
        "ideologias": "Ambientalismo, Direitos dos Animais, Humanismo",
        "prioridades": "Proteção Animal e Ambiental, Saúde Única (Humana/Animal/Ambiental), Combate às Alterações Climáticas, Direitos Humanos",
        "descricao": "Partido Pessoas-Animais-Natureza, focado na defesa dos direitos dos animais e na proteção ambiental como eixos centrais. Promove políticas de sustentabilidade, bem-estar animal, preservação dos ecosistemas e economia verde. Geralmente alinha com o centro-esquerda em questões sociais.",
        "programa_url": "https://2024.pan.com.pt/program",
        "wiki_url": "https://pt.wikipedia.org/wiki/Pessoas%E2%80%93Animais%E2%80%93Natureza",
    },
    "PCTP/MRPP": {
        "cor": "#8B2323",
        "site": "https://www.pctpmrpp.com/",
        "partido": "Partido Comunista dos Trabalhadores Portugueses",
        "lider": "Liderança coletiva",
        "fundacao": "1970 (MRPP), 1976 (PCTP/MRPP)",
        "espectro": "Extrema-esquerda",
        "ideologias": "Comunismo, Marxismo-Leninismo, Maoismo",
        "prioridades": "Revolução socialista, Ditadura do proletariado, Anti-imperialismo",
        "descricao": "Partido de linha maoista, mantém discurso revolucionário clássico que advoga a nacionalização dos meios de produção.",
        "programa_url": "https://www.pctpmrpp.com/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Partido_Comunista_dos_Trabalhadores_Portugueses",
    },
    "PS": {
        "cor": "#FF1493",
        "site": "https://ps.pt/",
        "partido": "Partido Socialista",
        "lider": "Pedro Nuno Santos (Secretário-Geral)",
        "fundacao": "19 de abril de 1973",
        "espectro": "Centro-esquerda",
        "ideologias": "Social-democracia, Europeísmo",
        "prioridades": "Reforço do Estado Social (SNS, Educação), Redistribuição de Rendimentos, Europeísmo",
        "descricao": "Principal partido de centro-esquerda em Portugal, defensor do estado social e membro do Partido Socialista Europeu. Procura equilibrar políticas sociais com crescimento económico sustentável.",
        "programa_url": "https://ps.pt/programa/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Partido_Socialista_(Portugal)",
    },
    "RIR": {
        "cor": "yellow",
        "site": "https://partido-rir.pt/",
        "partido": "Reagir-Incluir-Reciclar",
        "lider": "Márcia Henriques (Presidente)",
        "fundacao": "2019",
        "espectro": "Centro",
        "ideologias": "Centrismo, Humanismo, Reformismo, Descentralização, Ecologia",
        "prioridades": "Reforma do sistema político/justiça, Transparência, Combate à corrupção",
        "descricao": "Apresenta-se como alternativa aos partidos de centro esquerda e centro direita, com foco na reforma do sistema de justiça e político de forma a aumentar a transparência e a representatividade democrática. Adota posições geralmente moderadas noutras áreas.",
        "programa_url": "https://partido-rir.pt/",
        "wiki_url": "https://pt.wikipedia.org/wiki/Reagir_Incluir_Reciclar",
    },
    "Volt": {
        "cor": "purple",
        "site": "https://voltportugal.org/",
        "partido": "Volt Portugal",
        "lider": "Duarte Costa, Inês Bravo Figueiredo (Co-Presidentes)",
        "fundacao": "2020",
        "espectro": "Centro",
        "ideologias": "Liberalismo Social, Progressismo, Federalismo Europeu, Ecologia",
        "prioridades": "Reforma da UE, Transição digital e climática, Políticas sociais pragmáticas, Direitos Humanos",
        "descricao": "Secção portuguesa do movimento pan-europeu Volt Europa. Defende uma economia de mercado livre complementada com um estado social forte com base em políticas progressistas e baseadas em evidência científica e em melhores práticas. Defende uma União Europeia mais integrada e democrática.",
        "programa_url": "https://voltportugal.org/programa",
        "wiki_url": "https://pt.wikipedia.org/wiki/Volt_Portugal",
    },
}


def reset(mode="intro"):
    st.session_state.update(mode=mode, idx=0, answers={})


def answer(question, value, question_list):
    s = st.session_state
    if value is None:
        s.answers.pop(question, None)
    else:
        s.answers[question] = value
    s.idx += 1
    if s.idx == len(question_list):
        s.mode = "midpoint" if s.mode == "short" else "results"


def go_back():
    st.session_state.idx -= 1


def set_mode(mode):
    st.session_state.mode = mode


def show_intro():
    st.title("Paradigma Político")
    st.write(
        f"""
        Bem-vindo! Este teste visa **avaliar o seu posicionamento político**. O teste compara também o seu posicionamento em relação aos partidos portugueses que tiveram mais do que 7000 votos nas eleições legislativas de 2024 (mínimo de assinaturas para a formação de um partido político em Portugal).
        
        Em cada pergunta, o utilizador será confrontado com uma afirmação e será pedido para escolher qual o nível de concordância. As perguntas visam avaliar a posição relativamente a valores políticos abstractos e intemporais, não a questões especificas da realidade portuguesa num determinado ponto no tempo.
        
        O teste completo é composto por **60 perguntas** (20 perguntas por eixo). A descrição de cada um destes eixos é a seguinte:
        
        - **Eixo Económico**: Mede o grau de intervenção geral do Estado na Economia. Espectro Esquerda-Direita.
        - **Eixo Social**: Mede o grau de abertura a mudanças sociais. Espectro Conservador-Progressista.
        - **Eixo Político**: Mede o grau de liberalismo político. Espectro Autoritário-Liberal.
        
        Os resultados do teste mostram o posicionamento relativamente aos vários partidos políticos portugueses nos 3 eixos através de um mapa com 3 dimensões.
        
        Os resultados mostram também o grau de semelhança das resposta do utilzador em relação a cada partido, medido pela soma dos desvios absolutos em todas as respostas do teste.
        
        Pode optar por fazer um teste **curto de {len(short_questions)} perguntas** (resultados mais rápidos mas menos precisos) ou o teste **completo de {len(questions)} perguntas** (resultados mais fiáveis).
        ---
        """
    )
    col1, col2 = st.columns(2)
    col1.button(f"Iniciar Teste Curto ({len(short_questions)} Perguntas)", on_click=reset, args=("short",))
    col2.button(f"Iniciar Teste Completo ({len(questions)} Perguntas)", on_click=reset, args=("full",))
    st.write("---")
    st.markdown("**Partidos incluídos:** " + " | ".join(f"[{p}]({d['site']})" for p, d in PARTIES.items()))
    st.write("As respostas dos partidos são baseadas na avaliação da equipa que elaborou o teste tendo em conta os conteúdos dos mais recententes programas, posições públicas passadas, e a ideologia de cada partido (dados de abril de 2025). A equipa encontra-se disponível para ajustar as respostas de cada partido, caso os partidos entrem em contacto.")


def show_question(question_list):
    i = st.session_state.idx
    question = question_list[i]
    st.header(f"Pergunta {i + 1} de {len(question_list)}")
    st.subheader(question)
    st.write("Qual a sua posição sobre esta afirmação?")
    with st.container(key="answers"):
        for col, (label, value) in zip(st.columns(5), OPTIONS.items()):
            col.button(label, on_click=answer, args=(question, value, question_list), width="stretch")
    st.button("Sem opinião", on_click=answer, args=(question, None, question_list), width="stretch")
    if i > 0:
        st.button("Recuar", on_click=go_back, width="stretch")


def show_midpoint():
    st.header(f"Teste Curto ({len(short_questions)} Perguntas) Concluído!")
    st.write("Pode ver já os seus resultados (baseados nestas perguntas, menos precisos) ou continuar o teste para responder a todas as perguntas e obter resultados mais fiáveis.")
    st.write("---")
    col1, col2 = st.columns(2)
    col1.button(f"Ver Resultados ({len(short_questions)} Perguntas)", on_click=set_mode, args=("results",))
    col2.button(f"Continuar Teste ({len(questions)} Perguntas)", on_click=set_mode, args=("full",))


def compass_scores(entity_answers):
    """Economic, social and political scores in [-1, 1], over the answered questions of each axis."""
    scores = []
    for start in range(0, 3 * AXIS_SIZE, AXIS_SIZE):
        answered = entity_answers.reindex(questions[start:start + AXIS_SIZE]).dropna()
        weighted = (answered * multipliers[answered.index]).sum()
        scores.append(weighted / (2 * len(answered)) if len(answered) else 0.0)
    return scores


def show_results():
    st.success("Teste concluído!")
    answers = pd.Series(st.session_state.answers)
    if answers.empty:
        st.warning("Não respondeu a nenhuma pergunta.")
        st.button("Reiniciar Teste", on_click=reset)
        return
    st.info(f"Resultados baseados em {len(answers)} perguntas respondidas.")

    st.header("Percentagem de Concordância com os Partidos Portugueses")
    distance = party_answers.loc[answers.index].sub(answers, axis=0).abs().sum()
    affinity = (1 - distance / (4 * len(answers))).sort_values(ascending=False)
    affinity_df = affinity.rename_axis("Partido").reset_index(name="Concordância")
    affinity_chart = alt.Chart(affinity_df).mark_bar().encode(
        x=alt.X("Concordância", axis=alt.Axis(format="%", title="Percentagem de Concordância", grid=False)),
        y=alt.Y("Partido", sort="-x", title="Partido", axis=alt.Axis(labelLimit=200)),
        color=alt.Color("Partido", scale=alt.Scale(domain=list(PARTIES), range=[d["cor"] for d in PARTIES.values()]), legend=None),
        tooltip=["Partido", alt.Tooltip("Concordância", format=".1%")],
    )
    st.altair_chart(affinity_chart, width="stretch")
    st.write("O gráfico acima mostra a concordância geral com base em todas as suas respostas. Quanto mais distante a resposta do utilizador da resposta de um determinado partido, menor o grau de semelhança. Um resultado de 100% indica uma concordância total com um determinado partido em todas as perguntas.")
    st.caption("Os resultados devem ser interpretados tendo em consideração as limitações do teste. O teste dá o mesmo peso a todas as afirmações, o que normalmente não reflete as preferências dos eleitores. Assim, é útil considerar não apenas o partido com maior percentagem de semelhança, mas também os partidos com percentagens próximas, já que podem ter maior concordância em temas mais relevantes para o utilizador. ")
    st.write("---")

    st.header("Bússola Política")
    entities = {"Você": compass_scores(answers)} | {p: compass_scores(party_answers[p]) for p in PARTIES}
    compass_df = pd.DataFrame.from_dict(entities, orient="index", columns=["Eixo Económico", "Eixo Social", "Eixo Político"]).rename_axis("Entidade").reset_index()
    origin_lines = pd.DataFrame({"zero": [0]})
    vline = alt.Chart(origin_lines).mark_rule(strokeDash=[3, 3], color="grey", size=0.5).encode(x="zero:Q")
    hline = alt.Chart(origin_lines).mark_rule(strokeDash=[3, 3], color="grey", size=0.5).encode(y="zero:Q")
    base = alt.Chart(compass_df).encode(
        x=alt.X("Eixo Económico", scale=alt.Scale(domain=[-1.1, 1.1]), axis=alt.Axis(title="Económico (Esquerda <-> Direita)", grid=False, format=".1f")),
        y=alt.Y("Eixo Social", scale=alt.Scale(domain=[-1.1, 1.1]), axis=alt.Axis(title="Social (Conservador <-> Progressista)", grid=False, format=".1f")),
    )
    color_scale = alt.Scale(domain=[-1, 0, 1], range=["#FF0000", "#808080", "#FFFF00"])
    points = base.mark_point(size=120, filled=True, opacity=0.9).encode(
        color=alt.Color("Eixo Político", scale=color_scale, legend=alt.Legend(title="Eixo Político", orient="top", titleOrient="left", gradientLength=200, format=".1f")),
        tooltip=["Entidade", alt.Tooltip("Eixo Económico", format=".2f"), alt.Tooltip("Eixo Social", format=".2f"), alt.Tooltip("Eixo Político", format=".2f", title="Político (Aut/Lib)")],
        shape=alt.condition(alt.datum.Entidade == "Você", alt.value("diamond"), alt.value("circle")),
    )
    text = base.mark_text(align="left", baseline="middle", dx=9, fontSize=12, fontWeight="bold").encode(text="Entidade", color=alt.value("#FFFFFF"))
    st.altair_chart((vline + hline + points + text).interactive(), width="stretch")
    st.write("""
        **Como interpretar a Bússola Política:**
        * **Posição Horizontal (Eixo X):** Eixo **Económico**. Esquerda (-1) vs Direita (+1).
        * **Posição Vertical (Eixo Y):** Eixo **Social**. Conservador (-1) vs Progressista (+1).
        * **Côr:** Eixo **Político**. Vermelho (Autoritário, -1) -> Cinzento (Neutro, 0) -> Amarelo (Liberal, +1).

        A sua posição ("Você") é marcada com um losango (♦). As posições são calculadas com base nas respostas.
        """)
    st.caption("Nota: Se as etiquetas se sobrepuserem, use o zoom ou passe o rato.")
    st.write("---")

    st.subheader("Descobre mais sobre os Partidos")
    st.caption("Dados de abril de 2025. Classificações de espectro, ideologias e prioridades são subjectivas e identificadas com ajuda de Inteligência Artificial (ChatGPT).")
    for name, d in PARTIES.items():
        with st.expander(name):
            st.markdown(f"""
**Partido/Coligação:** {d["partido"]}

**Líder(es) (ref. Abril 2025):** {d["lider"]}

**Fundação:** {d["fundacao"]}

**Espectro Político:** {d["espectro"]}

**Ideologias Associadas:** {d["ideologias"]}

**Prioridades:** {d["prioridades"]}

**Descrição:** {d["descricao"]}

**Links:**
- [Site Oficial]({d["site"]})
- [Programa Eleitoral]({d["programa_url"]})
- [Página Wikipedia]({d["wiki_url"]})
""")

    st.write("---")
    st.button("Reiniciar Teste", on_click=reset)


if "mode" not in st.session_state:
    reset()

match st.session_state.mode:
    case "intro":
        show_intro()
    case "short":
        show_question(short_questions)
    case "full":
        show_question(full_questions)
    case "midpoint":
        show_midpoint()
    case "results":
        show_results()
