import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import datetime
import io
import dash_mantine_components as dmc
import plotly.express as px

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions=True

tab_style = {
    "background": "grey",
    'border-style': 'solid',
    'border-color': 'grey',
    "width": "100%",
    "height":"100px",
}

tab_selected_style = {
    "width": "100%",
    "height":"100px",
    "text-align": "center"
}

app.layout = dmc.MantineProvider(
 id="app-theme",
    theme={
  "colorScheme": "dark",
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[html.Div(children=[
    html.Div(children=[  
    dcc.Upload(id="upload-data",children=[
        html.Div(children=[html.P("Subir arquivo",id="upload-text")],id="upload-div"),
        html.Div(id="files-div", style={"display":"none"})
    ]),
    dcc.Tabs(id="selection-tabs",value="visao-geral",children=[
        dcc.Tab(label="Visão Geral",value="visao-geral",className="tabs",style=tab_style,selected_style=tab_selected_style),
        dcc.Tab(label="Análise de Produto",value="analise-produto",className="tabs",style=tab_style,selected_style=tab_selected_style),
        dcc.Tab(label="Análise de Filial",value="analise-filial",className="tabs",style=tab_style,selected_style=tab_selected_style)
    ])],id="tab-div"),
    html.Div(id="tabs-content")
],id="main-div")]
)

#Empty dataframe, prevents malfunction
df = pd.DataFrame(columns=["Nome","Categoria","Preço","Unidades Vendidas","Total","Filial","Forma de Pagamento","Método de Entrega","Data","Ano"])


#File upload
def read_file(contents, filename, date):
    global df
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df["Data"] = pd.to_datetime(df["Data"])
            df["Ano"] = df["Data"].apply(lambda x: x.year)
    except:
        print("There was an error processing the file")
    return html.P(filename)

@callback(Output("selection-tabs", "value"),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        read_file(list_of_contents,list_of_names,list_of_dates)
    return "visao-geral"

#analysis
def general_tab_analysis():
    produtos_mais_vendidos = {"Produtos":list(df.groupby("Nome",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False)[0:3].index.values),
                              "Unidades vendidas":list(((df.groupby("Nome",axis=0)["Unidades Vendidas"].sum()).sort_values(ascending=False))[0:3].values)}
    
    produtos_mais_lucrativos = {"Produtos":list(df.groupby("Nome",axis=0)["Total"].sum().sort_values(ascending=False)[0:3].index.values),
                                "Total":list(((df.groupby("Nome",axis=0)["Total"].sum()).sort_values(ascending=False))[0:3].values)}

    filial_mais_vendidos = {"Filiais":list(df.groupby("Filial",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False)[0:3].index.values),
                            "Unidades vendidas":list(((df.groupby("Filial",axis=0)["Unidades Vendidas"].sum()).sort_values(ascending=False))[0:3].values)}
    
    filial_mais_lucrativos = {"Filiais":list(df.groupby("Filial",axis=0)["Total"].sum().sort_values(ascending=False)[0:3].index.values),
                              "Total":list(((df.groupby("Filial",axis=0)["Total"].sum()).sort_values(ascending=False))[0:3].values)}

    return produtos_mais_vendidos,produtos_mais_lucrativos, filial_mais_vendidos, filial_mais_lucrativos


@callback(Output(component_id="unidades-grafico",component_property="figure",),Input("unidades-dropdown","value"))
def update_unities_graph(value):
    if value == "Produto":
        fig_dict = {"Produtos":list(df.groupby("Nome",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).index),
                    "Unidades vendidas":list(df.groupby("Nome",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).values)}
        fig = px.bar(fig_dict,x="Produtos",y="Unidades vendidas",template="plotly_dark",color="Produtos")
    elif value == "Categoria":
        fig_dict = {"Categorias":list(df.groupby("Categoria",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).index),
                    "Unidades vendidas":list(df.groupby("Categoria",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).values)}
        fig = px.bar(fig_dict,x="Categorias",y="Unidades vendidas",template="plotly_dark",color="Categorias")
    elif value == "Forma de pagamento":
        fig_dict = {"Forma de pagamento":list(df.groupby("Forma de Pagamento",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).index),
                    "Unidades vendidas":list(df.groupby("Forma de Pagamento",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).values)}
        fig = px.bar(fig_dict,x="Forma de pagamento",y="Unidades vendidas",template="plotly_dark",color="Forma de pagamento")
    elif value == "Método de entrega":
        fig_dict = {"Método de entrega":list(df.groupby("Método de Entrega",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).index),
                    "Unidades vendidas":list(df.groupby("Método de Entrega",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).values)}
        fig = px.bar(fig_dict,x="Método de entrega",y="Unidades vendidas",template="plotly_dark",color="Método de entrega")
    return fig

@callback(Output("filial-bar","figure"),Input("filial-dropdown","value"))
def update_filial_graph(value):
    if value == "Unidades vendidas":
        fig_dict = {"Filiais":list(df.groupby("Filial",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).index),
                    "Unidades vendidas": list(df.groupby("Filial",axis=0)["Unidades Vendidas"].sum().sort_values(ascending=False).values)}
        fig = px.bar(fig_dict,x="Filiais",y="Unidades vendidas",color="Filiais",template="plotly_dark")
    elif value == "Lucro total":
        fig_dict = {"Filiais":list(df.groupby("Filial",axis=0)["Total"].sum().sort_values(ascending=False).index),
                    "Total": list(df.groupby("Filial",axis=0)["Total"].sum().sort_values(ascending=False).values)}
        fig = px.bar(fig_dict,x="Filiais",y="Total",color="Filiais",template="plotly_dark")
    return fig


#tabs
@callback(Output("tabs-content","children"),Input("selection-tabs","value"))
def update_tab(tab):
    if tab == "visao-geral":
        produtos_mais_vendidos, produtos_mais_lucrativos, filial_mais_vendidos, filial_mais_lucrativos= general_tab_analysis()
        return html.Div(children=[
            html.Div(children=[
            dcc.Graph(figure=px.bar(produtos_mais_vendidos,x="Produtos",y="Unidades vendidas",template="plotly_dark",color="Produtos",title="Produtos mais vendidos"),id="product-unities"),
            dcc.Graph(figure=px.bar(produtos_mais_lucrativos,x="Produtos",y="Total",template="plotly_dark",color="Produtos",title="Produtos mais lucrativos"),id="product-profit")]),
            html.Div(children=[
            dcc.Graph(figure=px.bar(filial_mais_vendidos,x="Filiais",y="Unidades vendidas",template="plotly_dark",color="Filiais",title="Filiais com mais vendas"),id="filial-unities"),
            dcc.Graph(figure=px.bar(filial_mais_lucrativos,x="Filiais",y="Total",template="plotly_dark",color="Filiais",title="Filiais mais lucrativas"),id="filial-profit")])
        ],id="main-main-div")
    elif tab == "analise-produto":
        total = df["Total"].sum()
        
        best10 = {"Produtos":list(df.groupby("Nome")["Total"].sum().apply(lambda x: (x/total)*100).sort_values(ascending=False)[0:10].index),
                  "Valor (%)":list(df.groupby("Nome")["Total"].sum().apply(lambda x: (x/total)*100).sort_values(ascending=False)[0:10].values)}
        return html.Div(children=[
            html.P("Unidades vendidas por:",className="text"),
            dcc.Dropdown(options=["Produto","Categoria","Forma de pagamento","Método de entrega"],value="Produto",id="unidades-dropdown"),
            dcc.Graph(id="unidades-grafico"),
            dcc.Graph(figure=px.bar(best10,x="Produtos",y="Valor (%)",template="plotly_dark",color="Produtos",title="Contribuição dos 10 melhores produtos"),id="10-products"),
            dcc.Graph(figure=px.line(df.groupby(df["Data"].apply(lambda x: x.year))["Total"].sum(),template="plotly_dark",title="Lucro ao longo do tempo"),id="product-time")
        ])
    elif tab == "analise-filial":
        df_lucro_filiais = pd.DataFrame(columns=["Ano","Total","Filial"])
        filiais = list(df["Filial"].unique())
        for filial in filiais:
            anos_filial = list(df[df["Filial"] == filial].groupby("Ano")["Total"].sum().index)
            totais_filial = list(df[df["Filial"] == filial].groupby("Ano")["Total"].sum().values)
            for i,ano in enumerate(anos_filial):
                df_prov = pd.DataFrame()
                df_prov["Ano"] = [anos_filial[i]]
                df_prov["Total"] = [totais_filial[i]]
                df_prov["Filial"] = [filial]
                df_lucro_filiais = pd.concat([df_lucro_filiais,df_prov])
        return html.Div(children=[
            html.P("Análise de filial por:",className="text"),
            dcc.Dropdown(options=["Unidades vendidas","Lucro total"],value="Unidades vendidas",id="filial-dropdown"),
            dcc.Graph(id="filial-bar"),
            dcc.Graph(figure=px.pie(df,values="Total",names="Filial",template="plotly_dark",title="Contribuição de cada filial para a renda"),id="filial-pizza"),
            dcc.Graph(figure=px.line(df_lucro_filiais,x="Ano",y="Total",color="Filial",template="plotly_dark",title="Lucro das filiais ao longo dos anos"),id="filial-lucro")
        ])

if __name__ == "__main__":
    app.run_server(debug=True)