# 📚 Atividade: Testes Funcionais com Pytest

## 🎯 Objetivos da Atividade

Esta atividade prática tem como objetivo aplicar os critérios de **Particionamento em Classes de Equivalência** e **Análise de Valor Limite** para desenvolver testes funcionais automatizados usando **pytest**.

## 👥 Informações Gerais

- **Disciplina**: Teste de Software
- **Tema**: Testes Funcionais
- **Formato**: Duplas

## 📋 Instruções

### 1. Configuração do Ambiente

```bash
# Clone o repositório (se ainda não fez)
cd sistema_pei

# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements/local.txt

# Teste se o ambiente está funcionando
pytest tests_templates/test_00_exemplo_completo.py
```

### 2. Estrutura dos Arquivos

Você encontrará 4 arquivos de teste:

- `test_00_exemplo_completo.py` - **Exemplo completo** (referência de implementação)
- `test_01_enrollment_validation.py` - **Validação de Matrícula** (notas e faltas)
- `test_02_offer_management.py` - **Gestão de Ofertas** (adicionar/remover alunos)
- `test_03_pei_status.py` - **Status do PEI** (atualização automática)

### 3. O Que Fazer

1. **Estude** o arquivo `test_00_exemplo_completo.py` para entender a estrutura
2. **Implemente** os testes nos arquivos seguindo as orientações
3. **Execute** cada teste com: `pytest tests_templates/test_XX_nome.py -v`
4. **Documente** seu planejamento no arquivo `RELATORIO_EQUIPE.md`
5. **Capture** os resultados da execução dos testes

### 4. Técnicas a Aplicar

#### Classes de Equivalência (CE)
Agrupe entradas em partições que serão tratadas da mesma forma pelo sistema:
- **Partições Válidas**: Entradas aceitas pelo sistema
- **Partições Inválidas**: Entradas rejeitadas pelo sistema

#### Análise de Valor Limite (VL)
Teste os valores nos limites das partições:
- Valores imediatamente **antes**, **no** e **depois** do limite

### 5. Exemplo de Aplicação

**Funcionalidade**: Campo `grade` (nota) deve aceitar valores de 0 a 100

**Classes de Equivalência:**

| Partição | Válida/Inválida | Valores |
|----------|-----------------|---------|
| CE1: Abaixo do mínimo | Inválida | < 0 |
| CE2: Dentro do intervalo | Válida | 0 ≤ x ≤ 100 |
| CE3: Acima do máximo | Inválida | > 100 |

**Valores Limite:**

| Limite | Valores de Teste |
|--------|------------------|
| Mínimo | -0.01, 0, 0.01 |
| Máximo | 99.99, 100, 100.01 |

## 📊 Entregáveis

1. **Código dos Testes** (arquivos `.py` completados)
2. **Relatório de Planejamento** (`RELATORIO_EQUIPE.md`)
3. **Capturas de Tela** da execução dos testes

## ✅ Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| Planejamento | 30% | Aplicação correta dos critérios CE e VL |
| Implementação | 40% | Testes implementados corretamente |
| Cobertura | 15% | Diversidade de cenários testados |
| Documentação | 10% | Relatório claro e completo |
| Execução | 5% | Todos os testes passam |

## 🔧 Comandos Úteis

```bash
# Executar um arquivo específico
pytest tests_templates/test_01_enrollment_basico.py -v

# Executar todos os testes da pasta
pytest tests_templates/ -v

# Executar com cobertura
pytest tests_templates/ --cov=sistema_pei --cov-report=html

# Executar apenas testes que falharam
pytest tests_templates/ --lf

# Ver saída detalhada (print statements)
pytest tests_templates/ -v -s
```

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Django](https://pytest-django.readthedocs.io/)
- [Factory Boy](https://factoryboy.readthedocs.io/)

## ❓ Dúvidas Frequentes

**P: O que são fixtures?**
R: São funções que fornecem dados reutilizáveis para os testes. Exemplo: `@pytest.fixture` para criar objetos.

**P: O que são factories?**
R: Classes que criam objetos de teste com dados realistas de forma fácil. Exemplo: `UserFactory()`.

**P: Como testar exceções?**
R: Use `pytest.raises()`:
```python
with pytest.raises(ValidationError):
    funcao_que_deve_falhar()
```

**P: Por que usar `pytestmark = pytest.mark.django_db`?**
R: Permite que os testes acessem o banco de dados do Django.

## 🎓 Bom Trabalho

Lembre-se: o objetivo não é apenas fazer os testes passarem, mas **entender** e **aplicar** os critérios de teste funcional!
