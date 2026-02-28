import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db_functions import carregar_dados, executar_query
from fpdf import FPDF  # <-- Importação nova aqui

# ==========================================
# --- MOTOR GERADOR DE PDF ---
# ==========================================
def gerar_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    
    # Título do Relatório (Ajustado para 190mm de largura para centralizar perfeito)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, txt="Relatório Oficial - Inventário da Frota", ln=True, align='C')
    pdf.ln(10)
    
    # 💡 O TRUQUE: A soma dessas larguras agora dá exatamente 190mm (Largura útil do A4)
    pdf.set_font("Arial", 'B', 10)
    colunas = ['Placa', 'Marca', 'Modelo', 'Ano', 'Status']
    larguras = [35, 45, 50, 25, 35] 
    
    # Desenha os cabeçalhos
    for i, col in enumerate(colunas):
        pdf.cell(larguras[i], 10, str(col), border=1, align='C')
    pdf.ln()
    
    # Preenche os dados
    pdf.set_font("Arial", '', 10)
    for index, row in dataframe.iterrows():
        pdf.cell(larguras[0], 10, str(row.get('placa', '')).upper(), border=1, align='C')
        pdf.cell(larguras[1], 10, str(row.get('marca', '')).title(), border=1, align='C')
        pdf.cell(larguras[2], 10, str(row.get('modelo', '')).title(), border=1, align='C')
        pdf.cell(larguras[3], 10, str(row.get('ano', '')), border=1, align='C')
        pdf.cell(larguras[4], 10, str(row.get('status', '')).title(), border=1, align='C')
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')

# Configuração inicial da página (Seu código normal continua daqui pra baixo)
st.set_page_config(page_title="Gestão de Frota", layout="wide")
# ...

# ==========================================
# --- SISTEMA DE LOGIN ---
# ==========================================
# Cria a "memória" de autenticação se ela não existir
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# Se NÃO estiver autenticado, mostra a tela de Login
# Se NÃO estiver autenticado, mostra a tela de Login
if not st.session_state['autenticado']:
    
    # Criamos 3 colunas para empurrar o conteúdo para o meio
    st.write("") # Espaço em branco no topo para descer a tela um pouco
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Título centralizado usando HTML/Markdown
        st.markdown("<h2 style='text-align: center;'>🔐 Acesso ao Sistema de Frota</h2>", unsafe_allow_html=True)
        st.write("") # Espacinho de respiro
        
        with st.form("form_login"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            
            # Botão ocupando 100% da largura do formulário (visual premium)
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                # 💡 REGRA DE NEGÓCIO: Aqui você define o usuário e senha
                if usuario == "admin" and senha == "123":
                    st.session_state['autenticado'] = True
                    st.rerun() # Recarrega a página para liberar o sistema
                else:
                    st.error("⚠️ Usuário ou senha incorretos!")

# Se ESTIVER autenticado, mostra o sistema completo
else:
    # Botão de Logout no topo do menu lateral
    st.sidebar.markdown("### 👤 Olá, Admin!")
    if st.sidebar.button("🚪 Sair do Sistema"):
        st.session_state['autenticado'] = False
        st.rerun()
        
    st.sidebar.markdown("---")

    # Menu Lateral Seguro
    aba = st.sidebar.selectbox("Navegação do Sistema", [
        "Dashboard", 
        "Cadastrar Veículo", 
        "Gerenciar Frota", 
        "Registrar Manutenção", 
        "Gerenciar Manutenções"
    ])

    # ==========================================
    # --- AQUI COMEÇA O SEU CÓDIGO DO SISTEMA ---
    # ==========================================
    # IMPORTANTE: Selecione TUDO o que vem daqui para baixo (todos os seus ifs e elifs das abas)
    # e aperte TAB uma vez para que eles fiquem alinhados (indentados) DENTRO do 'else:'
    
    if aba == "Dashboard":
        st.title("📊 Painel de Controle e Inteligência de Frota")
        # ... resto do código do dashboard ...
        try:
            df_inv = carregar_dados("INVENTARIO")
            df_manut = carregar_dados("MANUTENCOES")
            
            # Normalização de colunas
            df_inv.columns = [str(c).lower() for c in df_inv.columns]
            df_manut.columns = [str(c).lower() for c in df_manut.columns]
            
            # Coluna Virtual: Cria o 'status' caso não exista no banco
            if 'status' not in df_inv.columns:
                df_inv['status'] = 'Ativo' # Define o padrão como Ativo
                
                # 💡 TRUQUE DE BI: Colocando veículos específicos em Manutenção
                # Placas que queremos destacar como indisponíveis no Dashboard 
                
                # Usamos o .loc do Pandas para localizar essas placas e alterar o status

                df_inv.columns = [str(c).lower() for c in df_inv.columns]
                df_manut.columns = [str(c).lower() for c in df_manut.columns]
            
            # KPIs
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("Total da Frota", len(df_inv))
            with c2: st.metric("Ativos", len(df_inv[df_inv['status'] == 'Ativo']))
            with c3: 
                em_manutencao = len(df_inv[df_inv['status'] == 'Manutenção'])
                st.metric("Em Manutenção", em_manutencao)

            # Gráficos de Operação
            if not df_inv.empty:
                col_graf1, col_graf2 = st.columns(2)
                with col_graf1:
                    fig_pizza = px.pie(df_inv, names='status', title="Saúde da Frota", hole=0.4)
                    st.plotly_chart(fig_pizza, use_container_width=True)
                with col_graf2:
                    if 'marca' in df_inv.columns:
                        fig_marca_cont = px.bar(df_inv, x='marca', title="Veículos por Marca", color='marca')
                        st.plotly_chart(fig_marca_cont, use_container_width=True)

            # ANÁLISE FINANCEIRA 
            st.markdown("---")
            st.subheader("💰 Análise de Custos")

            if not df_manut.empty and not df_inv.empty:
                # Cruzamento de tabelas pela placa
                df_cruzado = pd.merge(df_manut, df_inv, on='placa')
                
                if not df_cruzado.empty:
                    col_bi1, col_bi2 = st.columns(2)

                    with col_bi1:
                        custos_por_marca = df_cruzado.groupby('marca')['valor'].sum().reset_index()
                        fig_custos_marca = px.bar(
                            custos_por_marca, x='marca', y='valor',
                            title="Gasto Total por Marca (R$)", color='marca',
                            labels={'marca': 'Marca', 'valor': 'Custo Total'}
                        )
                        st.plotly_chart(fig_custos_marca, use_container_width=True)

                    with col_bi2:
                        custos_por_ano = df_cruzado.groupby('ano')['valor'].sum().reset_index()
                        fig_ano_fin = px.line(
                            custos_por_ano, x='ano', y='valor', markers=True,
                            title="Tendência de Gasto por Ano do Veículo"
                        )
                        st.plotly_chart(fig_ano_fin, use_container_width=True)
                else:
                    st.info("Nenhuma manutenção vinculada às placas atuais do inventário.")
            else:
                st.warning("⚠️ Registre veículos e manutenções para ativar os gráficos financeiros.")

                st.markdown("---")
            st.subheader("📋 Inventário Detalhado")
            st.dataframe(df_inv, use_container_width=True)
            
            # ==========================================
            # --- BOTÃO DE EXPORTAÇÃO (NOVIDADE) ---
            # ==========================================
            st.write("") # Espaço em branco
            col_vazia, col_botao = st.columns([4, 1]) # Empurra o botão para o canto direito
            
            with col_botao:
                pdf_bytes = gerar_pdf(df_inv)
                st.download_button(
                    label="📥 Baixar PDF do Inventário",
                    data=pdf_bytes,
                    file_name="relatorio_frota.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"⚠️ Erro ao processar Dashboard: {e}")
            

    # ==========================================
    # --- TELA 2: CADASTRAR VEÍCULO ---
    # ==========================================
    elif aba == "Cadastrar Veículo":
        st.title("🚛 Cadastrar Novo Veículo")
        with st.form("form_veiculo", clear_on_submit=True):
            placa = st.text_input("Placa do Veículo (Ex: ABC-1234)").upper()
            marca = st.text_input("Marca (Ex: Volvo, Scania)")
            modelo = st.text_input("Modelo (Ex: FH 540)")
            ano = st.number_input("Ano de Fabricação", min_value=1980, max_value=2026, step=1)
            km = st.number_input("Quilometragem Atual", min_value=0, step=100)
            
            if st.form_submit_button("Salvar Veículo"):
                if placa:
                    sql = "INSERT INTO INVENTARIO (placa, marca, modelo, ano, km) VALUES (?, ?, ?, ?, ?)"
                    executar_query(sql, (placa, marca, modelo, ano, km))
                    st.success(f"Veículo {placa} cadastrado com sucesso!")
                else:
                    st.warning("A Placa é obrigatória.")

    # ==========================================
    # --- TELA 3: GERENCIAR FROTA ---
    # ==========================================
    elif aba == "Gerenciar Frota":
        st.title("📂 Gerenciar Frota")
        df_inv = carregar_dados("INVENTARIO")
        
        if df_inv.empty:
            st.info("Nenhum veículo cadastrado.")
        else:
            # Mostra a tabela de veículos com o status atual
            st.dataframe(df_inv, use_container_width=True, hide_index=True)
            
            st.divider()
            col1, col2 = st.columns(2)
            
            # 💡 NOVA FUNÇÃO: Enviar para Manutenção / Liberar
            with col1:
                st.subheader("🔄 Alterar Status do Veículo")
                placa_status = st.selectbox("Selecione a Placa:", df_inv['placa'].tolist(), key="sel_status")
                novo_status = st.radio("Definir como:", ["Ativo", "Manutenção"])
                
                if st.button("Atualizar Status"):
                    # Atualiza diretamente no banco de dados
                    executar_query("UPDATE INVENTARIO SET status = ? WHERE placa = ?", (novo_status, placa_status))
                    st.success(f"Status do veículo {placa_status} alterado para {novo_status}!")
                    st.rerun() # Recarrega a página para atualizar a tabela
                    
            # Função antiga de excluir
            with col2:
                st.subheader("❌ Excluir Veículo")
                placa_deletar = st.selectbox("Selecione a Placa para remover:", df_inv['placa'].tolist(), key="sel_del")
                if st.button("Deletar Permanentemente"):
                    executar_query("DELETE FROM INVENTARIO WHERE placa = ?", (placa_deletar,))
                    st.error(f"Veículo {placa_deletar} excluído do sistema!")
                    st.rerun()

    # ==========================================
    # --- TELA 4: REGISTRAR MANUTENÇÃO ---
    # ==========================================
    elif aba == "Registrar Manutenção":
        st.title("🔧 Nova Ordem de Serviço")
        df_veiculos = carregar_dados("INVENTARIO")
        
        if df_veiculos.empty:
            st.warning("Cadastre um veículo primeiro.")
        else:
            df_veiculos.columns = [str(c).lower() for c in df_veiculos.columns]
            lista_placas = df_veiculos['placa'].tolist()
            
            with st.form("form_manutencao", clear_on_submit=True):
                placa = st.selectbox("Selecione o Veículo", lista_placas)
                data = st.date_input("Data da Manutenção", format="DD/MM/YYYY")
                descricao = st.text_area("Descrição do Serviço")
                tipo = st.selectbox("Tipo de Manutenção", ["Preventiva", "Corretiva"])
                valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
                
                if st.form_submit_button("Salvar Registro"):
                    sql = """
                        INSERT INTO MANUTENCOES (PLACA, DATA, DESCRICAO, TIPO, VALOR) 
                        VALUES (?, ?, ?, ?, ?)
                    """
                    data_formatada = data.strftime('%d/%m/%Y')
                    executar_query(sql, (placa, data_formatada, descricao, tipo, valor))
                    st.success("Manutenção registrada com sucesso!")

    # ==========================================
    # --- TELA 5: GERENCIAR MANUTENÇÕES ---
    # ==========================================
    elif aba == "Gerenciar Manutenções":
        st.title("🗑️ Gerenciar Manutenções")
        df_manut = carregar_dados("MANUTENCOES")

        if df_manut.empty:
            st.info("Nenhuma manutenção registrada até o momento.")
        else:
            df_manut.columns = [c.lower() for c in df_manut.columns]

            if 'data' in df_manut.columns:
                df_manut['data'] = pd.to_datetime(df_manut['data'], dayfirst=True, errors='coerce')

            st.dataframe(
                df_manut[['id', 'placa', 'data', 'tipo', 'valor']],
                column_config={
                    "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                    "valor": st.column_config.NumberColumn("Custo (R$)", format="R$ %.2f")
                },
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            try:
                id_col = df_manut['id'].map(str)
                placa_col = df_manut['placa'].map(str) if 'placa' in df_manut.columns else "S/P"
                
                df_manut['selecao'] = id_col + " - " + placa_col
                lista_para_deletar = df_manut['selecao'].tolist()
                selecionado = st.selectbox("Selecione a manutenção para excluir:", lista_para_deletar)
                
                id_para_deletar = selecionado.split(" - ")[0]

                if st.button("❌ Excluir Registro Permanente"):
                    sql = "DELETE FROM MANUTENCOES WHERE id = ?"
                    executar_query(sql, (id_para_deletar,))
                    st.success(f"Manutenção removida!")
                    st.rerun()
            except Exception as e:
                st.error(f"Erro na seleção: {e}")