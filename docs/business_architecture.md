# 🏢 Business Architecture – live-subtitle-translator

## 📌 Nome do Projeto
**Live Subtitle Translator**

---

## 🌟 Objetivo Principal
Permitir que usuários assistam filmes ou vídeos em uma língua estrangeira com tradução automática dos subtítulos em tempo real, seja capturando diretamente da tela (OCR) ou da aba do navegador (extensão), com exibição sobreposta e discreta.

---

## 👤 Perfis de Usuário (Stakeholders)

| Tipo de Usuário            | Descrição                                                                  |
|-----------------------------|-------------------------------------------------------------------------------|
| Usuário final              | Pessoa que quer assistir vídeos com legendas traduzidas ao vivo             |
| Desenvolvedor/colaborador  | Pessoa que quer contribuir com a evolução do projeto                        |
| Equipe de suporte (futuro) | Pode auxiliar na manutenção da aplicação em produção (quando houver) |

---

## 🧹 Funções Principais (Business Capabilities)

| Função do Sistema                  | Descrição                                                                 |
|--------------------------------------|-------------------------------------------------------------------------------|
| Captura de subtítulo                | Captura texto da legenda da tela (OCR) ou da aba do navegador               |
| Tradução automática               | Usa a API do Gemini para traduzir o texto capturado                         |
| Exibição sobreposta               | Mostra as legendas traduzidas sobre a imagem do vídeo, com opacidade ajustável |
| Gerenciamento de filmes/traduções  | Permite escolher filme, salvar traduções, reutilizar traduções anteriores  |
| Controle da experiência             | Botões Play/Stop, seleção de idioma, transparência da janela, etc.         |

---

## ♻️ Fluxo de Processo (Simplificado)

```
Usuário seleciona filme
      ↓
Usuário clica "Play"
      ↓
Sistema inicia captura (OCR ou navegador)
      ↓
Texto detectado é traduzido automaticamente
      ↓
Legenda traduzida é exibida na tela
      ↓
Ao clicar "Stop", novas traduções são salvas no banco
```

---

## 🧱 Regras de Negócio

- As traduções são mantidas em cache durante a execução para evitar repetidas chamadas à API.
- As traduções só são persistidas no banco ao pressionar "Stop".
- Se o subtítulo já tiver tradução salva (mesmo texto), usa a versão do cache.
- O campo de texto para novo filme só fica habilitado quando “Novo filme” for selecionado.
- A exibição da legenda na tela deve desaparecer após X segundos, salvo se um novo texto for detectado.

---

## 📊 Métricas de Sucesso (Indicadores de Negócio)

| Indicador                      | Meta esperada                              |
|-------------------------------|---------------------------------------------|
| Tempo médio de tradução       | < 2 segundos por subtítulo                 |
| Retenção de legendas          | > 90% dos subtítulos capturados com sucesso |
| Reutilização de traduções     | > 50% dos subtítulos vêm do cache           |
| Feedback positivo dos usuários| Medido via comentários/interações           |

---

## 🚀 Possíveis Evoluções Futuras

- Suporte a múltiplos idiomas de entrada e saída.
- Exportação das traduções para arquivos `.srt`.
- Modo “transcrição” (sem filme) para aulas e vídeos educativos.
- Integração com players específicos (VLC, YouTube, Netflix).
- Interface web ou mobile.

