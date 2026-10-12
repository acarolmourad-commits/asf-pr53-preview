# ASF PR #53 — prévia temporária de revisão

Este repositório separado publica somente a prévia de `guia-apps.html` do commit público `963124e2c94b50305342d4f6f8dd47c4ea37125f` de `acarolmourad-commits/asf-app`.

Não é o site de produção. Não altera o repositório de origem, não faz merge e não configura domínio personalizado.

O build baixa apenas sete arquivos públicos fixados por SHA e verifica SHA-256 antes de adaptar os caminhos para esta prévia. Não copia workflows, credenciais, CRM, documentos internos ou arquivos de configuração da origem.

Adaptações EXCLUSIVAS desta prévia: caminhos dos assets locais, aviso de revisão, robots noindex, base dos assets injetados e desativação da inscrição do service worker na cópia local. O HTML original fica somente no runner e não é publicado como rota adicional. Os 51 cards, seus destinos e a lógica de busca/filtros são preservados. Links para os aplicativos abrem as versões públicas existentes; use Voltar para retornar ao teste. O cache/offline de produção NÃO é validado por esta prévia.

GitHub Pages usa o mesmo host github.io, mas um caminho separado. A prévia não deve receber dados pessoais nem sensíveis. Não há expiração automática; sua remoção/desativação deve ser autorizada após a revisão.

## Teste no Safari do iPhone
1. Confira o aviso PR #53 / 963124e2 e os links Início ASF.
2. Digite previsão; selecione Mar & Condições; limpe a busca e escolha Todas (51 cards).
3. Abra e feche as três FAQs.
4. Confira rolagem, retrato/paisagem e zoom.
5. Informe modelo do iPhone, versão do iOS e envie capturas de problemas.
