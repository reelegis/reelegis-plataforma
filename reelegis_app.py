import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import numpy

# source venv/bin/activate
st.title('Devo reeleger meu candidato?')
st.subheader('Plataforma reeLegis')
st.text('Aqui você escolhe o/a seu/sua Deputado/a Federal!')
st.text("Versão beta 🐟")


## base de dados do político
@st.cache(ttl=60*60*24)
def load_data():
    data = pd.read_excel('bd-reeleicao-camara.xlsx', index_col=0)
    return data

df = load_data()

df = df.dropna() #lida com todos os espacos vazios dos dados

st.markdown(f'Agora em outubro, além de votar para presidente e governador, você também escolherá quem deve ocupar as cadeiras no Legislativo. Pensando nisso, a plataforma **reeLegis** ajuda você a observar o que os **deputados e deputadas federais que estão disputando a reeleição**. Ou seja, levamos em consideração apenas se o Deputado ou Deputada Federal estiver concorrendo à reeleição. Infelizmente os/as parlamentares que estão disputando, não foram considerados no cálculo individual, mas a sua produção foi levada em conta para o quantitativo do partido que esses fizeram parte, para que assim você analise quem mais apresentou as propostas sobre temas que você considera importante. Utilizando técnicas de aprendizado de máquina, após o tratamento e filtragem dos dados, obtivemos {len(df.index)} propostas legislativas apresentadas pelos parlamentares entre 2019 e 2022. Você pode consultar nossa metodologia [retornando ao nosso site principal](https://reelegis.netlify.app).')

st.markdown('Boa busca e esperamos que ajude na escolha de um voto mais consciente!')
#st.markdown(f'Número de casos {len(df.index)}')
# base de dados do partido

#@st.cache(ttl=60*60*24)
#def load_partido():
#    base_de_dados = pd.read_excel('bd_partido.xlsx', index_col=0)
#    return base

#base = load_partido()

#base = base.dropna()


## inicio do app


st.header('Nessas eleições, você prefere votar no Político ou no Partido para o cargo de Deputado/a Federal?')
pol_part = st.radio("Escolha uma opção", ['','Político', 'Partido', 'Ainda não decidi'], key='1')
df2 = df[df.nomeUrna != 'Não está concorrendo']
if pol_part == 'Político':
    st.header('Onde você vota?')
    uf = df2['estado'].unique()
    uf = np.append(uf, '')
    uf.sort()
    uf_escolha = st.selectbox("Identifique o Estado", uf)
    if uf_escolha != '':
        f_par2 = df2.loc[df2.estado == uf_escolha, :]
        f = pd.DataFrame(f_par2)
        perc = f.nomeUrna.value_counts() #/ len(f) * 100
        parlamentar_do_estado = f_par2['nomeUrna'].unique()
        parlamentar_do_estado = np.append(parlamentar_do_estado, '')
        parlamentar_do_estado.sort()
        escolha_parlamentar_do_estado = st.selectbox("Identifique o Parlamentar", parlamentar_do_estado)
        st.error(f'Caso você não encontre o/a Deputado/a do seu estado, isso é devido ao fato dele/a não estar concorrendo à reeleição, ou não apresentou propostas até o período de nossa coleta (18/julho/2022).')
        if escolha_parlamentar_do_estado != '':
            f_par23 = f_par2.loc[f_par2.nomeUrna == escolha_parlamentar_do_estado, :]
            f23 = pd.DataFrame(f_par23)
                    #f.nomeUrna = f.nomeUrna.astype('string')
            perc23 = f23.Tema.value_counts() / len(f23) * 100
                    #contar = f['nomeUrna'].value_counts()
                    #c = sum(contar)
                    #contar = contar/sum()
                    # filter_partido_proposi2 = f_par2.loc[f_par.autor_partido == choice_dep]
            st.header(f'Percentual de Temas apresentados por {escolha_parlamentar_do_estado}')
            estado_parla = px.bar(perc23, x='Tema', height=500,color='Tema',color_continuous_scale='Sunsetdark',
            # site com as cores: https://plotly.com/python/builtin-colorscales/
            labels=dict(index="Tema", Tema="Ênfase Temática"), orientation='h')
            estado_parla.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(estado_parla)

            n_proposta_uf = f_par23.index
            n_proposta_uf = len(n_proposta_uf)
            df_uf = pd.DataFrame(data=f_par23['Tema'].value_counts())
            df_uf['Tema'] = pd.to_numeric(df_uf['Tema'])
            saliente_uf = df_uf['Tema']
            gen_uf = pd.DataFrame(data=f_par23['genero'].value_counts())
            genero = gen_uf['genero']
            first = int(perc23.iloc[:1])
            last = perc23.iloc[:-1].round()

            st.write(f'Entre 2019 e 2022, {escolha_parlamentar_do_estado} apresentou {str(n_proposta_uf)} proposições legislativas. A maior ênfase temática d{genero.index[0]} foi {saliente_uf.index[0]}, com aproximadamente {first}% do total.')

            #st.subheader(f'Em comparação com os outros parlamentares de {uf_escolha}, {escolha_parlamentar_do_estado}')
            ## grafico destacado aqui!
            st.header('*Ranking* de Parlamentares propositivos')
            st.write(f'No gráfico a seguir, a barra em vermelho indica a posição de {escolha_parlamentar_do_estado} em comparação com os demais deputados federais da Unidade Federativa {uf_escolha} no que se refere à quantidade dos projetos apresentados.')
            #st.subheader(f'{escolha_parlamentar_do_estado}')
            contagem_parlamentares = f.groupby(f.nomeUrna.tolist(),as_index=False).size()
            #st.table(contagem_parlamentares)

            #st.table(perc)
            condicao_split_parlamentar = len(contagem_parlamentares.index)
            if condicao_split_parlamentar > 40:
                #parl_dep = px.bar(perc, x='nomeUrna', height=1500, width=900,
                #labels=dict(index="Parlamentar", nomeUrna="% Propostas apresentadas"),
                #orientation='h')
                fig1=px.bar(perc, height=1500, width=900, labels=dict(index="Parlamentar", value='Quantidade de propostas apresentadas'), orientation='h')
                fig1["data"][0]["marker"]["color"] = ["red" if c == escolha_parlamentar_do_estado else "#C0C0C0" for c in fig1["data"][0]["y"]]
                fig1.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig1)

                first = perc.iloc[:1].round()
                st.info(f'Na Unidade Federativa {uf_escolha}, {perc.index[0]} foi quem mais apresentou propostas legislativas entre 2019 e 2022, com {first.to_string(index=False)} apresentadas até o dia 18 de julho de 2022.')
                #st.info('Caso queira visualizar a tabela descritiva do gráfico, clique abaixo.')


                ## conhecer as Propostas
                st.header(f'Conheça as propostas apresentadas por {escolha_parlamentar_do_estado}')
                #st.checkbox('Consultar propostas apresentadas deste Parlamentar por tema', False):
                tema = f_par23['Tema'].unique()
                tema = np.append(tema, '')
                tema.sort()
                random_tema = st.radio("Escolha o Tema", tema)
                if random_tema != '':
                    random_val = f_par23.loc[f_par23.Tema == random_tema, :]
                    sorteio = random_val.loc[random_val.Tema == random_tema]
                    maior = pd.DataFrame(sorteio[['ementa', 'maior_prob']]).max()
                    ementa_maior=maior.iloc[0]

                    probabilidade_maior=int((maior.iloc[1] * 100))

                    #st.write(probabilidade_maior)

                    #max_percent = max(sorteio['maior_prob'].items(), key=lambda i: i[1])
                    #st.write(max_percent)
                    ementa = pd.DataFrame(data=random_val['explicacao_tema'].value_counts())
                    st.write(ementa.index[0])
                    st.write(f'Este é um exemplo de proposta apresentada por {escolha_parlamentar_do_estado} sobre {random_tema}.')
                    #A probabilidade de pertencer ao tópico é de {probabilidade_maior}%.
                    st.success(ementa_maior)
                    #st.success(sorteio.query("Tema == @random_tema")[["ementa", "keywords"]].sample(n=1).iat[0, 0])

                #grafico_parlamentar_maior = px.bar(perc, x='nomeUrna', height=1500, width=900, #color='nomeUrna',
                #    labels=dict(index="Parlamentar", nomeUrna="% Propostas apresentadas"),
                #    orientation='h')
                #grafico_parlamentar_maior.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})

                #st.plotly_chart(grafico_parlamentar_maior)
                #first = perc.iloc[:1].round()
                #last = perc.iloc[:-1].round()
                #st.write(perc.index[0], "foi quem mais apresentou propostas no Estado selecionado, contando com aproximadamente",
                #first.to_string(index=False) + '% em relação a todos os parlamentares na Unidade Federativa', uf_escolha +
                #'.') # Em contrapartida,', perc.index[-1])
                #st.info('Caso queira visualizar a tabela descritiva do gráfico, clique abaixo.')
            else:
                #parl_dep = px.bar(perc, x='nomeUrna', height=600, width=700,
                #labels=dict(index="Parlamentar", nomeUrna="% Propostas apresentadas"),
                #orientation='h')
                fig1=px.bar(perc, height=600, width=700, labels=dict(index="Parlamentar", value='Quantidade de propostas apresentadas'), orientation='h')
                fig1["data"][0]["marker"]["color"] = ["red" if c == escolha_parlamentar_do_estado else "#C0C0C0" for c in fig1["data"][0]["y"]]
                fig1.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig1)

                first = perc.iloc[:1].round()
                st.info(f'Na Unidade Federativa {uf_escolha}, {perc.index[0]} foi quem mais apresentou propostas legislativas entre 2019 e 2022, com {first.to_string(index=False)} apresentadas até o dia 18 de julho de 2022.')
                #st.info('Caso queira visualizar a tabela descritiva do gráfico, clique abaixo.')


                ## conhecer as Propostas
                st.header(f'Conheça as propostas apresentadas por {escolha_parlamentar_do_estado}')
                #st.checkbox('Consultar propostas apresentadas deste Parlamentar por tema', False):
                tema = f_par23['Tema'].unique()
                tema = np.append(tema, '')
                tema.sort()
                random_tema = st.radio("Escolha o Tema", tema)
                if random_tema != '':
                    random_val = f_par23.loc[f_par23.Tema == random_tema, :]
                    sorteio = random_val.loc[random_val.Tema == random_tema]
                    maior = pd.DataFrame(sorteio[['ementa', 'maior_prob']]).max()
                    ementa_maior=maior.iloc[0]
                    probabilidade_maior=int((maior.iloc[1] * 100))
                    #st.write(probabilidade_maior)

                    #max_percent = max(sorteio['maior_prob'].items(), key=lambda i: i[1])
                    #st.write(max_percent)
                    ementa = pd.DataFrame(data=random_val['explicacao_tema'].value_counts())
                    st.write(ementa.index[0])
                    st.write(f'Este é um exemplo de proposta apresentada por {escolha_parlamentar_do_estado} sobre {random_tema}.')
                    #A probabilidade de pertencer ao tópico é de {probabilidade_maior}%.
                    st.success(ementa_maior)
                    #st.success(sorteio.query("Tema == @random_tema")[["ementa", "keywords"]].sample(n=1).iat[0, 0])
                st.header('📢  Conta pra gente!')
                st.warning('Fique à vontade para nos informar sobre algo que queria ter visto nesta aba ou sobre a plataforma, para melhorarmos no futuro!')
                contact_form = """
                <form action="https://formsubmit.co/renata.aguiar@ufpe.br" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Nome" required>
                <input type="email" name="email" placeholder="E-mail" required>
                <textarea name="message" placeholder="Sua mensagem"></textarea>
                <button type="submit">Enviar</button>
                </form>
                """
                st.markdown(contact_form, unsafe_allow_html=True)

                def local_css(file_name):
                    with open(file_name) as f:
                        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
                local_css("style.css")

if pol_part == 'Partido':
    st.header('Onde você vota?')
    uf = df['estado'].unique()
    uf = np.append(uf, '')
    uf.sort()
    uf_escolha = st.selectbox("Identifique o Estado", uf)
    if uf_escolha != '':
        f_par2 = df.loc[df.estado == uf_escolha, :]
        f = pd.DataFrame(f_par2)
        perc = f.nomeUrna.value_counts() #/ len(f) * 100
        partido_do_estado = f_par2['partido_ext_sigla'].unique()
        partido_do_estado = np.append(partido_do_estado, '')
        partido_do_estado.sort()
        escolha_partido_do_estado = st.selectbox("Identifique o Partido", partido_do_estado)
        st.error(f'Alguns partidos podem não ter sido eleitos na Unidade Federativa {uf_escolha}.')
        if escolha_partido_do_estado != '':
            f_par23 = f_par2.loc[f_par2.partido_ext_sigla == escolha_partido_do_estado, :]
            f23 = pd.DataFrame(f_par23)
                    #f.nomeUrna = f.nomeUrna.astype('string')
            perc23 = f23.Tema.value_counts() / len(f23) * 100
                    #contar = f['nomeUrna'].value_counts()
                    #c = sum(contar)
                    #contar = contar/sum()
                    # filter_partido_proposi2 = f_par2.loc[f_par.autor_partido == choice_dep]
            st.header(f'Percentual de Temas apresentados pelo {escolha_partido_do_estado}')
            estado_partido = px.bar(perc23, x='Tema', height=500,color='Tema',color_continuous_scale='Sunsetdark',
            # site com as cores: https://plotly.com/python/builtin-colorscales/
            labels=dict(index="Tema", Tema="Ênfase Temática"), orientation='h')
            estado_partido.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(estado_partido)

            n_proposta_uf = f_par23.index
            n_proposta_uf = len(n_proposta_uf)
            df_uf = pd.DataFrame(data=f_par23['Tema'].value_counts())
            saliente_uf = df_uf['Tema']
            first = int(perc23.iloc[:1])
            last = perc23.iloc[:-1].round()

            st.write(f'Entre 2019 e 2022, {escolha_partido_do_estado} apresentou {str(n_proposta_uf)} proposições legislativas na Unidade Federativa {uf_escolha}. A maior ênfase temática foi {saliente_uf.index[0]}, com aproximadamente {first}% do total.')

            f = pd.DataFrame(f_par2[['nomeUrna', 'partido_ext_sigla']])
            new = f.groupby(['partido_ext_sigla', 'nomeUrna']).size()#.groupby(['partido_ext_sigla']).size()
            g_sum = new.groupby(['partido_ext_sigla']).sum()
            n = new.groupby(['partido_ext_sigla']).size()
            per = pd.concat([g_sum, n], axis=1)
            percapita = per[0]/per[1]
            per_capita = pd.DataFrame(percapita)
            per_capita.columns=['Taxa per capita']
            #f_par23 = f_par2.loc[f_par2.partido_ext_sigla == escolha_partido_do_estado, :]
            #st.write(partido_selecionado)
            #st.table(per_capita)
            #estado_parla = px.bar(per_capita, x='Taxa per capita', height=500, labels=dict(partido_ext_sigla="Partido"),
            #orientation='h')
            st.header('*Ranking* de Partidos Políticos propositivos')
            st.write(f'A barra em vermelho indica a posição do {escolha_partido_do_estado}  em comparação com os demais partidos que possuem representantes na Câmara Federal da Unidade Federativa {uf_escolha} no que se refere aos projetos apresentados.')
            partido_selecionado = int(per_capita.loc[escolha_partido_do_estado])
            #st.write(partido_selecionado.index[0])
            #st.write(f'{partido_selecionado.to_string(index=False)}')
            st.write(f'O {escolha_partido_do_estado} apresentou, em média, {partido_selecionado} propostas por Parlamentar na Unidade Federativa {uf_escolha}.')
            #st.header(f'Taxa _per capita_ de propostas apresentadas pelo {escolha_partido_do_estado} na Unidade Federativa {uf_escolha}')
            fig_partido=px.bar(per_capita, height=600, width=700, labels=dict(partido_ext_sigla="Partido", value='Taxa per capita'), orientation='h')
            fig_partido["data"][0]["marker"]["color"] = ["red" if c == escolha_partido_do_estado else "#C0C0C0" for c in fig_partido["data"][0]["y"]]
            fig_partido.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_partido)


            #estado_parla.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})

            #st.plotly_chart(estado_parla)
            st.info('A taxa _per capita_ de projetos apresentados leva em consideração o total de projetos apresentados do partido neste estado dividido pela quantidade de seus parlamentares. A opção por esta métrica permite tornar os partidos comparáveis com base na quantidade de seus membros, não indicando necessariamente o valor total de projetos que foram apresentados pelo partido. ')

            partidos_per = pd.DataFrame(per_capita)
            partidos_per.columns=['Taxa per capita']
            reorder = partidos_per.sort_values(by = 'Taxa per capita', ascending = False)
            partidos_per.Taxa = pd.to_numeric(partidos_per['Taxa per capita'], errors='coerce')
            ppc = partidos_per.sort_values(by='Taxa per capita', ascending=False)
            #st.table(partidos_per)
            first= ppc.iloc[0]
            last = ppc.iloc[-1]
            st.info(f'Na Unidade Federativa, {uf_escolha} o partido com maior taxa _per capita_ é o {ppc.index[0]}, com {first.to_string(index=False)}. Isso indica que, em média, 1 parlamentar deste partido apresentou {first.to_string(index=False)} propostas. Em contrapartida, o {ppc.index[-1]} é o partido que menos apresentou propostas, com {last.to_string(index=False)} de taxa _per capita_ no Estado selecionado.')

            ## conhecer as Propostas
            st.header(f'Conheça as propostas apresentadas pelo {escolha_partido_do_estado}')
            #st.checkbox('Consultar propostas apresentadas deste Parlamentar por tema', False):
            tema = f_par23['Tema'].unique()
            tema = np.append(tema, '')
            tema.sort()
            random_tema = st.radio("Escolha o Tema", tema)
            if random_tema != '':
                random_val = f_par23.loc[f_par23.Tema == random_tema, :]
                sorteio = random_val.loc[random_val.Tema == random_tema]
                maior = pd.DataFrame(sorteio[['ementa', 'maior_prob']]).max()
                ementa_maior=maior.iloc[0]
                probabilidade_maior=int((maior.iloc[1] * 100))
                #st.write(probabilidade_maior)

                #max_percent = max(sorteio['maior_prob'].items(), key=lambda i: i[1])
                #st.write(max_percent)
                ementa = pd.DataFrame(data=random_val['explicacao_tema'].value_counts())
                st.write(ementa.index[0])
                st.write(f'Este é um exemplo de proposta apresentada pelo {escolha_partido_do_estado} sobre {random_tema}.')
                #A probabilidade de pertencer ao tópico é de {probabilidade_maior}%.
                st.success(ementa_maior)
                #st.success(sorteio.query("Tema == @random_tema")[["ementa", "keywords"]].sample(n=1).iat[0, 0])

            st.header('📢  Conta pra gente!')
            st.warning('Fique à vontade para nos informar sobre algo que queria ter visto nesta aba ou sobre a plataforma, para melhorarmos no futuro!')
            contact_form = """
            <form action="https://formsubmit.co/renata.aguiar@ufpe.br" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Nome" required>
            <input type="email" name="email" placeholder="E-mail" required>
            <textarea name="message" placeholder="Sua mensagem"></textarea>
            <button type="submit">Enviar</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)

            def local_css(file_name):
                with open(file_name) as f:
                    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            local_css("style.css")


if pol_part == 'Ainda não decidi':
    st.header('Onde você vota?')
    uf = df2['estado'].unique()
    uf = np.append(uf, '')
    uf.sort()
    uf_escolha = st.selectbox("Identifique o Estado", uf)
    if uf_escolha != '':
        tem_state = df2.loc[df2.estado == uf_escolha, :]
        tem_state_partido = df.loc[df.estado == uf_escolha, :]
        tem = df2['Tema'].unique()
        tem = np.append(tem, '')
        tem.sort()
        tema = st.selectbox("Escolha o tema que você dá mais importância", tem)
        if tema != '':
            random_val = tem_state.loc[tem_state.Tema == tema, :]
            cand_ideal = random_val.loc[random_val.Tema == tema]
            random_val_partido = tem_state_partido.loc[tem_state_partido.Tema == tema, :]
            cand_ideal_partido = random_val_partido.loc[random_val_partido.Tema == tema]
            ementa = pd.DataFrame(data=random_val['explicacao_tema'].value_counts())
            st.success(ementa.index[0])
            top_politico = cand_ideal['nomeUrna'].value_counts()
            toppol = pd.DataFrame(data=top_politico)

            top_partido = cand_ideal_partido['partido_ext_sigla'].value_counts()
            toppart = pd.DataFrame(data=top_partido)
            st.subheader(f'Político com maior ênfase temática em {tema}: {toppol.index[0]}')
            st.write(f'Na Unidade Federativa {uf_escolha}, {toppol.index[0]} foi quem mais apresentou propostas sobre {tema}. Em contrapartida, {toppol.index[-1]} foi quem apresentou menos propostas relacionadas a {tema}.')
            f = pd.DataFrame(cand_ideal['nomeUrna'])
            f2 = pd.DataFrame(cand_ideal_partido['partido_ext_sigla'])
            new = f2.groupby(['partido_ext_sigla']).size()#.groupby(['partido_ext_sigla']).size()
            g_sum = new.groupby(['partido_ext_sigla']).sum()
            n = new.groupby(['partido_ext_sigla']).size()
            per = pd.concat([g_sum, n], axis=1)
            percapita = per[0]/per[1]
            per_capita = pd.DataFrame(percapita)
            per_capita.columns=['Taxa per capita']
            p = per_capita.sort_values(by=['Taxa per capita'], ascending=False)
            st.subheader(f'Partido com maior ênfase temática em {tema}: {p.index[0]}')
            st.write(f'Levando em consideração a _taxa per capita_, na Unidade Federativa {uf_escolha}, o {p.index[0]} foi quem mais apresentou propostas sobre {tema}. Em contrapartida, {p.index[-1]} foi quem apresentou menos propostas relacionadas a {tema}.')
            st.info(f'A taxa _per capita_ de projetos apresentados leva em consideração o total de projetos apresentados do partido no tema {tema} dividido pela quantidade de seus parlamentares que também apresentaram propostas sobre o mesmo tema. A opção por esta métrica permite tornar os partidos comparáveis com base na quantidade de seus membros, não indicando necessariamente o valor total de projetos que foram apresentados pelo partido. ')

            st.header('📊 Comparativo')

            st.subheader(f'No tema sobre {tema}, {toppol.index[0]} apresentou maior ênfase temática que os outros Parlamentares na Unidade Federativa {uf_escolha}.')
            #parlamentar_tema_selecionado = per_capita.loc[escolha_partido_do_estado]
            t_first = toppol.iloc[:1].round()
            #tf = pd.DataFrame(data=t_first)
            #st.write(f'{toppol.index[0]} apresentou {t_first.to_string(index=False)} propostas sobre {tema}.')

            contagem_parlamentares = t_first.groupby(t_first.nomeUrna.tolist(),as_index=False).size()
#st.table(contagem_parlamentares)

#st.table(perc)
            condicao_split_parlamentar = len(contagem_parlamentares.index)
            if condicao_split_parlamentar < 35:
                fig_político=px.bar(toppol, height=1500, width=900, labels=dict(index="Político", value=f'Quantidade de propostas apresentadas sobre {tema}'), orientation='h')
                fig_político["data"][0]["marker"]["color"] = ["green" if c == toppol.index[0] else "#A9DFBF" for c in fig_político["data"][0]["y"]]
                fig_político.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_político)


                st.subheader(f'No tema sobre {tema}, o {p.index[0]} apresentou maior ênfase temática que os outros Partidos na Unidade Federativa {uf_escolha}')
                #st.write(f'O {p.index[0]} apresentou em média  propostas legislativas sobre {tema} por Parlamentar.')
                fig_partido=px.bar(p, height=600, width=700, labels=dict(partido_ext_sigla="Partido", value='Taxa per capita'), orientation='h')
                fig_partido["data"][0]["marker"]["color"] = ["green" if c == p.index[0] else "#A9DFBF" for c in fig_partido["data"][0]["y"]]
                fig_partido.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_partido)

            else:

                fig_político=px.bar(toppol, height=600, width=700, labels=dict(index="Político", value=f'Quantidade de propostas apresentadas sobre {tema}'), orientation='h')
                fig_político["data"][0]["marker"]["color"] = ["green" if c == toppol.index[0] else "#A9DFBF" for c in fig_político["data"][0]["y"]]
                fig_político.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_político)


                st.subheader(f'No tema sobre {tema}, o {p.index[0]} apresentou maior ênfase temática que os outros Partidos na Unidade Federativa {uf_escolha}')
            #st.write(f'O {p.index[0]} apresentou em média  propostas legislativas sobre {tema} por Parlamentar.')
                fig_partido=px.bar(p, height=600, width=700, labels=dict(partido_ext_sigla="Partido", value='Taxa per capita'), orientation='h')
                fig_partido["data"][0]["marker"]["color"] = ["green" if c == p.index[0] else "#A9DFBF" for c in fig_partido["data"][0]["y"]]
                fig_partido.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_partido)


            st.header('📢  Conta pra gente!')
            st.warning('Fique à vontade para nos informar sobre algo que queria ter visto nesta aba ou sobre a plataforma, para melhorarmos no futuro!')
            contact_form = """
            <form action="https://formsubmit.co/renata.aguiar@ufpe.br" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Nome" required>
            <input type="email" name="email" placeholder="E-mail" required>
            <textarea name="message" placeholder="Sua mensagem"></textarea>
            <button type="submit">Enviar</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)

            def local_css(file_name):
                with open(file_name) as f:
                    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            local_css("style.css")


            #st.table(topmin)
