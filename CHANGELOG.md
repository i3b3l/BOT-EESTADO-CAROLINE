# Histórico de versões

## Atualização de 16/11/2026 — Painel CMD e estabilidade

### Adicionado
- Painel de execução no CMD com mensagens organizadas por página, patrimônio, etapas e resultado.
- Resumo da execução e registro do horário dos eventos.
- Histórico local e permanente de bens bloqueados em `bens_bloqueados.json` (não versionado).
- Filtro para ignorar bens com bloqueio registrado em execuções anteriores.
- Módulos separados `painel_terminal.py`, `historico_bloqueios.py` e `seletor_conferir.py`.

### Corrigido
- Evita repetir indefinidamente o mesmo bem bloqueado.
- Fecha o formulário de erro pelo botão vermelho **Fechar** e confirma que a janela foi ocultada.
- Localiza **Conferir** na linha do próprio bem, com checagem de ID, mesmo após mudanças na marcação HTML.
- Evita clicar em outro patrimônio quando não há identificação segura.
- Mensagens de erro mais claras, código de saída em falhas e melhorias na paginação.
- Preservada a abertura clássica em ASCII do `Iniciar_Robo_E-Estado.bat`.

### Segurança e testes
- O histórico com IDs patrimoniais e os perfis de navegação não devem ser publicados.
- Código validado sintaticamente; testada a seleção segura do botão em uma página HTML isolada.
- O EXE foi recompilado para Windows.
- O uso real no sistema requer supervisão e conferência dos resultados.
