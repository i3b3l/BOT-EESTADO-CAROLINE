# Instalar o BOT E-ESTADO a partir do GitHub

Este repositório inclui **o executável Windows já compilado**, o código-fonte, o painel CMD, os scripts de inicialização e os módulos auxiliares.

## Instalação em outro PC

1. No GitHub, escolha **Code → Download ZIP** e extraia a pasta inteira; ou faça `git clone https://github.com/i3b3l/BOT-EESTADO-CAROLINE.git`.
2. Confirme que os arquivos `Robo-E-Estado-Conferir.exe`, `Iniciar_Robo_E-Estado.bat` e `Abrir_Chrome_Depuracao.bat` estão na **mesma pasta**.
3. Tenha **Windows**, **Google Chrome instalado** e **acesso autorizado ao E-ESTADO**.
4. Execute `Iniciar_Robo_E-Estado.bat`. O inicializador abre o Chrome preparado para depuração.
5. Entre **manualmente** no E-ESTADO, abra a listagem certa e continue pelo CMD.

Para usar apenas o executável, **não é preciso instalar Python**. Python e as dependências do `requirements.txt` são necessários apenas para executar o código-fonte ou recompilar o EXE.

## O histórico dos bens bloqueados

O arquivo real `bens_bloqueados.json` **não está no GitHub**, porque pode conter IDs patrimoniais internos. Isso **não impede uma instalação nova de funcionar**: se não existir, o robô começa com o histórico vazio e o cria automaticamente quando identificar o primeiro bloqueio.

Se desejar criar o arquivo vazio manualmente, copie `bens_bloqueados.exemplo.json` como `bens_bloqueados.json`. **Não renomeie o exemplo original.**

Se for migrar a lista de bloqueios de outro computador, copie o `bens_bloqueados.json` antigo para a mesma pasta do EXE **por um meio privado e autorizado**, antes de iniciar o robô. Nunca publique IDs patrimoniais ou dados de login no repositório.

## O que não acompanha o download (intencionalmente)

- Credenciais, cookies, sessões ou perfis de Chrome;
- Histórico patrimonial real, relatórios e backups locais;
- Google Chrome e conexão com o E-ESTADO.

## Verificações

- O repositório foi clonado numa pasta vazia em Windows e continha todos os arquivos necessários para inicialização.
- O EXE clonado teve o mesmo SHA-256 do executável publicado pela pasta de desenvolvimento.
- Os módulos Python foram verificados por compilação; a conferência real no sistema necessita de acesso e acompanhamento do operador.

> Se o Windows mostrar um aviso sobre um executável recém-baixado, confira primeiro a origem e a integridade do arquivo. Não desative proteções do computador.
