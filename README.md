# Robô E-ESTADO — Conferência de Bens

Automação em Python para apoiar a **reclassificação e a conferência de bens patrimoniais** no sistema E-ESTADO de Rondônia, com um painel de acompanhamento no terminal Windows.

Desenvolvido por **Izabel Galvão** · [GitHub @i3b3l](https://github.com/i3b3l).

> **Uso autorizado e supervisionado.** Antes de utilizar em produção, valide as ações e resultados no sistema oficial. O robô não substitui a conferência humana.

## Funcionalidades

- Encontra bens com os estados **NÃO CONFERIDO** e **NÃO RECLASSIFICADO**.
- Abre a reclassificação e preenche as opções configuradas: **Servível**, **Localizado**, **Uso e usufruto do bem** e **Bom**.
- Tenta salvar e, quando a interface permite, aciona **Conferir** somente na linha correspondente ao mesmo ID patrimonial.
- Reconhece avisos de bloqueio, fecha o formulário pelo botão **Fechar** e ignora os itens bloqueados.
- Mantém uma lista **local e persistente** de bens bloqueados, evitando novas tentativas após reiniciar o programa.
- Navega pelas páginas de resultados e aceita a solicitação de interrupção pela tecla **Esc**.
- Exibe um painel CMD organizado por página e bem, com etapas, horários, avisos e resumo final.
- Preserva a abertura tradicional em ASCII no arquivo `Iniciar_Robo_E-Estado.bat`.

## Arquivos principais

| Arquivo | Descrição |
| --- | --- |
| `Robo-E-Estado-Conferir.exe` | Executável Windows compilado. |
| `Iniciar_Robo_E-Estado.bat` | Inicialização com banner ASCII e instruções. |
| `Abrir_Chrome_Depuracao.bat` | Inicia o Chrome com depuração local na porta 9222. |
| `inventario.py` | Rotina principal de automação. |
| `seletor_conferir.py` | Localização segura do botão **Conferir** na linha do mesmo bem. |
| `historico_bloqueios.py` | Leitura e gravação dos IDs bloqueados localmente. |
| `painel_terminal.py` | Apresentação e organização das mensagens do CMD. |
| `GERAR_EXE.bat` | Recompilação do executável. |
| `requirements.txt` | Bibliotecas necessárias para executar o código-fonte. |

Para instalar uma cópia nova baixada do GitHub, veja **[Instalação do GitHub](INSTALACAO-DO-GITHUB.md)**. O repositório já inclui o executável Windows e um exemplo vazio de histórico, sem IDs patrimoniais reais.

## Requisitos

- Windows e Google Chrome instalados.
- Acesso autorizado ao E-ESTADO e à listagem de bens.
- O executável já contém o runtime Python; **não inclui o Chrome ou as credenciais de acesso**.
- Para executar o código-fonte ou recompilar o EXE, instale o Python e as dependências de `requirements.txt`.

## Como usar

1. Abra `Iniciar_Robo_E-Estado.bat`.
2. Siga as instruções para iniciar o Chrome preparado para automação.
3. Entre manualmente no E-ESTADO e abra a **listagem correta de bens**.
4. Volte ao CMD e inicie o robô.
5. Acompanhe os registros e valide os resultados. A tecla **Esc** solicita a parada.

A instância de depuração do Chrome precisa responder em `http://localhost:9222`.

## Histórico de bens bloqueados

O arquivo `bens_bloqueados.json` é criado/utilizado **ao lado do EXE**, na pasta local da instalação. Ele registra somente **ID**, **data** e **motivo**. A cada execução, os IDs registrados são consultados antes de reclassificar.

- **O histórico real não é publicado no GitHub**: `bens_bloqueados.json` está no `.gitignore`.
- Se mover o programa para outro computador/pasta, transporte o histórico **se autorizado**.
- Se um bem for desbloqueado, revise o registro local com o robô fechado e faça backup antes de remover o ID.
- Uma anotação de bloqueio é histórica: não garante que o status do bem continue bloqueado.
- Se o histórico estiver inválido, o programa interrompe a inicialização em vez de descartá-lo silenciosamente.

## Gerar novamente o executável

Instale as dependências e execute `GERAR_EXE.bat` na pasta do projeto. O script usa o PyInstaller para gerar `Robo-E-Estado-Conferir.exe`, incluindo os módulos Python auxiliares importados por `inventario.py`.

## Avisos de segurança

- **Não publique** `bens_bloqueados.json`, sessões do navegador, arquivos de autenticação, relatórios patrimoniais ou dados internos.
- O robô utiliza seletores da interface atual do E-ESTADO; mudanças na página podem exigir revisão.
- Em caso de botão ambíguo ou linha sem identificação segura, **não confirma outro patrimônio por aproximação**.
- A saída **Conferências acionadas** indica ações solicitadas; não comprova, sozinha, o registro definitivo no servidor.
- O Chrome com depuração deve permanecer sob controle do operador.
- O EXE pode ultrapassar a recomendação de 50 MB do GitHub, embora esteja abaixo do limite comum de 100 MB por arquivo.

## Licença

Veja [LICENSE](LICENSE).
