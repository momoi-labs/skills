# Como publicar um repositório de Agent Skills e distribuí-lo no ChatGPT

> Pesquisa realizada em 24 de julho de 2026, com base em documentação e código-fonte oficiais.

## Resposta curta

Você pode criar um repositório GitHub público com uma ou mais pastas `skills/<nome>/SKILL.md`. Sem publicar um pacote npm, ele já poderá ser instalado assim:

```bash
npx skills@latest add sua-org/seu-repo
```

Esse comando pertence ao CLI open source [`vercel-labs/skills`](https://github.com/vercel-labs/skills), e não ao ChatGPT. Ele clona/lê o repositório, descobre as skills e as instala nos diretórios esperados pelos agentes locais. O próprio CLI documenta o atalho GitHub `owner/repo`, URLs Git completas, caminhos locais, instalação por skill e seleção do agente de destino ([README do CLI](https://github.com/vercel-labs/skills#install-a-skill)).

Para disponibilizar as mesmas skills no ChatGPT para um time, o repositório sozinho não basta. Hoje há duas rotas oficiais:

1. **Skills do workspace:** fazer upload/criar a skill no ChatGPT e compartilhá-la com pessoas, grupos ou com todo o workspace.
2. **Plugin:** empacotar uma ou mais skills como plugin e compartilhá-lo com o workspace; é a rota recomendada pela OpenAI para distribuição reutilizável, catálogos e bundles que também possam incluir apps/MCP.

A documentação da OpenAI é explícita: skills são o formato de autoria; plugins são o formato preferido quando o objetivo é distribuir para outras pessoas no workspace ([OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)).

## 1. Estrutura mínima do repositório

Estrutura recomendada para começar:

```text
seu-repo/
├── README.md
├── LICENSE
└── skills/
    ├── revisar-pr/
    │   ├── SKILL.md
    │   ├── references/       # opcional
    │   ├── scripts/          # opcional
    │   └── assets/           # opcional
    └── escrever-adr/
        └── SKILL.md
```

O CLI procura skills na raiz e em diretórios conhecidos, incluindo `skills/`, `.agents/skills/` e vários diretórios específicos de agentes. No layout comum, ele percorre `skills/<nome>/SKILL.md`; também aceita um nível de categoria, como `skills/<categoria>/<nome>/SKILL.md` ([regras de descoberta do CLI](https://github.com/vercel-labs/skills#skill-discovery)).

O formato Agent Skills é uma pasta cujo único arquivo obrigatório é `SKILL.md`. Scripts, referências, templates e outros recursos podem acompanhar a skill ([visão geral do padrão Agent Skills](https://agentskills.io/home)).

Exemplo mínimo:

```markdown
---
name: revisar-pr
description: Revisa pull requests segundo os padrões internos. Use quando o usuário pedir revisão de PR, branch ou diff.
---

# Revisar PR

1. Leia os padrões do repositório.
2. Inspecione o diff completo.
3. Classifique achados por severidade.
4. Cite arquivo e linha para cada problema.
```

Pelo padrão aberto:

- `name` é obrigatório, tem no máximo 64 caracteres, usa apenas letras minúsculas ASCII, números e hífens, não começa/termina com hífen, não contém `--` e deve ser igual ao nome da pasta;
- `description` é obrigatória, tem no máximo 1024 caracteres e deve explicar tanto o que a skill faz quanto quando deve ser usada;
- `license`, `compatibility`, `metadata` e `allowed-tools` são opcionais; `allowed-tools` ainda é experimental e seu suporte varia entre clientes;
- o corpo é Markdown livre; instruções longas devem mover detalhes para `references/`.

Essas regras vêm da [especificação Agent Skills](https://agentskills.io/specification). A especificação também recomenda manter o `SKILL.md` abaixo de 500 linhas e usar referências relativas a partir da raiz da skill.

## 2. Criar, validar e publicar

O CLI oferece um gerador simples:

```bash
mkdir meu-repo
cd meu-repo
mkdir -p skills
cd skills
npx skills@latest init revisar-pr
```

Também é possível criar a pasta e o `SKILL.md` manualmente. Para validação estrita do padrão, a especificação aponta o validador de referência:

```bash
skills-ref validate ./skills/revisar-pr
```

Depois, publique o repositório normalmente no GitHub. Para que o atalho abaixo funcione sem configuração de autenticação, use um repositório público:

```bash
npx skills@latest add sua-org/seu-repo --list
npx skills@latest add sua-org/seu-repo
```

Testes úteis antes de anunciar:

```bash
# listar o que o CLI encontrou
npx skills@latest add sua-org/seu-repo --list

# instalar uma skill específica no Codex
npx skills@latest add sua-org/seu-repo \
  --skill revisar-pr \
  --agent codex

# instalar globalmente, sem prompts (útil em setup automatizado)
npx skills@latest add sua-org/seu-repo \
  --skill revisar-pr \
  --agent codex \
  --global \
  --yes
```

As opções `--list`, `--skill`, `--agent`, `--global`, `--copy`, `--yes` e `--all` são documentadas no [README do `vercel-labs/skills`](https://github.com/vercel-labs/skills#options). O mesmo documento identifica o Codex com `--agent codex`.

Não é necessário “publicar no skills.sh” para o comando `add owner/repo` funcionar: o source of truth é o repositório Git. O diretório/leaderboard do skills.sh é alimentado por telemetria anônima de instalações do CLI; portanto, aparecer e ganhar ranking ali é uma consequência de instalações, não um pré-requisito de distribuição ([documentação do skills.sh](https://www.skills.sh/docs)).

### Repositório privado

O CLI aceita qualquer URL Git, inclusive SSH, por exemplo:

```bash
npx skills@latest add git@github.com:sua-org/skills-internas.git
```

Esse formato consta entre as fontes suportadas no [README oficial](https://github.com/vercel-labs/skills#source-formats). Na prática, o processo precisa ter credenciais Git válidas. Para uso empresarial, teste autenticação, CI e política de telemetria antes de padronizar essa rota; o próprio projeto ainda mantém discussões sobre a experiência e a documentação de repositórios privados ([issue oficial #381](https://github.com/vercel-labs/skills/issues/381)).

## 3. Instalação local no Codex

O CLI da Vercel e o Codex são projetos distintos:

- `npx skills add` resolve um repositório e copia/cria links nos diretórios dos agentes escolhidos;
- o Codex descobre e executa skills instaladas nos seus próprios escopos.

Segundo a documentação atual da OpenAI, o Codex lê skills do repositório, do usuário, do administrador e do sistema. Em repositórios, ele procura `.agents/skills` desde o diretório atual até a raiz Git; a OpenAI também documenta `$HOME/.agents/skills` para o usuário e `/etc/codex/skills` para administração da máquina/container ([OpenAI — onde salvar skills](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills)). O CLI `skills`, por sua vez, declara `.agents/skills/` como caminho de projeto e `~/.codex/skills/` como caminho global para seu target `codex` ([tabela de agentes do CLI](https://github.com/vercel-labs/skills#supported-agents)). Por isso, use explicitamente `--agent codex` e confirme com a listagem de skills do Codex após instalar.

Para uma equipe de engenharia, há duas estratégias locais:

- **Repo-scoped:** instalar/commitar as skills em `.agents/skills/` dentro de cada projeto. Todos que clonarem o projeto recebem os mesmos workflows.
- **User-scoped:** cada pessoa instala globalmente com `--global`. É conveniente, mas exige um processo de atualização por máquina.

O CLI fornece `npx skills update` para atualizar instalações gerenciadas por ele ([comandos do CLI](https://github.com/vercel-labs/skills#other-commands)).

## 4. Adicionar ao ChatGPT como skill pessoal

No ChatGPT:

1. Abra **Plugins** na barra lateral.
2. Entre na aba **Skills**.
3. Selecione **Create**.
4. Use **Upload from your computer**, o editor ou “Create with chat”.
5. Revise a skill e instale-a.

Esses caminhos são documentados em [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt/). O ChatGPT verifica skills enviadas; elas podem ficar disponíveis imediatamente, exigir revisão ou ser bloqueadas. Como uma skill pode incluir código e arquivos auxiliares, a OpenAI recomenda revisar a origem e o conteúdo antes do upload.

Pontos importantes:

- Skills pessoais estão geralmente disponíveis em ChatGPT Business, Enterprise, Healthcare e Edu.
- Skills pessoais precisam ser adicionadas separadamente no desktop e no web/mobile; elas não sincronizam automaticamente entre essas superfícies.
- O formato segue o padrão aberto Agent Skills, mas recursos específicos de um cliente podem não funcionar em outro. Por exemplo, o CLI `skills` mantém uma [matriz de compatibilidade](https://github.com/vercel-labs/skills#compatibility) e mostra que alguns campos/hooks são específicos de determinados agentes.

Em outras palavras: o mesmo `SKILL.md` básico é portátil, mas scripts, ferramentas, hooks e caminhos locais devem ser testados em cada superfície.

## 5. Disponibilizar para o time no ChatGPT

### Opção A — compartilhar/publicar uma Skill no workspace

Depois de criar ou enviar a skill:

1. Abra **Plugins → Skills**.
2. Abra o menu `•••` da skill.
3. Selecione **Share**.
4. Compartilhe com pessoas/grupos ou publique para o workspace, conforme as permissões disponíveis.

Os membros encontram skills em **Shared with me** ou **Shared by {workspace}** e podem instalá-las. Administradores podem fazer upload diretamente na página administrativa de Skills, alterar acesso e proprietário, baixar ou excluir uma skill ([OpenAI — Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt/)).

Para Enterprise e Edu, Skills estão desativadas por padrão no momento descrito pela documentação; admins podem habilitá-las por papel. As permissões são separadas:

- criar e usar skills;
- fazer upload;
- compartilhar;
- publicar para todo o workspace;
- instalar para outros membros.

Esses controles valem para as Skills gerenciadas no ChatGPT. A OpenAI ressalta que Skills em outros produtos, inclusive Codex, podem ter governança separada.

### Opção B — empacotar como plugin

Use plugin quando quiser:

- distribuir uma ou várias skills como pacote versionado;
- oferecer um catálogo instalável;
- incluir futuramente um app, conector MCP, hooks ou identidade visual;
- compartilhar o pacote entre ChatGPT Work e Codex.

A estrutura mínima oficial é:

```text
meu-plugin/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    └── revisar-pr/
        └── SKILL.md
```

`.codex-plugin/plugin.json`:

```json
{
  "name": "skills-do-time",
  "version": "1.0.0",
  "description": "Workflows reutilizáveis do time",
  "skills": "./skills/"
}
```

Essa estrutura e os campos mínimos são mostrados em [OpenAI — Build plugins](https://learn.chatgpt.com/docs/build-plugins#create-a-plugin-manually). Um repositório cuja raiz contenha `.codex-plugin/plugin.json` e `skills/` pode, em princípio, servir simultaneamente como:

- fonte do `npx skills add owner/repo`, porque o CLI descobre `skills/<nome>/SKILL.md`;
- raiz de um plugin OpenAI, porque o manifesto aponta para `./skills/`.

Ainda assim, trate as duas instalações como pipelines independentes e teste ambas.

Para acelerar o empacotamento, a OpenAI fornece `@plugin-creator` no ChatGPT e `$plugin-creator` no Codex. Ele gera o manifesto obrigatório e pode criar uma entrada de marketplace local ([OpenAI — criação de plugins](https://learn.chatgpt.com/docs/build-plugins#create-a-plugin-with-plugin-creator)).

Depois de adicionar o plugin no app desktop:

1. mude para o workspace Work;
2. abra **Plugins → Created by you**;
3. abra o plugin e selecione **Share**;
4. escolha membros, grupos ou copie o link.

Os destinatários o encontram em **Shared with you**. Isso não publica o plugin no diretório público; ele permanece dentro da organização ([OpenAI — compartilhar plugin local](https://learn.chatgpt.com/docs/build-plugins#share-a-local-plugin-with-your-workspace)).

## 6. Marketplace Git para Codex/desktop

Se quiser que o próprio repositório seja um catálogo de plugins, a OpenAI documenta marketplaces JSON:

- repo: `$REPO_ROOT/.agents/plugins/marketplace.json`;
- pessoal: `~/.agents/plugins/marketplace.json`.

Também é possível registrar um marketplace Git:

```bash
codex plugin marketplace add sua-org/seu-repo
codex plugin marketplace list
codex plugin marketplace upgrade
```

Fontes aceitas incluem atalho GitHub, URL Git HTTPS/SSH e diretório local. Isso é uma distribuição diferente do `npx skills`: o comando `codex plugin marketplace add` instala/rastreia um **catálogo de plugins**, enquanto `npx skills add` instala **pastas de skills** em agentes locais ([OpenAI — adicionar marketplace pela CLI](https://learn.chatgpt.com/docs/build-plugins#add-a-marketplace-from-the-cli)).

Para times que usam o ChatGPT desktop, um marketplace de repositório é útil durante desenvolvimento e curadoria. Para acesso organizacional administrado no ChatGPT, prefira compartilhar/publicar dentro do workspace, porque isso aplica identidade, grupos e permissões da organização.

## 7. Arquitetura recomendada para o seu caso

### Fase 1 — repositório instalável

1. Crie `github.com/sua-org/skills`.
2. Mantenha as skills em `skills/<nome>/SKILL.md`.
3. Use `name` igual ao diretório e uma `description` precisa.
4. Inclua licença, README, exemplos e política de segurança.
5. Teste `npx skills@latest add sua-org/skills --list`.
6. Teste instalação explícita em cada agente suportado.
7. Versione mudanças com tags/releases e changelog, mesmo que o CLI instale diretamente do Git.

### Fase 2 — piloto no ChatGPT

1. Faça upload de uma skill no workspace.
2. Compartilhe somente com um grupo piloto.
3. Teste prompts que devem e não devem ativá-la.
4. Confirme se scripts/dependências funcionam na superfície escolhida.
5. Publique para o workspace somente depois da revisão de segurança e conteúdo.

### Fase 3 — distribuição organizada

Se houver várias skills ou conectores, adicione `.codex-plugin/plugin.json`, transforme o repositório em plugin/catálogo e use os controles de compartilhamento do workspace. Se o objetivo for entregar uma experiência única e repetível aos usuários, também é possível anexar skills a um Workspace Agent e publicar esse agente no diretório da organização; o builder aceita skills criadas, enviadas ou já disponíveis ([OpenAI — Workspace Agents](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business)).

## 8. Checklist de segurança e manutenção

- Revise todo `SKILL.md`, script e asset antes de instalar ou compartilhar.
- Não coloque segredos, tokens ou dados internos no repositório público.
- Declare dependências e requisitos de rede em `compatibility` e na documentação.
- Prefira instruções a scripts quando não precisar de comportamento determinístico.
- Fixe versões de dependências usadas por scripts.
- Teste ativações positivas e negativas; a `description` controla a descoberta implícita.
- Defina ownership e revisão por pull request.
- Use tags/releases e changelog para auditoria.
- Para ChatGPT gerenciado, configure papéis de upload, compartilhamento, publicação e instalação com privilégio mínimo.
- Trate instalação local do Codex e distribuição do workspace ChatGPT como canais separados.

## Fontes primárias

- [vercel-labs/skills — código e README do CLI](https://github.com/vercel-labs/skills)
- [skills.sh — documentação do diretório e telemetria](https://www.skills.sh/docs)
- [Agent Skills — especificação aberta](https://agentskills.io/specification)
- [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI — Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [OpenAI Help — Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt/)
- [OpenAI Help — ChatGPT Workspace Agents](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business)
