# Relatório de Planejamento de Testes Funcionais

---

## 🎯 Objetivo da Atividade

Aplicar técnicas de **Particionamento em Classes de Equivalência** e **Análise de Valor Limite** para desenvolver testes funcionais automatizados usando pytest no Sistema PEI.

---

## 📊 Funcionalidades Testadas

### Funcionalidade 1: [Nome da Funcionalidade]

**Descrição**: _Descreva brevemente o que a funcionalidade faz_

**Módulo**: `[nome do módulo]`

**Método/Função Testada**: `[nome do método]`

#### Classes de Equivalência Identificadas

| ID  | Descrição da Partição | Válida/Inválida | Valores de Exemplo |
|-----|----------------------|-----------------|-------------------|
| CE1 | [Descrição]          | [Válida/Inválida] | [Exemplos]      |
| CE2 | [Descrição]          | [Válida/Inválida] | [Exemplos]      |
| ... | ...                  | ...             | ...               |

#### Valores Limite Identificados

| Campo/Limite | Valores Testados | Justificativa |
|--------------|------------------|---------------|
| [Campo]      | [valores]        | [Por que esses valores?] |
| ...          | ...              | ...           |

#### Casos de Teste Implementados

| ID   | Nome do Teste | Critério | Entrada | Saída Esperada | Status |
|------|---------------|----------|---------|----------------|--------|
| TC01 | test_xxx      | CE/VL    | [dados] | [resultado]    | ✅/❌   |
| TC02 | test_yyy      | CE/VL    | [dados] | [resultado]    | ✅/❌   |
| ...  | ...           | ...      | ...     | ...            | ...    |

---

### Funcionalidade 2: [Nome da Funcionalidade]

_Repita a estrutura acima para cada funcionalidade testada_

---

## 💻 Implementação

### Tecnologias Utilizadas

- **Framework de Teste**: pytest
- **Extensão Django**: pytest-django
- **Factories**: Factory Boy
- **Banco de Dados**: SQLite (teste)

### Estrutura dos Testes

```
tests_templates/
├── test_00_exemplo_completo.py (exemplo de referência)
├── test_01_enrollment_validation.py (validação de matrículas)
├── test_02_offer_management.py (gestão de ofertas)
└── test_03_pei_status.py (status do PEI)
```

---

## 📈 Resultados da Execução

### Resumo Geral

**Total de Testes**: X

**Passaram**: Y ✅

**Falharam**: Z ❌

**Cobertura de Código**: XX%

### Cobertura de Testes

**Cenários válidos testados**: X

**Cenários inválidos testados**: Y

**Cenários não testados** _(se houver)_:

- [Cenário 1 - Justificativa]
- [Cenário 2 - Justificativa]

### Bugs/Problemas Encontrados

_Liste quaisquer bugs ou comportamentos inesperados que vocês encontraram durante os testes:_

1. **[Descrição do problema]**
   - Teste que encontrou: `test_xxx`
   - Comportamento esperado: ...
   - Comportamento observado: ...

---

## ✅ Checklist de Entrega

- [ ] Todos os arquivos de teste implementados
- [ ] Relatório completo preenchido
- [ ] Screenshots dos testes executando
- [ ] Documentação de cada teste (docstrings)
- [ ] Tabelas de CE e VL preenchidas
- [ ] Análise crítica realizada
- [ ] Código comentado quando necessário

---

**Assinaturas:**

_Integrante 1:_ ___________________________

_Integrante 2:_ ___________________________
