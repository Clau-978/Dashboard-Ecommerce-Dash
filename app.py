import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc


# Criação dos gráficos
def cria_graficos(df):
    # Histograma
    fig1 = px.histogram(df, x='Preço', nbins=30, title='Distribuição dos Preços')
    fig1.update_layout(template='plotly_white', xaxis_title='Preço', yaxis_title='Quantidade de Produtos')


# Conta a quantidade de produtos por marca
    top5 = (
        df.groupby('Marca')['Preço']
          .mean()
          .sort_values(ascending=False)
          .head(5)
          .reset_index()
    )

    fig2 = px.pie(top5, names='Marca', values='Preço', hole=0.45, title='Top 5 Marcas por Preço Médio')

    # Gráfico de bolhas
    fig3 = px.scatter(df, x='Nota', y='N_Avaliações', size='Qtd_Vendidos_Cod', color='Desconto', hover_data=['Marca','Gênero'], size_max=30, color_continuous_scale='Viridis')
    fig3.update_traces(opacity=0.65, marker=dict(line=dict(color='white', width=1)))
    fig3.update_layout(template='plotly_white', title='Relação entre Nota e Número de Avaliações', xaxis_title='Nota', yaxis_title='N_Avaliações')

    # Gráfico de Linha
    df_media = (
        df.groupby(['Temporada', 'Nota'])['N_Avaliações']
          .mean()
          .reset_index()
    )

    fig4 = px.line(df_media, x='Nota', y='N_Avaliações', color='Temporada', markers=True)
    fig4.update_layout(
        template='plotly_white',
        title='Média de Avaliações por Nota e temporada',
        xaxis_title='Nota',
        yaxis_title='Média de Avaliações',
    )

    # Gráfico #3D
    fig5 = px.scatter_3d(df, x='Nota', y='Preço', z='N_Avaliações', color='Temporada')
    fig5.update_layout(title='Nota, Preço e Número de Avaliações')

    # Gráfico de Barra
    df_bar = (
        df.groupby(['Gênero', 'Temporada'])['N_Avaliações']
          .mean()
          .reset_index()
    )

    fig6 = px.bar(df_bar, x="Gênero", y="N_Avaliações", color="Temporada", barmode="group", color_discrete_sequence=px.colors.qualitative.Bold)
    fig6.update_layout(
        template="plotly_white",
        title="Média de Avaliações por Gênero e Temporada",
        xaxis_title="Gênero",
        yaxis_title="Média de Avaliações",
        legend_title="Temporada"
        )
    return fig1, fig2, fig3, fig4, fig5, fig6

def cria_app(df):
    # Cria APP
    app = Dash(__name__)

    fig1,fig2,fig3,fig4,fig5,fig6 = cria_graficos(df)

    app.layout = html.Div([

        html.H1(
            "Dashboard de Análise do E-Commerce",
            style={
                'text-align': 'center',
                'marginBottom': '30px'
           }
        ),

        html.Div([
            dcc.Graph(figure=fig1, style={'width':'50%'}),
            dcc.Graph(figure=fig2, style={'width':'50%'})
        ], style={'display': 'flex'}),

        html.Div([
            dcc.Graph(figure=fig3, style={'width':'50%'}),
            dcc.Graph(figure=fig4, style={'width':'50%'})
        ], style={'display': 'flex'}),

        html.Div([
            dcc.Graph(figure=fig5),
            dcc.Graph(figure=fig6)
        ], style={'display': 'flex'})
    ])
    return app

# Leitura dos dados
df = pd.read_csv(r"C:\Users\claud\PycharmProjects\dashboard-ecommerce-dash\ecommerce_estatistica.csv")

# Executa APP
if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug=True)
