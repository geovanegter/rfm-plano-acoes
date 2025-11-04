
ActionBI - RFM MVP (Streamlit)
==============================

Arquivos gerados:
- vendas_template.xlsx -> modelo de dados de vendas (colunas: cliente, data, valor, colecao, vendedor, regional)
- planos_acoes.xlsx -> arquivo Excel onde os planos de ação serão salvos
- rfm_app.py -> app Streamlit (MVP)
- pasta data_files/ -> local esperado pelo app para armazenar os arquivos (vendas_template.xlsx e planos_acoes.xlsx podem ser movidos pra lá)

Como rodar localmente:
1) Instale dependências:
   pip install streamlit pandas openpyxl

2) Copie os arquivos para uma pasta do seu projeto, por exemplo:
   /seu-projeto/
     rfm_app.py
     vendas_template.xlsx
     planos_acoes.xlsx

   ou mantenha a estrutura criada em /mnt/data/rfm_mvp/ e rode de lá.

3) Execute:
   streamlit run rfm_app.py

Uso:
- O app permite fazer upload do Excel de vendas. Se não enviar, ele tenta usar o template vendas_template.xlsx.
- Depois de calcular RFM, selecione um cliente e crie planos de ação. Eles serão salvos em planos_acoes.xlsx.

Observações:
- Esta é a versão MVP: para produção, recomenda-se migrar o salvamento de planos para um banco de dados e configurar autenticação.
- Ajuste regras de segmentação conforme necessário.

Arquivos gerados neste ambiente: /mnt/data/rfm_mvp
