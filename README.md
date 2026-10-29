# Robô E-ESTADO — Conferência de Bens

Automação em Python para auxiliar na reclassificação e conferência de bens no sistema E-ESTADO de Rondônia. O projeto foi desenvolvido por Izabel Galvão.

> Use somente com autorização e acompanhe a execução para confirmar as ações realizadas no sistema.

## O que o robô faz

- Localiza itens marcados como **NÃO CONFERIDO** e **NÃO RECLASSIFICADO**.
- Abre a reclassificação e preenche as opções configuradas no código.
- Salva a reclassificação e tenta conferir o item quando o sistema permite.
- Identifica avisos de bem bloqueado e pula esses itens para evitar tentativas repetidas.
- Percorre as páginas disponíveis na listagem.
- Permite solicitar a interrupção pressionando **Esc**.

## Arquivos do projeto

| Arquivo | Finalidade |
|---|---|
| `Robo-E-Estado-Conferir.exe` | Executável pronto para uso no Windows. |
| `Iniciar_Robo_E-Estado.bat` | Apresenta as instruções e inicia o robô. |
| `Abrir_Chrome_Depuracao.bat` | Abre o Chrome com depuração remota na porta `9222`. |
| `inventario.py` | Código-fonte Python da automação. |
| `GERAR_EXE.bat` | Script para gerar novamente o executável. |
| `requirements.txt` | Dependências Python do projeto. |
| `LEIA-ME.txt` | Instruções resumidas de utilização. |
| `.gitignore` | Arquivos locais que não devem ser versionados. |
| `LICENSE` | Arquivo de licença incluído no repositório. |

## Requisitos

- Windows.
- Google Chrome instalado.
- Acesso autorizado ao sistema E-ESTADO.
- Para a execução do `.exe`, não é necessário instalar Python; o Chrome não está incluído no executável.

Para executar o código-fonte ou gerar o executável, instale uma versão compatível do Python e as dependências listadas em `requirements.txt`.

## Como executar

1. Na pasta do projeto, execute `Iniciar_Robo_E-Estado.bat`.
2. O script abrirá o Chrome com a depuração remota habilitada e acessará o E-ESTADO.
3. Faça login manualmente no sistema e navegue até a lista correta de bens.
4. Retorne ao terminal e siga a instrução apresentada para iniciar a automação.
5. Acompanhe a execução, especialmente na primeira utilização.
6. Para solicitar a interrupção, pressione **Esc**.

Se necessário, execute `Abrir_Chrome_Depuracao.bat` separadamente para abrir o navegador de depuração. O Chrome usado pelo robô deve estar disponível em `http://localhost:9222`.

## Gerar o executável

Com Python instalado, abra o terminal na pasta do projeto, instale as dependências e execute o arquivo `GERAR_EXE.bat`. Confira o conteúdo desse script antes de executá-lo e confirme que o executável gerado corresponde à versão atual de `inventario.py`.

## Segurança e observações

- Não compartilhe senhas, cookies, perfis do navegador ou dados de autenticação.
- O robô conecta-se a uma sessão do Chrome já aberta com depuração remota; mantenha essa sessão sob seu controle.
- A automação depende da estrutura visual e dos seletores do sistema. Mudanças no E-ESTADO podem exigir ajustes no código.
- A tecla **Esc** solicita a interrupção, mas não substitui o acompanhamento da execução.
- Confira os resultados no sistema após a execução e valide o comportamento antes de usar em produção.
- O executável tem aproximadamente 60,88 MB, acima do tamanho de arquivo recomendado pelo GitHub; o aviso de tamanho não impede o envio atual.

## Dependências

As versões e os pacotes utilizados estão definidos em [`requirements.txt`](requirements.txt), incluindo Playwright, PyAutoGUI, keyboard e PyInstaller.

## Autoria

Desenvolvido por **Izabel Galvão**.
GitHub: https://github.com/i3b3l
